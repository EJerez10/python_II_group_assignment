import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

from pysimfin import PySimFin

load_dotenv()

st.title("📊 Go Live")

api_key = os.getenv("SIMFIN_API_KEY")

if not api_key:
    st.error("API key not found. Check your .env file.")
    st.stop()

simfin = PySimFin(api_key)

st.sidebar.header("Market Inputs")

popular_ticker = st.sidebar.selectbox(
    "Popular Tickers",
    ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL", "NVDA"]
)

ticker = st.sidebar.text_input(
    "Or type any ticker",
    value=popular_ticker
).upper().strip()

chart_type = st.sidebar.radio("Chart Type", ["Line", "Candlestick"])
show_ma10 = st.sidebar.checkbox("Show 10-day MA", value=True)
show_ma20 = st.sidebar.checkbox("Show 20-day MA", value=False)

start_date = st.sidebar.date_input("Start Date", date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", date(2023, 3, 31))

if start_date > end_date:
    st.error("Start date must be before end date.")
    st.stop()

df = simfin.get_share_prices(ticker, str(start_date), str(end_date))

if df.empty:
    st.warning("No data returned.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").copy()

df["MA_10"] = df["Close"].rolling(10).mean()
df["MA_20"] = df["Close"].rolling(20).mean()

latest_close = df["Close"].iloc[-1]
latest_volume = df["Volume"].iloc[-1]
period_high = df["High"].max()
period_low = df["Low"].min()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest Close", f"{latest_close:,.2f}")
col2.metric("Latest Volume", f"{latest_volume:,.0f}")
col3.metric("Period High", f"{period_high:,.2f}")
col4.metric("Period Low", f"{period_low:,.2f}")

st.subheader(f"{ticker} Price Chart")
st.caption(f"Showing {ticker} data from {start_date} to {end_date}")

if chart_type == "Line":
    fig_price = px.line(
        df,
        x="Date",
        y="Close",
        title=f"{ticker} Share Price"
    )

    if show_ma10:
        fig_price.add_scatter(
            x=df["Date"],
            y=df["MA_10"],
            mode="lines",
            name="10-day MA"
        )

    if show_ma20:
        fig_price.add_scatter(
            x=df["Date"],
            y=df["MA_20"],
            mode="lines",
            name="20-day MA"
        )

else:
    fig_price = go.Figure(data=[go.Candlestick(
        x=df["Date"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Price"
    )])

    if show_ma10:
        fig_price.add_scatter(
            x=df["Date"],
            y=df["MA_10"],
            mode="lines",
            name="10-day MA"
        )

    if show_ma20:
        fig_price.add_scatter(
            x=df["Date"],
            y=df["MA_20"],
            mode="lines",
            name="20-day MA"
        )

    fig_price.update_layout(
        title=f"{ticker} Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price"
    )

st.plotly_chart(fig_price, use_container_width=True)

st.subheader(f"{ticker} Trading Volume")
fig_vol = px.bar(
    df,
    x="Date",
    y="Volume",
    title=f"{ticker} Volume"
)
st.plotly_chart(fig_vol, use_container_width=True)

with st.expander("View Raw Market Data"):
    st.dataframe(df, use_container_width=True)