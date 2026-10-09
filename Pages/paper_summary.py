import streamlit as st

from src.ui import render_summary_page

st.set_page_config(
    page_title="StudECO AI",
    page_icon="assets/kk_ai.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔎 Analyse d'article")
st.caption(
    "Fiche de lecture académique : question de recherche, contribution, données, méthode, "
    "stratégie d'identification, résultats (qualifiés : descriptif, corrélationnel, causal "
    "sous hypothèses ou théorique), limites et citations exactes."
)

render_summary_page("paper")
