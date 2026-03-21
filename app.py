import streamlit as st

st.set_page_config(page_title="Raviolution", page_icon="📈", layout="wide")

home = st.Page("pages/0_Home.py", title="Home", icon="🏠")
team = st.Page("pages/1_Team.py", title="Team", icon="👥")
watchlist = st.Page("pages/2_Watchlist.py", title="Watchlist", icon="👀")
overview = st.Page("pages/3_Overview.py", title="Stock Overview", icon="📊")
recommendations = st.Page("pages/4_Recommendations.py", title="Recommendations", icon="🤖")

pg = st.navigation([home, team, watchlist, overview, recommendations])
pg.run()