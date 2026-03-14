import streamlit as st

st.set_page_config(page_title="SimFin Dashboard", layout="wide")

st.title("📈 Web-Based Trading System (SimFin + ML)")
st.write("""
This app provides an interactive trading dashboard.

Use the sidebar to navigate:
- **Go Live**: explore company fundamentals and trends (stand-in data for now)
- Later: **Model Signals / Backtesting** (once the ML model is integrated)
""")

st.subheader("Development Team")
st.write("""
- **You**: Part 2 (SimFin wrapper + Streamlit app)
- **Partner**: ML model + signals
""")

st.info("Go Live currently uses hard-coded sample data until the SimFin API key + model are ready.")