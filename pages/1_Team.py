import streamlit as st
import base64
from pathlib import Path

st.title("👥 Meet the Team")
st.caption("The people behind Raviolution.")

st.markdown("""
Raviolution was built through collaboration across data, machine learning,
and application development.
""")

st.markdown("""
<style>
.team-card {
    text-align: center;
    padding: 0.8rem;
}

.team-img {
    width: 180px;
    height: 180px;
    object-fit: cover;
    object-position: center top;
    border-radius: 50%;
    display: block;
    margin: 0 auto 0.6rem auto;
    border: 3px solid rgba(255,255,255,0.15);
}

.team-name {
    font-weight: 600;
    font-size: 1.05rem;
}

.team-role {
    color: #6b7280;
    font-size: 0.9rem;
}

.team-bio {
    font-size: 0.9rem;
    color: #d1d5db;
    margin-top: 0.35rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("---")

team_members = [
    {
        "name": "Enzo Jerez",
        "role": "Web App Development",
        "image": "assets/enzo.png",
    },
    {
        "name": "Roberto Cummings",
        "role": "Machine Learning",
        "image": "assets/roberto.png",
    },
    {
        "name": "Jia Yi Rachel Lee",
        "role": "ETL / Data",
        "image": "assets/rachel.png",
    },
    {
        "name": "Thomas-Christian Manteco",
        "role": "Research / UX",
        "image": "assets/thomas.png",
    },
    {
        "name": "Maria-Irina Popa",
        "role": "Support / Analysis",
        "image": "assets/maria.png",
    },
]

def image_to_base64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return base64.b64encode(p.read_bytes()).decode()

def render_member(member):
    img_b64 = image_to_base64(member["image"])

    if img_b64:
        st.markdown(
            f"""
            <div class="team-card">
                <img class="team-img" src="data:image/png;base64,{img_b64}" />
                <div class="team-name">{member['name']}</div>
                <div class="team-role">{member['role']}</div>
                <div class="team-bio">{member['bio']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="team-card">
                <div class="team-name">{member['name']}</div>
                <div class="team-role">{member['role']}</div>
                <div class="team-bio">{member['bio']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Top row: 2 members
col1, col2 = st.columns(2)
with col1:
    render_member(team_members[0])
with col2:
    render_member(team_members[1])

# Bottom row: 3 members
col3, col4, col5 = st.columns(3)
with col3:
    render_member(team_members[2])
with col4:
    render_member(team_members[3])
with col5:
    render_member(team_members[4])

st.markdown("---")

st.subheader("Why We Built Raviolution")
st.write("""
We wanted to create a platform that combines market data, visualization, and machine learning
into one unified experience. Raviolution was designed to make stock analysis more interactive,
more intuitive, and more accessible by giving users a clean dashboard to monitor stocks,
explore trading patterns, and generate model-based recommendations.
""")