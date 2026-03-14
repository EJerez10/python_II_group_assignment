import streamlit as st

st.title("📈 Model Trading Signals")

st.warning("Model integration pending...")

ticker = st.selectbox("Select Ticker", ["AAPL", "MSFT"])
st.metric("Predicted Direction", "BUY")