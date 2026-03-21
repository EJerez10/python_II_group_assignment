import streamlit as st
import pandas as pd
import joblib
from dotenv import load_dotenv
import os

from pysimfin import PySimFin
from etl_pipeline import build_etl_dataset

load_dotenv()

st.title("📈 Model Signals")
st.caption("Generate a model-based trading recommendation using recent market data.")

api_key = os.getenv("SIMFIN_API_KEY") or st.secrets["SIMFIN_API_KEY"]

if not api_key:
    st.error("API key not found. Check your .env file.")
    st.stop()

simfin = PySimFin(api_key)
loaded_model = joblib.load("gradient_boosting_model.joblib")

st.sidebar.header("Signal Inputs")

ticker = st.sidebar.selectbox(
    "Popular Tickers",
    ["AAPL", "MSFT", "TSLA", "AMZN", "GOOG", "NVDA"]
)

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-12-31"))

if st.button("Generate Signal"):
    try:
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
        recent_change_pct = ((recent_close.iloc[-1] - recent_close.iloc[0]) / recent_close.iloc[0]) * 100

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

        col1, col2, col3 = st.columns(3)
        col1.metric("Ticker", ticker)
        col2.metric("Recommendation", signal_label)
        col3.metric("Latest Close", f"{latest_close:.2f}")

        if signal_style == "success":
            st.success(signal_message)
        elif signal_style == "warning":
            st.warning(signal_message)
        else:
            st.error(signal_message)

        with st.expander("View processed features used for prediction"):
            st.dataframe(latest_row.round(3), use_container_width=True)

    except Exception as e:
        st.error(f"Error generating signal: {e}")