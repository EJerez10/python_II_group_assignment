import streamlit as st

st.set_page_config(
    page_title="Raviolution",
    page_icon="📈",
    layout="wide"
)

st.image("assets/logo.jpg", width=180)

st.title("📈 Raviolution")
st.subheader("AI-Powered Trading Dashboard")

st.markdown("""
Welcome to **Raviolution**, a web-based trading system built to help users explore stock performance,
track selected companies, and generate machine-learning-based trading recommendations.

This platform combines:
- **SimFin market data**
- **Interactive visualizations**
- **A machine learning recommendation engine**
""")

st.markdown("---")

st.subheader("What You Can Do")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
### 👀 Watchlist
Monitor a curated list of major stocks and quickly compare:
- latest price
- daily change
- trading volume
""")

with col2:
    st.markdown("""
### 📊 Overview
Explore each stock in more detail with:
- price charts
- candlestick view
- moving averages
- timeframe filters
""")

with col3:
    st.markdown("""
### 🤖 Recommendations
Generate a model-based stock recommendation using:
- ticker-specific ML models
- engineered market features
- recent price behavior
""")

st.markdown("---")

st.subheader("Why We Built Raviolution")

st.write("""
We wanted to build a platform that makes market analysis more visual, more interactive,
and easier to understand. By combining financial data with machine learning in one place,
Raviolution provides a simplified trading dashboard experience inspired by real financial platforms.
""")