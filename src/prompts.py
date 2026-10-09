"""Prompts de l'agent de synthèse académique."""

import json

from src.schemas import NOT_FOUND

SYSTEM_PROMPT = f"""<role>
Tu es StudECO AI, un agent de synthèse académique rigoureux spécialisé en économie,
économétrie, statistique, théorie des jeux et analyse de données.
Tu résumes exclusivement à partir du document fourni. Tu ne dois jamais inventer
une donnée, une référence, une méthode, un résultat, une définition ou une conclusion
absente du document.
</role>

<rules>
- Distingue clairement : (1) les informations explicitement présentes dans le document ;
  (2) les interprétations prudentes ; (3) les informations absentes ou impossibles à établir.
- Si une information est absente, écris exactement « {NOT_FOUND} » et ajoute-la
  à la liste missing_information. Ne comble jamais un vide par une supposition.
- Pour tout chiffre, résultat, équation, définition ou affirmation centrale, indique
  la page d'origine en t'appuyant sur les balises [Page N] du document.
- Recopie les chiffres et les formules exactement comme dans le document ; explique
  ensuite chaque variable.
- Conserve les nuances : corrélation n'est pas causalité ; hypothèse n'est pas résultat ;
  significativité statistique n'est pas importance économique.
- N'ajoute aucune référence bibliographique absente du document.
- Explique les termes techniques dans un français clair, sans perdre la rigueur.
- Rédige en français, même si le document est dans une autre langue (citations
  exceptées : elles restent dans la langue d'origine).
</rules>"""

COURSE_TASK = """Produis une fiche de révision du cours ci-dessus.
- key_ideas : exactement 5 idées, par ordre d'importance.
- definitions : reprends les définitions du cours sans les simplifier abusivement.
- formulas : transcription exacte ; si le cours n'en contient pas, renvoie une liste vide.
- applied_example : privilégie un exemple du document ; sinon construis-en un simple
  et indique origin = « construit à titre illustratif ».
- review_questions : de la restitution à l'application."""

PAPER_TASK = """Produis une fiche de lecture académique de l'article ci-dessus.
- Pour chaque résultat, choisis evidence_type avec soin :
  « descriptif » (statistiques descriptives), « corrélationnel » (association sans
  stratégie d'identification), « causal sous hypothèses » (stratégie d'identification
  explicite : expérience, IV, RDD, différences-de-différences, etc.), « théorique »
  (résultat d'un modèle), « non précisé ».
- Ne formule jamais un résultat de façon causale si l'identification n'est pas décrite.
  Exemple : écrire « l'étude observe une association positive » et non « X a causé Y ».
- limitations.methodological et interpretation.cannot_conclude sont tes analyses
  critiques : reste prudent et fonde-les sur la méthode décrite.
- key_quotes : citations mot pour mot uniquement, avec leur page.
- relevance : relie l'article au sujet de recherche de l'utilisateur s'il est fourni ;
  related_work ne cite que des travaux mentionnés dans l'article."""

TASKS = {"course": COURSE_TASK, "paper": PAPER_TASK}

LEVELS = {
    "standard": "Public : étudiant de master en économie.",
    "debutant": "Public : étudiant débutant ; explique davantage les notions techniques.",
    "examen": "Public : révision d'examen ; va à l'essentiel, privilégie ce qui est à retenir.",
    "recherche": "Public : chercheur ; insiste sur la méthode, l'identification et les limites.",
}

NOTES_PROMPT = """Voici un extrait (pages {first} à {last}) d'un document plus long.
Extrais sous forme de notes fidèles toutes les informations utiles pour une fiche de {kind_label} :
{focus}
Règles :
- Une note par ligne, au format « - [p. N] contenu » ; au plus {max_lines} notes, les plus importantes.
- Recopie mot pour mot les chiffres, formules, définitions et phrases citables (entre guillemets).
- N'invente rien, n'interprète pas : ce sont des notes de lecture brutes.

<extrait>
{text}
</extrait>"""

NOTES_FOCUS = {
    "course": "titres, objectifs, définitions, mécanismes, formules, exemples, mises en garde.",
    "paper": (
        "référence, question de recherche, contribution, cadre théorique, données, méthode, "
        "stratégie d'identification, résultats chiffrés et significativité, robustesse, limites, conclusion."
    ),
}

CONDENSE_PROMPT = """Voici des notes de lecture d'un document, rédigées bloc par bloc.
Fusionne-les et condense-les en au plus {max_chars} caractères pour une fiche de {kind_label} :
- conserve les références [p. N], les chiffres, les formules et les citations exactes ;
- supprime les redondances et les détails secondaires ;
- n'ajoute rien qui ne figure pas dans les notes.

<notes>
{text}
</notes>"""

REPAIR_PROMPT = """Ta réponse n'est pas conforme au schéma demandé :
{problem}
Renvoie uniquement l'objet JSON complet et corrigé, sans texte autour."""


def _kind_label(kind: str) -> str:
    return "cours" if kind == "course" else "lecture d'article"


def build_notes_messages(kind: str, text: str, first: int, last: int, max_lines: int = 40) -> list[dict]:
    prompt = NOTES_PROMPT.format(
        first=first,
        last=last,
        kind_label=_kind_label(kind),
        focus=NOTES_FOCUS[kind],
        max_lines=max_lines,
        text=text,
    )
    return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]


def build_condense_messages(kind: str, text: str, max_chars: int) -> list[dict]:
    prompt = CONDENSE_PROMPT.format(max_chars=max_chars, kind_label=_kind_label(kind), text=text)
    return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]


def build_summary_messages(
    kind: str,
    source_text: str,
    schema: dict,
    from_notes: bool = False,
    level: str = "standard",
    research_focus: str = "",
) -> list[dict]:
    if from_notes:
        intro = (
            "Le document était trop long pour être lu d'un bloc : voici des notes de lecture "
            "fidèles, extraites page par page. Les références [p. N] renvoient aux pages du document."
        )
        tag = "notes_de_lecture"
    else:
        intro = "Voici le document, balisé par page."
        tag = "document"

    context = LEVELS.get(level, LEVELS["standard"])
    if research_focus.strip():
        context += f"\nSujet de recherche de l'utilisateur : {research_focus.strip()}"

    user = f"""{intro}

<{tag}>
{source_text}
</{tag}>

<task>
{TASKS[kind]}
</task>

<user_context>
{context}
</user_context>

<output_format>
Réponds uniquement avec un objet JSON valide conforme à ce JSON Schema
(tous ses champs sont obligatoires ; ne remplis que ceux-là ; aucun texte hors JSON) :
{json.dumps(schema, ensure_ascii=False)}
</output_format>"""
    return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user}]
