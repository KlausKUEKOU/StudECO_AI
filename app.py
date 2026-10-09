import streamlit as st

st.set_page_config(
    page_title="StudECO AI",
    page_icon="assets/kk_ai.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.logo(
    "assets/kk_ai.png",
    icon_image="assets/kk_ai.png"
)

home_page = st.Page(
    "Pages/home.py",
    title="Accueil",
    icon="🏠",
    default=True
)

course_page = st.Page(
    "Pages/course_summary.py",
    title="Synthèse de cours",
    icon="📖"
)

paper_page = st.Page(
    "Pages/paper_summary.py",
    title="Analyse d'article",
    icon="🔎"
)

about_page = st.Page(
    "Pages/about.py",
    title="À propos",
    icon="⚙️"
)

navigation = st.navigation(
    {
        "StudECO AI": [
            home_page,
            course_page,
            paper_page
        ],
        "Projet": [
            about_page
        ]
    }
)

st.sidebar.divider()
st.sidebar.caption("StudECO AI - Prototype portfolio")
st.sidebar.caption("Provided - BY - Klaus KUEKOU")
st.sidebar.caption("Version 0.1.0")

navigation.run()



