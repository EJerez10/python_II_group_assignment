import os
from datetime import date, timedelta

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from pysimfin import PySimFin

load_dotenv()

st.title("👀 Watchlist")
st.caption("Track key market information for our selected stocks.")

api_key = os.getenv("SIMFIN_API_KEY") or st.secrets["SIMFIN_API_KEY"]

if not api_key:
    st.error("API key not found.")
    st.stop()

simfin = PySimFin(api_key)

# Fixed watchlist
watchlist = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "TSLA": "Tesla Inc.",
    "AMZN": "Amazon.com Inc.",
    "GOOGL": "Alphabet Inc.",
    "NVDA": "NVIDIA Corp.",
    "META": "Meta Platforms Inc.",
    "SPOT": "Spotify Technology S.A."
}

@st.cache_data(show_spinner=False)
def get_watchlist_row(ticker, company):
    # Broad fetch first
    broad_start = "2023-01-01"
    broad_end = date.today().isoformat()

    df = simfin.get_share_prices(ticker, broad_start, broad_end)

    if df.empty:
        return {
            "Company": company,
            "Ticker": ticker,
            "Last Price": None,
            "Change": None,
            "Change %": None,
            "Volume": None
        }

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").copy()

    # Use latest available SimFin date, not today's date
    latest_available = df["Date"].max()
    df = df[df["Date"] <= latest_available].copy()

    latest = df.iloc[-1]
    previous_close = df.iloc[-2]["Close"] if len(df) > 1 else latest["Close"]

    change = latest["Close"] - previous_close
    change_pct = (change / previous_close * 100) if previous_close != 0 else 0

    return {
        "Company": company,
        "Ticker": ticker,
        "Last Price": round(latest["Close"], 2),
        "Change": round(change, 2),
        "Change %": round(change_pct, 2),
        "Volume": int(latest["Volume"]),
        "As Of": latest_available.date()
    }

latest_snapshot = watchlist_df["As Of"].dropna().max()
st.caption(f"Watchlist based on latest available SimFin data: {latest_snapshot}")

with st.spinner("Loading watchlist..."):
    rows = [get_watchlist_row(ticker, company) for ticker, company in watchlist.items()]

watchlist_df = pd.DataFrame(rows)

# Optional formatting helpers
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
        "Volume": "{:,.0f}"
    }, na_rep="N/A")
    .map(color_change, subset=["Change", "Change %"])
)

# Top summary row
valid_prices = watchlist_df["Last Price"].notna().sum()
gainers = (watchlist_df["Change"] > 0).sum()
losers = (watchlist_df["Change"] < 0).sum()

col1, col2, col3 = st.columns(3)
col1.metric("Stocks Tracked", len(watchlist_df))
col2.metric("Gainers", int(gainers))
col3.metric("Losers", int(losers))

st.markdown("---")

st.subheader("Watchlist Snapshot")
st.dataframe(styled_df, use_container_width=True)

st.info("Use the Overview page to inspect a stock in detail, and the Recommendations page to view the ML-based trading signal.")