from pysimfin import PySimFin
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.title("📊 Go Live")

api_key = "YOUR_API_KEY"  # placeholder for now
simfin = PySimFin(api_key)

@st.cache_data
def load_fake_data():
    return pd.DataFrame({
        "date": pd.date_range("2023-01-01", periods=10, freq="D"),
        "close": [100, 102, 101, 104, 106, 105, 107, 110, 108, 111],
        "ticker": ["AAPL"] * 10
    })

# --------------------------
# Sidebar controls first
# --------------------------
st.sidebar.header("Filters")

ticker = st.sidebar.selectbox("Ticker", ["AAPL", "MSFT", "TSLA", "AMZN"])

start_date = st.sidebar.date_input("Start Date", date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", date(2023, 1, 10))

# --------------------------
# Load data after inputs exist
# --------------------------
try:
    df = simfin.get_share_prices(ticker, str(start_date), str(end_date))

    if df.empty:
        st.warning("No API data returned. Using fallback sample data.")
        df = load_fake_data()

except Exception as e:
    st.warning(f"Using fallback sample data. Reason: {e}")
    df = load_fake_data()

# --------------------------
# If API data doesn't have date as a normal column,
# reset index so Plotly can use it
# --------------------------
if "date" not in df.columns:
    df = df.reset_index()

# try to rename likely date column if needed
if "Date" in df.columns and "date" not in df.columns:
    df = df.rename(columns={"Date": "date"})

if "Close" in df.columns and "close" not in df.columns:
    df = df.rename(columns={"Close": "close"})

# --------------------------
# Display
# --------------------------
st.subheader(f"{ticker} Price Chart")

if "date" in df.columns and "close" in df.columns:
    fig = px.line(
        df,
        x="date",
        y="close",
        title=f"{ticker} Price"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Data does not contain the expected 'date' and 'close' columns.")
    st.dataframe(df, use_container_width=True)

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)