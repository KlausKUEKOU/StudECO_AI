"""Composants Streamlit partagés par les pages de synthèse."""

import hashlib
import json
import os
from pathlib import Path

import streamlit as st

from src.config import DEFAULT_PROVIDER, PROVIDERS
from src.llm import LLMError, LLMSettings
from src.pdf_extractor import ExtractedDocument, extract_pdf, guess_document_type
from src.quality_check import run_checks
from src.render import render_markdown
from src.summarizer import summarize

LEVEL_LABELS = {
    "standard": "Standard (master)",
    "debutant": "Étudiant débutant",
    "examen": "Révision d'examen",
    "recherche": "Lecture de recherche",
}

_FINDING_DISPLAY = {"error": st.error, "warning": st.warning, "info": st.info}


@st.cache_data(show_spinner="Extraction du texte…")
def _extract(data: bytes, filename: str) -> ExtractedDocument:
    return extract_pdf(data, filename)


def model_settings_sidebar() -> tuple[LLMSettings | None, int]:
    """Paramètres du modèle dans la barre latérale ; None si la configuration est incomplète."""
    with st.sidebar.expander("🤖 Modèle IA", expanded=False):
        keys = list(PROVIDERS)
        default = os.getenv("STUDECO_PROVIDER", DEFAULT_PROVIDER)
        provider_key = st.selectbox(
            "Fournisseur",
            keys,
            index=keys.index(default) if default in keys else 0,
            format_func=lambda key: PROVIDERS[key].label,
            key="provider",
        )
        preset = PROVIDERS[provider_key]
        st.caption(preset.help)

        base_url = st.text_input("Adresse de l'API", preset.base_url, key=f"base_url_{provider_key}")
        default_model = preset.default_model
        if provider_key == default:
            default_model = os.getenv("STUDECO_MODEL") or default_model
        model = st.text_input("Modèle", default_model, key=f"model_{provider_key}")
        api_key = ""
        if preset.api_key_env:
            api_key = st.text_input(
                f"Clé API ({preset.api_key_env})",
                os.getenv(preset.api_key_env, ""),
                type="password",
                key=f"api_key_{provider_key}",
            )
        max_chars = st.number_input(
            "Taille max. d'un bloc (caractères)",
            min_value=4_000,
            max_value=400_000,
            value=preset.max_chars,
            step=2_000,
            key=f"max_chars_{provider_key}",
            help="Au-delà, le document est lu par blocs de pages puis synthétisé. "
            "Réduisez cette valeur pour les petits modèles locaux ou les offres gratuites limitées.",
        )

    if preset.api_key_env and not api_key and provider_key != "custom":
        st.sidebar.warning(f"Renseignez la clé {preset.api_key_env} (fichier .env ou panneau « Modèle IA »).")
        return None, int(max_chars)
    if not base_url or not model:
        return None, int(max_chars)

    settings = LLMSettings(
        base_url=base_url.strip(),
        model=model.strip(),
        api_key=api_key.strip(),
        extra_body=preset.extra_body,
    )
    return settings, int(max_chars)


def _show_document_overview(document: ExtractedDocument, kind: str) -> None:
    detected = guess_document_type(document)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pages", document.page_count)
    col2.metric("Mots extraits", f"{document.word_count:,}".replace(",", " "))
    col3.metric("Pages sans texte", len(document.ocr_pages))
    col4.metric("Type estimé", detected)

    if document.is_probably_scanned:
        st.warning(
            "La majorité des pages ne contient pas de texte : le PDF est probablement scanné. "
            "Appliquez une OCR avant l'analyse pour un résultat fiable."
        )
    elif document.ocr_pages:
        st.info(f"Pages sans texte extractible (non lues) : {', '.join(map(str, document.ocr_pages))}")

    expected = "cours" if kind == "course" else "article"
    if detected not in (expected, "inconnu"):
        other = "Analyse d'article" if kind == "course" else "Synthèse de cours"
        st.info(f"Ce document ressemble plutôt à un·e **{detected}**. La page « {other} » sera peut-être plus adaptée.")

    with st.expander("Aperçu du texte extrait"):
        page_number = st.number_input("Page", 1, max(document.page_count, 1), 1, key=f"preview_{kind}")
        page = document.pages[int(page_number) - 1]
        st.text(page.text or "(aucun texte extractible sur cette page)")


def _show_result(result: dict, kind: str) -> None:
    findings = result["findings"]
    errors = sum(f.level == "error" for f in findings)
    warnings = sum(f.level == "warning" for f in findings)
    quality_label = f"Contrôle qualité ({errors} ❌ · {warnings} ⚠️)" if errors or warnings else "Contrôle qualité ✅"

    tabs = st.tabs(["📄 Fiche", quality_label, "🧾 JSON"] + (["📝 Notes intermédiaires"] if result["notes"] else []))

    with tabs[0]:
        st.markdown(result["markdown"])
    with tabs[1]:
        st.caption(
            "Vérifications automatiques fondées sur le texte extrait. "
            "Elles ne remplacent pas une relecture du document original."
        )
        for finding in findings:
            _FINDING_DISPLAY[finding.level](finding.message)
    with tabs[2]:
        st.json(result["data"])
    if result["notes"]:
        with tabs[3]:
            st.caption("Document long : notes de lecture produites bloc par bloc avant la synthèse.")
            st.markdown("\n\n".join(result["notes"]))

    stem = Path(result["filename"]).stem
    prefix = "fiche_cours" if kind == "course" else "fiche_article"
    col1, col2 = st.columns(2)
    col1.download_button(
        "⬇️ Télécharger en Markdown",
        result["markdown"],
        file_name=f"{prefix}_{stem}.md",
        mime="text/markdown",
        width="stretch",
    )
    col2.download_button(
        "⬇️ Télécharger en JSON",
        json.dumps(result["data"], ensure_ascii=False, indent=2),
        file_name=f"{prefix}_{stem}.json",
        mime="application/json",
        width="stretch",
    )


def render_summary_page(kind: str) -> None:
    settings, max_chars = model_settings_sidebar()
    state_key = f"result_{kind}"

    uploaded = st.file_uploader("Déposez un PDF", type=["pdf"], key=f"upload_{kind}")
    if uploaded is None:
        st.info("Commencez par importer un document PDF (texte ou scan déjà OCRisé).")
        return

    data = uploaded.getvalue()
    file_hash = hashlib.sha1(data).hexdigest()
    try:
        document = _extract(data, uploaded.name)
    except ValueError as exc:
        st.error(str(exc))
        return

    _show_document_overview(document, kind)

    col1, col2 = st.columns([1, 2])
    level = col1.selectbox("Niveau de restitution", list(LEVEL_LABELS), format_func=LEVEL_LABELS.get, key=f"level_{kind}")
    research_focus = ""
    if kind == "paper":
        research_focus = col2.text_input(
            "Votre sujet de recherche (optionnel)",
            placeholder="ex. effets des infrastructures de transport sur l'emploi local",
            help="Sert à remplir la rubrique « Apport pour mes recherches ».",
        )

    if st.button("✨ Générer la fiche", type="primary", disabled=settings is None, width="stretch"):
        with st.status("Analyse en cours…", expanded=True) as status:
            progress_bar = st.progress(0.0)

            def on_progress(fraction: float, message: str) -> None:
                progress_bar.progress(min(fraction, 1.0), text=message)

            try:
                summary = summarize(
                    document, kind, settings,
                    max_chars=max_chars, level=level, research_focus=research_focus, progress=on_progress,
                )
            except (LLMError, ValueError) as exc:
                status.update(label="Échec de la génération", state="error")
                st.error(str(exc))
                return

            st.session_state[state_key] = {
                "file_hash": file_hash,
                "filename": uploaded.name,
                "data": summary.data,
                "notes": summary.notes,
                "markdown": render_markdown(kind, summary.data, uploaded.name),
                "findings": run_checks(kind, summary.data, document),
            }
            status.update(label="Fiche générée", state="complete", expanded=False)

    result = st.session_state.get(state_key)
    if result and result["file_hash"] == file_hash:
        st.divider()
        _show_result(result, kind)
