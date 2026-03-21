import streamlit as st

st.title("👥 Meet the Team")

st.markdown("""
This project was developed as part of our Python II group assignment.

Our goal was to build a complete web-based trading system that combines:
- financial market data from SimFin
- interactive dashboards in Streamlit
- a machine learning model for stock recommendations
""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Enzo Jerez")
    st.write("""
**Role:** Web App Development, SimFin API Integration, UI/UX Design

Contributions:
- built the Streamlit multi-page app
- integrated the SimFin API wrapper
- developed the stock overview and watchlist pages
- connected the app to deployed secrets for production
""")

with col2:
    st.subheader("Roberto Cummings")
    st.write("""
**Role:** Machine Learning Model Development

Contributions:
- trained the Gradient Boosting model
- prepared the ETL pipeline
- handed off model artifacts and feature engineering logic
- supported recommendation system integration
""")

st.markdown("---")

st.subheader("Why We Built Raviolution")
st.write("""
We wanted to create a platform that makes stock monitoring and recommendation generation more interactive,
more visual, and more accessible. By combining market data and machine learning in one application,
we aimed to simulate a simplified intelligent trading dashboard.
""")