import streamlit as st

st.set_page_config(
    page_title="À propos - StudECO AI",
    page_icon="assets/kk_ai.png",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 10% 5%, rgba(37, 99, 235, 0.10), transparent 25%),
                radial-gradient(circle at 95% 20%, rgba(14, 165, 233, 0.10), transparent 22%),
                #f8fafc;
        }

        .hero {
            background: linear-gradient(135deg, #0f172a 0%, #172554 55%, #1d4ed8 100%);
            padding: 2.6rem 2.4rem;
            border-radius: 20px;
            color: white;
            margin: 0.5rem 0 1.8rem 0;
            box-shadow: 0 16px 35px rgba(15, 23, 42, 0.24);
        }

        .hero-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.24);
            padding: 0.38rem 0.8rem;
            border-radius: 999px;
            font-size: 0.85rem;
            letter-spacing: 0.04rem;
            margin-bottom: 1rem;
        }

        .hero h1 {
            font-size: 2.5rem;
            margin: 0;
            color: #ffffff;
        }

        .hero p {
            font-size: 1.08rem;
            margin: 0.8rem 0 0 0;
            color: #dbeafe;
            max-width: 760px;
            line-height: 1.65;
        }

        .section-title {
            color: #0f172a;
            font-size: 1.45rem;
            font-weight: 700;
            margin: 1.8rem 0 0.75rem 0;
        }

        .card {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.35rem;
            min-height: 195px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 14px 26px rgba(30, 64, 175, 0.16);
            border-color: #93c5fd;
        }

        .card-icon {
            font-size: 1.8rem;
            margin-bottom: 0.7rem;
        }

        .card-title {
            color: #0f172a;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.55rem;
        }

        .card-text {
            color: #475569;
            font-size: 0.93rem;
            line-height: 1.55;
        }

        .metric-card {
            background: linear-gradient(135deg, #ffffff, #eff6ff);
            border: 1px solid #bfdbfe;
            border-radius: 14px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(30, 64, 175, 0.08);
        }

        .metric-number {
            color: #1d4ed8;
            font-size: 1.75rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .metric-label {
            color: #475569;
            font-size: 0.84rem;
        }

        .timeline {
            border-left: 3px solid #60a5fa;
            margin: 1rem 0;
            padding-left: 1.3rem;
        }

        .timeline-item {
            position: relative;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 0.95rem 1.1rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
        }

        .timeline-item::before {
            content: "";
            width: 13px;
            height: 13px;
            background: #2563eb;
            border: 3px solid #dbeafe;
            border-radius: 50%;
            position: absolute;
            left: -1.83rem;
            top: 1.05rem;
        }

        .timeline-title {
            color: #0f172a;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .timeline-text {
            color: #64748b;
            font-size: 0.91rem;
            line-height: 1.5;
        }

        .principle {
            background: #ffffff;
            border-left: 4px solid #2563eb;
            border-radius: 0 12px 12px 0;
            padding: 1rem 1.1rem;
            margin: 0.65rem 0;
            color: #334155;
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04);
        }

        .footer-box {
            background: #0f172a;
            color: #cbd5e1;
            border-radius: 14px;
            padding: 1.1rem 1.3rem;
            margin-top: 2rem;
            text-align: center;
            font-size: 0.9rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">PROJET PORTFOLIO · DOCUMENT INTELLIGENCE</div>
        <h1>StudECO AI</h1>
        <p>
            Assistant de synthèse académique structuré pour l'économie,
            l'économétrie, l'analyse de données et la recherche scientifique.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Une application pensée pour les documents académiques</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📖</div>
            <div class="card-title">Comprendre les cours</div>
            <div class="card-text">
                Transformer des chapitres, diapositives et notes en fiches de
                révision structurées : concepts, définitions, mécanismes,
                exemples et questions de révision.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">🔎</div>
            <div class="card-title">Analyser les articles</div>
            <div class="card-text">
                Identifier la question de recherche, les données, la méthode,
                les résultats, les limites et les implications d'un article
                scientifique.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📑</div>
            <div class="card-title">Structurer l'information</div>
            <div class="card-text">
                Produire des restitutions homogènes et personnalisables,
                fondées sur un modèle de fiche défini par l'utilisateur.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="section-title">Principes de conception</div>',
    unsafe_allow_html=True
)

left_column, right_column = st.columns([1.15, 1])

with left_column:
    st.markdown(
        """
        <div class="principle">
            <strong>Traçabilité.</strong> Le document original reste la source
            de référence ; les informations importantes doivent pouvoir être
            reliées à une page ou une section.
        </div>

        <div class="principle">
            <strong>Rigueur méthodologique.</strong> Une information absente
            doit être signalée, et une corrélation ne doit pas être présentée
            comme une causalité.
        </div>

        <div class="principle">
            <strong>Personnalisation.</strong> La structure de sortie doit
            s'adapter au document et au besoin : révision, lecture critique,
            recherche ou création de support pédagogique.
        </div>
        """,
        unsafe_allow_html=True
    )

with right_column:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">🎯</div>
            <div class="card-title">Objectif du projet</div>
            <div class="card-text">
                Concevoir un outil qui accélère la lecture et l'organisation
                des connaissances sans remplacer la vérification humaine,
                l'analyse critique ou la lecture du document original.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="section-title">Fonctionnalités et évolution</div>',
    unsafe_allow_html=True
)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-number">PDF</div>
            <div class="metric-label">Import de documents</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-number">Pages</div>
            <div class="metric-label">Extraction traçable</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-number">IA</div>
            <div class="metric-label">Synthèse structurée</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-number">Export</div>
            <div class="metric-label">Markdown, DOCX, PDF</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="section-title">Feuille de route</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="timeline">
        <div class="timeline-item">
            <div class="timeline-title">Version 0.1 · Extraction documentaire</div>
            <div class="timeline-text">
                Import de PDF, lecture page par page, aperçu du contenu extrait
                et signalement des documents nécessitant potentiellement une OCR.
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-title">Version 0.2 · Synthèse de cours</div>
            <div class="timeline-text">
                Génération d'une fiche de révision avec objectifs, concepts,
                définitions, exemples, formules et questions de révision.
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-title">Version 0.3 · Analyse d'articles scientifiques</div>
            <div class="timeline-text">
                Extraction structurée de la question de recherche, des données,
                de la méthode, des résultats, de la stratégie d'identification
                et des limites.
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-title">Version 1.0 · Export et bibliothèque documentaire</div>
            <div class="timeline-text">
                Export Markdown, DOCX et PDF, historique local, modèles de
                synthèse personnalisés et gestion d'une bibliothèque de documents.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Technologies mobilisées</div>',
    unsafe_allow_html=True
)

tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:
    st.info("**Python**\n\nLogique applicative et traitement des données.")

with tech2:
    st.info("**Streamlit**\n\nInterface web interactive et multipage.")

with tech3:
    st.info("**PyMuPDF**\n\nExtraction de texte et traitement de PDF.")

with tech4:
    st.info("**LLM + JSON**\n\nSynthèses contrôlées et structurées.")

st.markdown(
    """
    <div class="footer-box">
        StudECO AI · Projet portfolio en développement<br>
        Synthèse académique structurée pour l'économie, les données et la recherche
    </div>
    """,
    unsafe_allow_html=True
)