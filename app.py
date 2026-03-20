import streamlit as st

st.set_page_config(page_title="SimFin Dashboard", layout="wide")

st.title("📈 AI Trading Dashboard")

st.markdown("""
Welcome to our web-based trading system built with **SimFin**, **Streamlit**, and a **machine learning model**.

This platform allows users to:
- explore historical stock market data
- review company financial information
- generate model-based trading signals
""")

st.subheader("Pages")
st.markdown("""
- **Go Live** → explore historical market data and company performance  
- **Model Signals** → generate machine learning trading recommendations  
""")

st.subheader("Team")
st.write("Enzo Jerez")
st.write("Roberto Cummings")
st.write("Jia Yi Rachel Lee")
st.write("Thomas Christan Matenco")
st.write("Maria-Irina Popa")