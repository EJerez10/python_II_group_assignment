import os
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

from pysimfin import PySimFin

load_dotenv()

st.title("📊 Go Live")

api_key = os.getenv("SIMFIN_API_KEY") or st.secrets["SIMFIN_API_KEY"]
if not api_key:
    st.error("API key not found. Check your .env file.")
    st.stop()

simfin = PySimFin(api_key)

# ---------------------------
# Sidebar: ticker selection
# ---------------------------
st.sidebar.header("Market Inputs")

ticker = st.sidebar.selectbox(
    "Popular Tickers",
    ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL", "NVDA", "META", "SPOT"]
)

# ---------------------------
# Main-page chart controls
# ---------------------------
today = date.today()

df_all = simfin.get_share_prices(ticker, "2023-01-01", str(today))

if df_all.empty:
    st.warning("No data returned for this ticker.")
    st.stop()

df_all["Date"] = pd.to_datetime(df_all["Date"])
latest_available = df_all["Date"].max().date()

st.subheader(ticker)
st.caption("Live market view with customizable chart controls.")

control_col1, control_col2 = st.columns([2, 2])

with control_col1:
    timeframe = st.radio(
        "Timeframe",
        ["5D", "1M", "3M", "6M", "YTD", "1Y"],
        horizontal=True
    )

with control_col2:
    chart_type = st.radio(
        "Chart Type",
        ["Line", "Candlestick"],
        horizontal=True
    )

ma_col1, ma_col2, ma_col3 = st.columns([1, 1, 3])

with ma_col1:
    show_ma10 = st.checkbox("Show 10-day MA", value=True)

with ma_col2:
    show_ma20 = st.checkbox("Show 20-day MA", value=False)

with ma_col3:
    manual_dates = st.toggle("Use custom dates", value=False)

if manual_dates:
    date_col1, date_col2 = st.columns(2)
    with date_col1:
        start_date = st.date_input("Start Date", date(2023, 1, 1))
    with date_col2:
        end_date = st.date_input("End Date", today)
else:
    if timeframe == "5D":
        start_date = latest_available - timedelta(days=7)
    elif timeframe == "1M":
        start_date = latest_available - timedelta(days=30)
    elif timeframe == "3M":
        start_date = latest_available - timedelta(days=90)
    elif timeframe == "6M":
        start_date = latest_available - timedelta(days=180)
    elif timeframe == "YTD":
        start_date = date(latest_available.year, 1, 1)
    else:  # 1Y
        start_date = latest_available - timedelta(days=365)

    end_date = latest_available


if start_date > end_date:
    st.error("Start date must be before end date.")
    st.stop()

# ---------------------------
# Fetch data
# ---------------------------
with st.spinner("Loading market data..."):
    df = simfin.get_share_prices(ticker, str(start_date), str(end_date))

if df.empty:
    st.warning("No data returned for the selected ticker and date range.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").copy()

# Moving averages
df["MA_10"] = df["Close"].rolling(10).mean()
df["MA_20"] = df["Close"].rolling(20).mean()

# ---------------------------
# Price snapshot
# ---------------------------
latest_close = df["Close"].iloc[-1]
previous_close = df["Close"].iloc[-2] if len(df) > 1 else latest_close
price_delta = latest_close - previous_close
price_delta_pct = (price_delta / previous_close * 100) if previous_close != 0 else 0

period_high = df["High"].max()
period_low = df["Low"].min()
latest_volume = df["Volume"].iloc[-1]
avg_volume = df["Volume"].mean()

top_col1, top_col2, top_col3, top_col4 = st.columns(4)
top_col1.metric("Current Price", f"${latest_close:,.2f}", f"{price_delta:+.2f} ({price_delta_pct:+.2f}%)")
top_col2.metric("Period High", f"${period_high:,.2f}")
top_col3.metric("Period Low", f"${period_low:,.2f}")
top_col4.metric("Latest Volume", f"{latest_volume:,.0f}")

st.caption(f"Showing {ticker} data from {start_date} to {end_date}")

st.markdown("---")

# ---------------------------
# Main price chart
# ---------------------------
if chart_type == "Line":
    fig_price = px.line(
        df,
        x="Date",
        y="Close",
        title=f"{ticker} Price"
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

    fig_price.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        height=500
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
        yaxis_title="Price",
        height=500
    )

st.plotly_chart(fig_price, use_container_width=True)

# ---------------------------
# Volume chart
# ---------------------------
st.subheader(f"{ticker} Trading Volume")

fig_vol = px.bar(
    df,
    x="Date",
    y="Volume",
    title=f"{ticker} Volume"
)

fig_vol.update_layout(
    xaxis_title="Date",
    yaxis_title="Volume",
    height=350
)

st.plotly_chart(fig_vol, use_container_width=True)

# ---------------------------
# Company news placeholder
# ---------------------------
st.markdown("---")
st.subheader(f"📰 {ticker} News & Market Context")

news_col1, news_col2 = st.columns([2, 1])

with news_col1:
    st.info(
        "News feed placeholder: this section can later display recent headlines, "
        "company developments, and market-moving events related to the selected ticker."
    )

    st.markdown("""
**Example future content:**
- Latest earnings updates
- Analyst rating changes
- Major company announcements
- Sector-specific news
- Macroeconomic events affecting the stock
""")

with news_col2:
    st.metric("Average Volume", f"{avg_volume:,.0f}")
    st.metric("Trading Days", len(df))
    st.metric("Timeframe", timeframe if not manual_dates else "Custom")

# ---------------------------
# Raw data
# ---------------------------
with st.expander("View Raw Market Data"):
    st.dataframe(df.round(3), use_container_width=True)