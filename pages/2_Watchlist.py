import os
from datetime import date
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from pysimfin import PySimFin

load_dotenv()

st.title("👀 Watchlist")
st.caption("Track selected stocks and view their latest available performance for a chosen date.")

api_key = os.getenv("SIMFIN_API_KEY") or st.secrets["SIMFIN_API_KEY"]

if not api_key:
    st.error("API key not found.")
    st.stop()

simfin = PySimFin(api_key)

watchlist = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "TSLA": "Tesla Inc.",
    "AMZN": "Amazon.com Inc.",
    "GOOG": "Alphabet Inc.",
    "NVDA": "NVIDIA Corp.",
    "META": "Meta Platforms Inc.",
    "SPOT": "Spotify Technology S.A."
}

@st.cache_data(show_spinner=False)
def load_watchlist_data():
    all_rows = []

    for ticker, company in watchlist.items():
        df = simfin.get_share_prices(ticker, "2023-01-01", str(date.today()))

        if df.empty:
            continue

        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date").copy()
        df["Ticker"] = ticker
        df["Company"] = company

        all_rows.append(df)

    if not all_rows:
        return pd.DataFrame()

    return pd.concat(all_rows, ignore_index=True)

all_data = load_watchlist_data()

if all_data.empty:
    st.warning("No watchlist data returned from SimFin.")
    st.stop()

latest_available = all_data["Date"].max().date()

# Controls
control_col1, control_col2 = st.columns([2, 1])

with control_col1:
    selected_tickers = st.multiselect(
        "Select stocks",
        options=list(watchlist.keys()),
        default=list(watchlist.keys())
    )

with control_col2:
    snapshot_date = st.date_input(
        "Snapshot date",
        value=latest_available,
        max_value=latest_available
    )

if not selected_tickers:
    st.warning("Please select at least one stock.")
    st.stop()

filtered_data = all_data[all_data["Ticker"].isin(selected_tickers)].copy()

# For each ticker, get the latest available row on or before snapshot_date
snapshot_rows = []

for ticker in selected_tickers:
    stock_df = filtered_data[
        (filtered_data["Ticker"] == ticker) &
        (filtered_data["Date"].dt.date <= snapshot_date)
    ].sort_values("Date")

    if stock_df.empty:
        continue

    latest_row = stock_df.iloc[-1]

    # previous close for change calculation
    prev_rows = stock_df.iloc[:-1]
    if not prev_rows.empty:
        prev_close = prev_rows.iloc[-1]["Close"]
    else:
        prev_close = latest_row["Close"]

    change = latest_row["Close"] - prev_close
    change_pct = (change / prev_close * 100) if prev_close != 0 else 0

    snapshot_rows.append({
        "Company": latest_row["Company"],
        "Ticker": latest_row["Ticker"],
        "Date": latest_row["Date"].date(),
        "Last Price": round(latest_row["Close"], 2),
        "Change": round(change, 2),
        "Change %": round(change_pct, 2),
        "Volume (M)": round(latest_row["Volume"] / 1_000_000, 1)
    })

watchlist_df = pd.DataFrame(snapshot_rows)

watchlist_df = watchlist_df[
    ["Ticker", "Company", "Date", "Last Price", "Change", "Change %", "Volume (M)"]
]

if watchlist_df.empty:
    st.warning("No data available for the selected stocks and date.")
    st.stop()

# Summary metrics
gainers = (watchlist_df["Change"] > 0).sum()
losers = (watchlist_df["Change"] < 0).sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Stocks Displayed", len(watchlist_df))
col2.metric("Gainers", int(gainers))
col3.metric("Losers", int(losers))
col4.metric("Latest Available API Date", str(latest_available))

st.caption(f"Showing watchlist snapshot for {snapshot_date} using the latest available trading day on or before that date.")

# Style helpers
def color_change(val):
    if pd.isna(val):
        return ""
    if val > 0:
        return "color: green;"
    if val < 0:
        return "color: red;"
    return ""

styled_df = (
    watchlist_df.style
    .format({
        "Last Price": "${:,.2f}",
        "Change": "{:+.2f}",
        "Change %": "{:+.2f}%",
        "Volume (M)": "{:,.1f}M"
    })
    .map(color_change, subset=["Change", "Change %"])
)

st.markdown("---")
st.subheader("Watchlist Snapshot")
st.dataframe(styled_df, use_container_width=True)

with st.expander("View raw watchlist data"):
    st.dataframe(
        filtered_data.sort_values(["Ticker", "Date"]),
        use_container_width=True
    )