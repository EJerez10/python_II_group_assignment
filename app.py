import streamlit as st

st.set_page_config(page_title="Raviolution", layout="wide")

st.title("📈 Raviolution")
st.subheader("AI-Powered Trading Dashboard")

st.markdown("""
Welcome to **Raviolution**, a web-based trading system designed to help users explore market data,
monitor selected stocks, and generate machine-learning-based trading recommendations.

This platform combines:
- **SimFin financial market data**
- **Interactive visualizations**
- **A machine learning model for stock recommendations**
""")

st.markdown("---")

st.subheader("What you can do in this app")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
### 👀 Watchlist
View your selected stocks in one place, including:
- latest price
- daily change
- trading volume
""")

    st.markdown("""
### 📊 Stock Overview
Inspect a specific stock in more detail:
- price chart
- candlestick chart
- moving averages
- timeframe filters
""")

with col2:
    st.markdown("""
### 🤖 Recommendations
Generate a model-based signal for a selected stock:
- BUY
- HOLD / WATCH
- SELL / HOLD
""")

    st.markdown("""
### 👥 Team
Learn more about the creators of the project and the motivation behind the system.
""")

st.markdown("---")

st.info("Use the navigation menu on the left to explore the platform.")