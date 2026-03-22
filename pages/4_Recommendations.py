import os
from datetime import date

import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

from pysimfin import PySimFin
from etl_pipeline import build_etl_dataset

#add up or down singaler

load_dotenv()

st.title("🤖 Recommendations")
st.caption("Generate a model-based trading recommendation using recent market data.")

api_key = os.getenv("SIMFIN_API_KEY") or st.secrets["SIMFIN_API_KEY"]

if not api_key:
    st.error("API key not found. Check your .env file or Streamlit secrets.")
    st.stop()

simfin = PySimFin(api_key)

MODEL_PATHS = {
    "AAPL": "models/gradient_boosting_AAPL.joblib",
    "MSFT": "models/gradient_boosting_MSFT.joblib",
    "TSLA": "models/gradient_boosting_TSLA.joblib",
    "AMZN": "models/gradient_boosting_AMZN.joblib",
    "GOOG": "models/gradient_boosting_GOOG.joblib",
    "NVDA": "models/gradient_boosting_NVDA.joblib",
    "META": "models/gradient_boosting_META.joblib",
    "SPOT": "models/gradient_boosting_SPOT.joblib",
}

@st.cache_resource
def load_model(model_path):
    return joblib.load(model_path)

st.subheader("Select Stock & Analysis Window")

input_col1, input_col2 = st.columns([2, 2])

with input_col1:
    ticker = st.selectbox(
        "Select Stock",
        ["AAPL", "MSFT", "TSLA", "AMZN", "GOOG", "NVDA", "META", "SPOT"]
    )

with input_col2:
    timeframe = st.radio(
        "Analysis Window",
        ["1M", "3M", "6M", "YTD", "1Y"],
        horizontal=True
    )

use_custom_range = st.toggle("Use Custom Date Range", value=False)

if use_custom_range:
    date_col1, date_col2 = st.columns(2)
    with date_col1:
        start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
    with date_col2:
        end_date = st.date_input("End Date", pd.to_datetime("2024-12-31"))

    if start_date > end_date:
        st.error("Start date must be before end date.")
        st.stop()
else:
    start_date = None
    end_date = None

if st.button("Generate Recommendation"):
    with st.spinner("Fetching market data, engineering features, and generating recommendation..."):
        try:
            model_path = MODEL_PATHS.get(ticker)

            if not model_path:
                st.error(f"No model found for ticker {ticker}.")
                st.stop()

            loaded_model = load_model(model_path)

            raw_df = simfin.get_share_prices(
                ticker,
                "2023-01-01",
                str(pd.Timestamp.today().date())
            )

            if raw_df.empty:
                st.error("No data returned from SimFin.")
                st.stop()

            raw_df["Date"] = pd.to_datetime(raw_df["Date"])
            latest_available = raw_df["Date"].max().date()

            if use_custom_range:
                if end_date > latest_available:
                    end_date = latest_available
            else:
                if timeframe == "1M":
                    start_date = latest_available - pd.Timedelta(days=30)
                elif timeframe == "3M":
                    start_date = latest_available - pd.Timedelta(days=90)
                elif timeframe == "6M":
                    start_date = latest_available - pd.Timedelta(days=180)
                elif timeframe == "YTD":
                    start_date = pd.Timestamp(
                        year=latest_available.year,
                        month=1,
                        day=1
                    ).date()
                else:  # 1Y
                    start_date = latest_available - pd.Timedelta(days=365)

                end_date = latest_available

            raw_df = raw_df[
                (raw_df["Date"].dt.date >= start_date) &
                (raw_df["Date"].dt.date <= end_date)
            ].copy()

            if raw_df.empty:
                st.error("No data available for the selected analysis window.")
                st.stop()

            raw_df = raw_df.sort_values("Date").copy()
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
                    signal_color = "green"
                    signal_bg = "#DCFCE7"
                    signal_text = "#166534"
                    zone_color = "rgba(34, 197, 94, 0.20)"
                elif recent_change_pct < -2:
                    signal_label = "BUY"
                    signal_message = "The model suggests a possible rebound despite recent weakness."
                    signal_color = "green"
                    signal_bg = "#DCFCE7"
                    signal_text = "#166534"
                    zone_color = "rgba(34, 197, 94, 0.20)"
                else:
                    signal_label = "BUY"
                    signal_message = "The model predicts tomorrow's close may move higher."
                    signal_color = "green"
                    signal_bg = "#DCFCE7"
                    signal_text = "#166534"
                    zone_color = "rgba(34, 197, 94, 0.20)"
            else:
                if recent_change_pct > 2:
                    signal_label = "HOLD / WATCH"
                    signal_message = "The stock has been rising recently, but the model does not confirm continued upside. Keep an eye on it over the coming days."
                    signal_color = "orange"
                    signal_bg = "#FEF3C7"
                    signal_text = "#92400E"
                    zone_color = "rgba(234, 179, 8, 0.22)"
                elif recent_change_pct < -2:
                    signal_label = "SELL / HOLD"
                    signal_message = "Recent price action has been weak, and the model does not suggest a near-term recovery."
                    signal_color = "red"
                    signal_bg = "#FEE2E2"
                    signal_text = "#991B1B"
                    zone_color = "rgba(239, 68, 68, 0.20)"
                else:
                    signal_label = "HOLD"
                    signal_message = "The model predicts limited upside in the near term."
                    signal_color = "orange"
                    signal_bg = "#FEF3C7"
                    signal_text = "#92400E"
                    zone_color = "rgba(234, 179, 8, 0.22)"

            st.markdown("---")
            st.subheader(f"Recommendation for {ticker}")

            # Up / Down label from raw model prediction
            direction_label = "UP" if prediction == 1 else "DOWN"
            direction_color = "#16A34A" if prediction == 1 else "#DC2626"

            # 5-day change color
            if recent_change_pct > 0:
                change_color = "#16A34A"
            elif recent_change_pct < 0:
                change_color = "#DC2626"
            else:
                change_color = "#6B7280"

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("Ticker", ticker)

            with col2:
                st.markdown(
                    f"""
                    <div style="margin-top: 0.1rem;">
                        <div style="font-size:0.95rem; color:#374151; font-weight:600;">Model Predicts</div>
                        <div style="font-size:2.8rem; font-weight:700; color:{direction_color}; line-height:1.1;">
                            {direction_label}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    f"""
                    <div style="margin-top: 0.1rem;">
                        <div style="font-size:0.95rem; color:#374151; font-weight:600;">Recommendation</div>
                        <div style="font-size:2.8rem; font-weight:700; color:{signal_color}; line-height:1.1;">
                            {signal_label}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col4:
                st.metric("Latest Close", f"${latest_close:,.2f}")

            with col5:
                st.markdown(
                    f"""
                    <div style="margin-top: 0.1rem;">
                        <div style="font-size:0.95rem; color:#374151; font-weight:600;">5-Day Change</div>
                        <div style="font-size:2.8rem; font-weight:700; color:{change_color}; line-height:1.1;">
                            {recent_change_pct:+.2f}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                f"""
                <div style="color:#6B7280; font-size:0.85rem; font-style:italic; margin-top:8px; margin-bottom:2px;">
                Model used: {model_path}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div style="color:#6B7280; font-size:0.85rem; font-style:italic; margin-bottom:12px;">
                Recommendation based on latest available data: {latest_available}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div style="
                    background-color:{signal_bg};
                    color:{signal_text};
                    padding:12px;
                    border-radius:10px;
                    font-size:0.95rem;
                    margin-bottom:12px;
                ">
                {signal_message}
                </div>
                """,
                unsafe_allow_html=True
            )
            if hasattr(loaded_model, "predict_proba"):
                prob_up = loaded_model.predict_proba(latest_row)[0][1]
                st.metric("Probability of Price Increase", f"{prob_up:.1%}")

            st.markdown("---")
            st.subheader("Recommendation Signal View")

            chart_df = raw_df.reset_index().copy()
            fig = px.line(
                chart_df.tail(30),
                x="Date",
                y="Close",
                title=f"{ticker} Recent Closing Prices"
            )

            fig.update_traces(
                line=dict(color="black", width=2),
                name="Price"
            )

            latest_x = chart_df["Date"].iloc[-1]

            fig.add_vline(
                x=latest_x,
                line_dash="dash",
                line_color="black"
            )

            fig.add_vrect(
                x0=latest_x,
                x1=latest_x + pd.Timedelta(days=5),
                fillcolor=zone_color,
                opacity=0.8,
                line_width=0
            )

            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Close Price",
                height=450
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

            with st.expander("View raw market data used for this recommendation"):
                st.dataframe(chart_df.tail(30), use_container_width=True)

        except Exception as e:
            st.error(f"Error generating recommendation: {e}")