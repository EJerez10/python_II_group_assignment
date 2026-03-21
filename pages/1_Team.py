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
    width: 100%;
    height: 260px;
    object-fit: cover;
    object-position: center top;
    border-radius: 12px;
    display: block;
    margin-bottom: 0.5rem;
}

.team-name {
    font-weight: 600;
    font-size: 1.05rem;
}

.team-role {
    color: #6b7280;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("---")

team_members = [
    {
        "name": "Enzo Jerez",
        "role": "Web App Development",
        "image": "assets/enzo.png"
    },
    {
        "name": "Roberto Cummings",
        "role": "Machine Learning",
        "image": "assets/roberto.png"
    },
    {
        "name": "Jia Yi Rachel Lee",
        "role": "ETL / Data",
        "image": "assets/rachel.png"
    },
    {
        "name": "Thomas-Christian Manteco",
        "role": "Research / UX",
        "image": "assets/thomas.png"
    },
    {
        "name": "Maria-Irina Popa",
        "role": "Support / Analysis",
        "image": "assets/maria.png"
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
                <img class="team-img" src="data:image/jpeg;base64,{img_b64}" />
                <div class="team-name">{member['name']}</div>
                <div class="team-role">{member['role']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"Image not found: {member['image']}")
        st.markdown(
            f"""
            <div class="team-card">
                <div class="team-name">{member['name']}</div>
                <div class="team-role">{member['role']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Row 1
left, col1, col2, right = st.columns([1, 2, 2, 1])
with col1:
    render_member(team_members[0])
with col2:
    render_member(team_members[1])

# Row 2
left, col3, col4, right = st.columns([1, 2, 2, 1])
with col3:
    render_member(team_members[2])
with col4:
    render_member(team_members[3])

# Centered bottom member
left, center, right = st.columns([2, 1.5, 2])
with center:
    render_member(team_members[4])