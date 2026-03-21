import streamlit as st

st.title("👥 Meet the Team")
st.caption("The people behind Raviolution.")

st.markdown("""
Raviolution was built through collaboration across data, machine learning,
and application development.
""")

st.markdown("---")

# ---- TEAM DATA ----
team_members = [
    {
        "name": "Enzo Jerez",
        "role": "Web App Development",
        "image": "assets/enzo.jpg"
    },
    {
        "name": "Roberto Cummings",
        "role": "Machine Learning",
        "image": "assets/roberto_cummings.jpeg"
    },
    {
        "name": "Jia Yi Rachel Lee",
        "role": "ETL / Data",
        "image": "assets/jiayirachel_lee.jpeg"
    },
    {
        "name": "Thomas-Christian Manteco",
        "role": "Research / UX",
        "image": "assets/thomaschristian_manteco.jpeg"
    },
    {
        "name": "Maria-Irina Popa",
        "role": "Support / Analysis",
        "image": "assets/maria-irina_popa.jpeg"
    },
]

# ---- HELPER FUNCTION ----
def render_member(member):
    st.image(member["image"], use_container_width=True)
    st.markdown(f"**{member['name']}**")
    st.caption(member["role"])

# ---- ROW 1 ----
col1, col2 = st.columns(2)

with col1:
    render_member(team_members[0])

with col2:
    render_member(team_members[1])

# ---- ROW 2 ----
col3, col4 = st.columns(2)

with col3:
    render_member(team_members[2])

with col4:
    render_member(team_members[3])

# ---- CENTERED MEMBER ----
left_spacer, center_col, right_spacer = st.columns([1, 2, 1])

with center_col:
    render_member(team_members[4])
