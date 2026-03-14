import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# Fake stand-in dataset
# ------------------------------
@st.cache_data
def load_fake_data():
    return pd.DataFrame({
        "ticker": ["AAPL", "AAPL", "AAPL", "MSFT", "MSFT", "MSFT"],
        "year":   [2021, 2022, 2023, 2021, 2022, 2023],
        "revenue":    [365_817, 394_328, 383_285, 168_088, 198_270, 211_915],
        "net_income": [94_680,  99_803,  97_000,  61_271,  72_738,  75_000],
    })

df = load_fake_data()

# ------------------------------
# Sidebar controls
# ------------------------------
st.sidebar.header("Filters")

ticker = st.sidebar.selectbox("Ticker", sorted(df["ticker"].unique()))

year_min, year_max = st.sidebar.slider(
    "Year range",
    int(df["year"].min()),
    int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max()))
)

filtered = df[(df["ticker"] == ticker) & (df["year"].between(year_min, year_max))].copy()

# ------------------------------
# Main layout
# ------------------------------
st.title("📊 Financial Dashboard (Stand-in Data)")

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"{filtered['revenue'].sum():,}")
col2.metric("Total Net Income", f"{filtered['net_income'].sum():,}")
col3.metric("Rows", f"{len(filtered)}")

st.subheader("Trend")
fig = px.line(filtered, x="year", y=["revenue", "net_income"], markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Raw Data")
st.dataframe(filtered, use_container_width=True)