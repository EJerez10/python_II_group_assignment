import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from dotenv import load_dotenv
import os

from pysimfin import PySimFin
from etl_pipeline import build_etl_dataset

load_dotenv()

st.title("📈 Model Signals")
st.caption("Generate a model-based trading recommendation using recent market data.")

api_key = os.getenv("SIMFIN_API_KEY") or st.secrets["SIMFIN_API_KEY"]

if not api_key:
    st.error("API key not found. Check your .env file or Streamlit secrets.")
    st.stop()

simfin = PySimFin(api_key)

MODEL_PATHS = {
    "AAPL": "gradient_boosting_AAPL.joblib",
    "MSFT": "gradient_boosting_MSFT.joblib",
    "TSLA": "gradient_boosting_TSLA.joblib",
    "AMZN": "gradient_boosting_AMZN.joblib",
    "GOOG": "gradient_boosting_GOOG.joblib",
    "NVDA": "gradient_boosting_NVDA.joblib",
    "META": "gradient_boosting_META.joblib",
    "SPOT": "gradient_boosting_SPOT.joblib",
}

@st.cache_resource
def load_model(model_path):
    return joblib.load(model_path)

st.sidebar.header("Signal Inputs")

ticker = st.sidebar.selectbox(
    "Popular Tickers",
    ["AAPL", "MSFT", "TSLA", "AMZN", "GOOG", "NVDA", "META", "SPOT"]
)

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-12-31"))

if start_date > end_date:
    st.error("Start date must be before end date.")
    st.stop()

if st.button("Generate Signal"):
    with st.spinner("Fetching market data, engineering features, and generating recommendation..."):
        try:
            model_path = MODEL_PATHS.get(ticker)

            if not model_path:
                st.error(f"No model found for ticker {ticker}.")
                st.stop()

            loaded_model = load_model(model_path)

            raw_df = simfin.get_share_prices(ticker, str(start_date), str(end_date))

            if raw_df.empty:
                st.error("No data returned from SimFin.")
                st.stop()

            if "Date" in raw_df.columns:
                raw_df["Date"] = pd.to_datetime(raw_df["Date"])
                raw_df = raw_df.set_index("Date")

            processed_df = build_etl_dataset(raw_df, live_inference=True)

            if processed_df.empty:
                st.error("Processed dataset is empty. Not enough historical rows for indicators.")
                st.stop()

            latest_row = processed_df.iloc[[-1]]
            prediction = loaded_model.predict(latest_row)[0]

            latest_close = latest_row["Close"].iloc[0]

            recent_close = raw_df["Close"].tail(5)
            recent_change_pct = (
                (recent_close.iloc[-1] - recent_close.iloc[0]) / recent_close.iloc[0]
            ) * 100

            if prediction == 1:
                if recent_change_pct > 2:
                    signal_label = "BUY"
                    signal_message = "The stock has shown recent upward momentum, and the model predicts further gains."
                    signal_style = "success"
                elif recent_change_pct < -2:
                    signal_label = "BUY"
                    signal_message = "The model suggests a possible rebound despite recent weakness."
                    signal_style = "success"
                else:
                    signal_label = "BUY"
                    signal_message = "The model predicts tomorrow's close may move higher."
                    signal_style = "success"
            else:
                if recent_change_pct > 2:
                    signal_label = "HOLD / WATCH"
                    signal_message = "The stock has been rising recently, but the model does not confirm continued upside. Keep an eye on it over the coming days."
                    signal_style = "warning"
                elif recent_change_pct < -2:
                    signal_label = "SELL / HOLD"
                    signal_message = "Recent price action has been weak, and the model does not suggest a near-term recovery."
                    signal_style = "error"
                else:
                    signal_label = "HOLD"
                    signal_message = "The model predicts limited upside in the near term."
                    signal_style = "warning"

            st.markdown("---")
            st.subheader(f"Recommendation for {ticker}")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Ticker", ticker)
            col2.metric("Recommendation", signal_label)
            col3.metric("Latest Close", f"${latest_close:,.2f}")
            col4.metric("5-Day Change", f"{recent_change_pct:+.2f}%")

            st.caption(f"Model used: {model_path}")

            if signal_style == "success":
                st.success(signal_message)
            elif signal_style == "warning":
                st.warning(signal_message)
            else:
                st.error(signal_message)

            # Optional probability if supported
            if hasattr(loaded_model, "predict_proba"):
                prob_up = loaded_model.predict_proba(latest_row)[0][1]
                st.metric("Probability of Price Increase", f"{prob_up:.1%}")

            st.markdown("---")
            st.subheader("Recent Price Trend")

            chart_df = raw_df.reset_index().copy()
            fig = px.line(
                chart_df.tail(30),
                x="Date",
                y="Close",
                title=f"{ticker} Recent Closing Prices"
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Signal Summary")
            st.info(
                f"For **{ticker}**, the model currently suggests **{signal_label}**. "
                f"This recommendation is based on the latest available engineered market features "
                f"and recent short-term price behavior."
            )

            with st.expander("Why did the model give this signal?"):
                st.write("""
This recommendation is based on engineered market features such as:
- opening and closing price behavior
- short-term moving averages
- daily price change
- recent volume behavior

The model predicts whether the next trading session is likely to close higher or not.
                """)

            with st.expander("View processed features used for prediction"):
                st.dataframe(latest_row.round(3), use_container_width=True)

        except Exception as e:
            st.error(f"Error generating signal: {e}")