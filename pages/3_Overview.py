import os
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from pysimfin import PySimFin

load_dotenv()

st.title("📊 Stock Overview")

api_key = os.getenv("SIMFIN_API_KEY") or st.secrets["SIMFIN_API_KEY"]
if not api_key:
    st.error("API key not found. Check your .env file or Streamlit secrets.")
    st.stop()

simfin = PySimFin(api_key)

# ---------------------------
# Ticker selector near title
# ---------------------------
ticker_col1, ticker_col2 = st.columns([2, 3])

with ticker_col1:
    ticker = st.selectbox(
        "Select Stock",
        ["AAPL", "MSFT", "TSLA", "AMZN", "GOOG", "NVDA", "META", "SPOT"]
    )

with ticker_col2:
    st.caption("Explore historical price action, moving averages, and recent trading patterns.")

# ---------------------------
# Fetch broad range first
# ---------------------------
today = date.today()
df_all = simfin.get_share_prices(ticker, "2023-01-01", str(today))

if df_all.empty:
    st.warning("No data returned for this ticker.")
    st.stop()

df_all["Date"] = pd.to_datetime(df_all["Date"])
latest_available = df_all["Date"].max().date()

# ---------------------------
# Main-page controls
# ---------------------------
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
    show_ma10 = st.checkbox("10-day MA", value=False)

with ma_col2:
    show_ma20 = st.checkbox("20-day MA", value=False)

with ma_col3:
    manual_dates = st.toggle("Use custom dates", value=False)

if manual_dates:
    date_col1, date_col2 = st.columns(2)
    with date_col1:
        start_date = st.date_input("Start Date", date(2023, 1, 1))
    with date_col2:
        end_date = st.date_input("End Date", latest_available, max_value=latest_available)
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
# Filter from broad data
# ---------------------------
df = df_all[
    (df_all["Date"].dt.date >= start_date) &
    (df_all["Date"].dt.date <= end_date)
].copy()

if df.empty:
    st.warning("No data returned for the selected ticker and date range.")
    st.stop()

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

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Average Volume", f"{avg_volume:,.0f}")
metric_col2.metric("Trading Days", len(df))
metric_col3.metric("Data Current As Of", str(latest_available))

st.caption(f"Showing {ticker} data from {start_date} to {end_date}")

# Moving average warnings
ma_notes = []
if show_ma10 and len(df) < 10:
    ma_notes.append("Not enough history in the selected window to fully display the 10-day moving average.")
if show_ma20 and len(df) < 20:
    ma_notes.append("Not enough history in the selected window to fully display the 20-day moving average.")

for note in ma_notes:
    st.info(note)

st.markdown("---")

# ---------------------------
# Main price chart
# ---------------------------
st.subheader(f"{ticker} Price Chart")

if chart_type == "Line":
    fig_price = px.line(
        df,
        x="Date",
        y="Close",
        title=f"{ticker} Stock Price"
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
    fig_price = px.line(
        df,
        x="Date",
        y="Close",
        title=f"{ticker} Stock Price"
    )

    # Make price line neutral (black)
    fig_price.update_traces(
        line=dict(color="black", width=2),
        name="Price"
    )

    if show_ma10:
        fig_price.add_scatter(
            x=df["Date"],
            y=df["MA_10"],
            mode="lines",
            name="10-day MA",
            line=dict(color="#60A5FA", width=2)  # light blue
        )

    if show_ma20:
        fig_price.add_scatter(
            x=df["Date"],
            y=df["MA_20"],
            mode="lines",
            name="20-day MA",
            line=dict(color="#1D4ED8", width=2)  # darker blue
        )

st.plotly_chart(fig_price, use_container_width=True)

# Optional candlestick alternative
if chart_type == "Candlestick":
    with st.expander("View Candlestick Chart"):
        import plotly.graph_objects as go

        fig_candle = go.Figure(data=[go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price"
        )])

        if show_ma10:
            fig_candle.add_scatter(
                x=df["Date"],
                y=df["MA_10"],
                mode="lines",
                name="10-day MA"
            )

        if show_ma20:
            fig_candle.add_scatter(
                x=df["Date"],
                y=df["MA_20"],
                mode="lines",
                name="20-day MA"
            )

        fig_candle.update_layout(
            title=f"{ticker} Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            height=500
        )

        st.plotly_chart(fig_candle, use_container_width=True)

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
# Recent trading patterns
# ---------------------------
st.markdown("---")
st.subheader("Recent Trading Patterns")

recent_5d_change = (
    ((df["Close"].iloc[-1] - df["Close"].iloc[-5]) / df["Close"].iloc[-5]) * 100
    if len(df) >= 5 else 0
)

volume_ratio = latest_volume / avg_volume if avg_volume != 0 else 1

latest_ma10 = df["MA_10"].iloc[-1] if not pd.isna(df["MA_10"].iloc[-1]) else None
latest_ma20 = df["MA_20"].iloc[-1] if not pd.isna(df["MA_20"].iloc[-1]) else None

pattern_points = []

if recent_5d_change > 2:
    pattern_points.append(
        f"📈 {ticker} is up **{recent_5d_change:.2f}%** over the last 5 trading days, showing short-term strength."
    )
elif recent_5d_change < -2:
    pattern_points.append(
        f"📉 {ticker} is down **{abs(recent_5d_change):.2f}%** over the last 5 trading days, reflecting recent weakness."
    )
else:
    pattern_points.append(
        f"➖ {ticker} has moved **{recent_5d_change:.2f}%** over the last 5 trading days, indicating relatively stable short-term performance."
    )

if latest_ma10 is not None:
    if latest_close > latest_ma10:
        pattern_points.append(
            "✅ The latest closing price is above the 10-day moving average, suggesting near-term bullish momentum."
        )
    else:
        pattern_points.append(
            "⚠️ The latest closing price is below the 10-day moving average, which may indicate weaker short-term momentum."
        )

if latest_ma20 is not None:
    if latest_close > latest_ma20:
        pattern_points.append(
            "✅ The stock is trading above its 20-day moving average, reinforcing a stronger medium-term trend."
        )
    else:
        pattern_points.append(
            "⚠️ The stock is trading below its 20-day moving average, which may reflect softer medium-term sentiment."
        )

if volume_ratio > 1.3:
    pattern_points.append(
        f"🔊 Trading volume is elevated at **{volume_ratio:.2f}x** the recent average, which may indicate increased market attention."
    )
else:
    pattern_points.append(
        "📊 Trading volume is close to its recent average, suggesting normal trading activity."
    )

pattern_col1, pattern_col2 = st.columns([2, 1])

with pattern_col1:
    for point in pattern_points:
        st.write(point)

with pattern_col2:
    st.metric("5-Day Change", f"{recent_5d_change:+.2f}%")
    st.metric("Average Volume", f"{avg_volume:,.0f}")
    st.metric("Timeframe", timeframe if not manual_dates else "Custom")

# ---------------------------
# Raw data
# ---------------------------
with st.expander("View Raw Market Data"):
    st.dataframe(df.round(3), use_container_width=True)