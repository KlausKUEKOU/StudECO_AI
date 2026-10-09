import streamlit as st

st.set_page_config(
    page_title="StudECO AI",
    page_icon="assets/kk_ai.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
        .hero {
            background: linear-gradient(135deg, #0f172a 0%, #172554 55%, #1d4ed8 100%);
            padding: 2.4rem 2.2rem;
            border-radius: 20px;
            color: white;
            margin: 0.5rem 0 1.6rem 0;
            box-shadow: 0 16px 35px rgba(15, 23, 42, 0.24);
        }

        .hero h1 {
            font-size: 2.4rem;
            margin: 0;
            color: #ffffff;
        }

        .hero p {
            font-size: 1.05rem;
            margin: 0.8rem 0 0 0;
            color: #dbeafe;
            max-width: 760px;
            line-height: 1.65;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero">
        <h1>StudECO AI</h1>
        <p>
            Importez un cours ou un article scientifique : l'agent extrait le texte page par page,
            produit une fiche structurée selon votre modèle, puis vérifie sa fidélité au document.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

course_column, paper_column = st.columns(2)

with course_column:
    with st.container(border=True):
        st.subheader("📖 Synthèse de cours")
        st.write(
            "Fiche de révision : objectifs, 5 idées clés, définitions, mécanisme, "
            "formules, exemple appliqué, erreurs fréquentes et questions de révision."
        )
        st.page_link("Pages/course_summary.py", label="Résumer un cours", icon="➡️")

with paper_column:
    with st.container(border=True):
        st.subheader("🔎 Analyse d'article")
        st.write(
            "Fiche de lecture : question de recherche, contribution, données, méthode, "
            "identification, résultats qualifiés, limites et citations exactes."
        )
        st.page_link("Pages/paper_summary.py", label="Analyser un article", icon="➡️")

st.subheader("Comment ça marche")
step1, step2, step3, step4 = st.columns(4)
step1.markdown("**1. Extraction**  \nTexte lu page par page ; les pages scannées sont signalées.")
step2.markdown("**2. Lecture**  \nLes documents longs sont d'abord résumés en notes, bloc par bloc.")
step3.markdown("**3. Fiche**  \nLe modèle remplit un schéma JSON imposé, validé puis converti en Markdown.")
step4.markdown("**4. Contrôle**  \nPages citées, chiffres, citations et causalité sont vérifiés.")

st.info(
    "**Modèle IA** : réglez le fournisseur dans le panneau « 🤖 Modèle IA » de la barre latérale "
    "des pages d'analyse. Par défaut : Qwen via Groq (gratuit, clé requise) ; "
    "ou Qwen en local avec Ollama, sans clé ni envoi de vos documents."
)
