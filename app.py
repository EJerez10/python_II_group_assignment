import streamlit as st

st.set_page_config(page_title="Raviolution", page_icon="📈", layout="wide")

home = st.Page("pages/home.py", title="Home", icon="🏠")
team = st.Page("pages/1_👥_Team.py", title="Team", icon="👥")
watchlist = st.Page("pages/2_👀_Watchlist.py", title="Watchlist", icon="👀")
overview = st.Page("pages/3_📊_Overview.py", title="Stock Overview", icon="📊")
recommendations = st.Page("pages/4_🤖_Recommendations.py", title="Recommendations", icon="🤖")

pg = st.navigation([home, team, watchlist, overview, recommendations])
pg.run()