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
    padding: 0.5rem 0.5rem 1rem 0.5rem;
}

.team-img {
    width: 100%;
    height: 320px;
    object-fit: cover;
    border-radius: 14px;
    display: block;
    margin: 0 auto 0.75rem auto;
    box-shadow: 0 4px 14px rgba(0,0,0,0.12);
}

.team-name {
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 0.2rem;
}

.team-role {
    color: #6b7280;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("---")

team_members = [
    {
        "name": "Enzo Jerez",
        "role": "Web App Development",
        "image": "assets/enzo_jerez.jpeg"
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
        "image": "assets/thomaschristian_matenco.jpeg"
    },
    {
        "name": "Maria-Irina Popa",
        "role": "Support / Analysis",
        "image": "assets/maria-irina_popa.jpeg"
    },
]

def image_to_base64(path: str) -> str:
    img_path = Path(path)
    if not img_path.exists():
        return ""
    return base64.b64encode(img_path.read_bytes()).decode()

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

col1, col2 = st.columns(2)
with col1:
    render_member(team_members[0])
with col2:
    render_member(team_members[1])

col3, col4 = st.columns(2)
with col3:
    render_member(team_members[2])
with col4:
    render_member(team_members[3])

left_spacer, center_col, right_spacer = st.columns([1, 2, 1])
with center_col:
    render_member(team_members[4])