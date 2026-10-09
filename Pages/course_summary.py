import streamlit as st

from src.ui import render_summary_page

st.set_page_config(
    page_title="StudECO AI",
    page_icon="assets/kk_ai.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📖 Synthèse de cours")
st.caption(
    "Transforme un chapitre, des diapositives ou des notes en fiche de révision : "
    "objectifs, 5 idées clés, définitions, mécanisme, formules, exemple, erreurs fréquentes "
    "et questions de révision - chaque élément relié à sa page d'origine."
)

render_summary_page("course")
