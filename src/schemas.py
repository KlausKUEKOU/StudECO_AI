"""Contrats de sortie (JSON Schema) des fiches de cours et d'article."""

NOT_FOUND = "Non précisé dans le document"

EVIDENCE_TYPES = ["descriptif", "corrélationnel", "causal sous hypothèses", "théorique", "non précisé"]


def _str(description: str) -> dict:
    return {"type": "string", "description": description}


def _list(items: dict, description: str, min_items: int = 0) -> dict:
    return {"type": "array", "items": items, "description": description, "minItems": min_items}


def _obj(properties: dict, description: str = "") -> dict:
    schema = {"type": "object", "properties": properties, "required": list(properties)}
    if description:
        schema["description"] = description
    return schema


SOURCE = _str(
    "Localisation dans le document : « p. 4 », « p. 4-5 », « p. 7, section 2.1 », « tableau 3 (p. 12) ». "
    f"« {NOT_FOUND} » si introuvable."
)

COURSE_SCHEMA = _obj(
    {
        "title": _str("Titre du cours ou du chapitre, tel qu'il figure dans le document."),
        "learning_objectives": _list(
            _str("Ce que l'étudiant doit savoir expliquer ou appliquer."),
            "Objectifs pédagogiques (explicites ou déduits prudemment du contenu).",
            1,
        ),
        "key_ideas": _list(
            _obj({"idea": _str("Idée essentielle, une phrase."), "source": SOURCE}),
            "Exactement 5 idées clés, par ordre d'importance.",
            1,
        ),
        "definitions": _list(
            _obj(
                {
                    "notion": _str("Terme défini."),
                    "definition": _str("Définition fidèle au cours."),
                    "example": _str("Exemple du document, ou « (illustratif) ... » s'il est construit."),
                    "source": SOURCE,
                }
            ),
            "Notions et définitions du cours.",
        ),
        "mechanism": _list(
            _obj({"step": _str("Étape du raisonnement."), "source": SOURCE}),
            "Étapes du mécanisme ou du raisonnement central, dans l'ordre.",
        ),
        "formulas": _list(
            _obj(
                {
                    "element": _str("Nom de la formule, de l'indicateur ou de la méthode."),
                    "formula": _str("Transcription exacte (LaTeX entre $...$ si possible) ou procédure."),
                    "variables": _str("Signification de chaque variable."),
                    "interpretation": _str("Comment l'interpréter."),
                    "conditions": _str("Conditions d'application ou limites."),
                    "source": SOURCE,
                }
            ),
            "Formules, indicateurs ou méthodes.",
        ),
        "applied_example": _obj(
            {
                "origin": {"type": "string", "enum": ["tiré du document", "construit à titre illustratif"]},
                "context": _str("Contexte."),
                "reasoning": _str("Raisonnement."),
                "result": _str("Résultat."),
                "interpretation": _str("Interprétation."),
                "source": SOURCE,
            },
            "Un exemple appliqué ; privilégier un exemple du document.",
        ),
        "common_mistakes": _list(_str("Erreur fréquente ou confusion à éviter."), "Erreurs fréquentes."),
        "review_questions": _list(_str("Question de révision."), "3 à 6 questions de révision.", 1),
        "missing_information": _list(
            _str("Élément attendu mais absent ou illisible."),
            "Ce que le document ne permet pas d'établir.",
        ),
        "sources_used": _list(_str("Page ou section utilisée."), "Pages/sections mobilisées."),
    }
)

PAPER_SCHEMA = _obj(
    {
        "reference": _obj(
            {
                "authors": _str("Auteurs."),
                "year": _str("Année."),
                "title": _str("Titre."),
                "journal": _str("Revue, éditeur ou série de working papers."),
                "doi_url": _str("DOI ou URL s'ils figurent dans le document."),
                "field": _str("Domaine (ex. économie du travail, économétrie, théorie des jeux)."),
            }
        ),
        "paper_type": {
            "type": "string",
            "enum": ["empirique", "théorique", "méthodologique", "revue de littérature", "mixte"],
        },
        "research_question": _obj({"question": _str("Question de recherche précise."), "source": SOURCE}),
        "contribution": _obj(
            {
                "problem": _str("Problème traité."),
                "literature_gap": _str("Lacune dans la littérature."),
                "contribution": _str("Contribution annoncée par les auteurs."),
                "source": SOURCE,
            }
        ),
        "theoretical_framework": _obj(
            {
                "theories": _str("Théories ou modèles mobilisés."),
                "hypotheses": _list(_str("Hypothèse."), "Hypothèses principales."),
                "mechanism": _str("Mécanisme économique étudié."),
                "source": SOURCE,
            }
        ),
        "data_method": _obj(
            {
                "data": _str("Données utilisées."),
                "period_area": _str("Période et zone étudiées."),
                "unit": _str("Unité d'observation."),
                "method": _str("Méthode économétrique ou théorique."),
                "variables": _str("Variables principales (dépendante, d'intérêt, contrôles)."),
                "identification": _str("Stratégie d'identification causale."),
                "robustness": _str("Tests de robustesse."),
                "source": SOURCE,
            }
        ),
        "results": _list(
            _obj(
                {
                    "result": _str("Résultat, formulé avec la prudence requise."),
                    "magnitude": _str("Ampleur quantitative si indiquée."),
                    "significance": _str("Significativité / incertitude si indiquée."),
                    "evidence_type": {"type": "string", "enum": EVIDENCE_TYPES},
                    "source": SOURCE,
                }
            ),
            "Résultats principaux (1 à 5).",
            1,
        ),
        "interpretation": _obj(
            {
                "meaning": _str("Ce que les résultats signifient concrètement."),
                "mechanism": _str("Mécanisme plausible avancé."),
                "cannot_conclude": _str("Ce que l'article ne permet pas de conclure."),
            }
        ),
        "limitations": _obj(
            {
                "acknowledged": _list(_str("Limite reconnue."), "Limites reconnues par les auteurs."),
                "methodological": _list(
                    _str("Limite possible."), "Limites méthodologiques possibles (interprétation prudente)."
                ),
                "generalization": _str("Portée et généralisation des résultats."),
                "bias_endogeneity": _str("Risques de biais ou d'endogénéité."),
            }
        ),
        "relevance": _obj(
            {
                "usefulness": _str("Utilité pour le sujet de recherche de l'utilisateur."),
                "reusable_idea": _str("Idée ou résultat réutilisable."),
                "related_work": _str("Liens avec d'autres travaux CITÉS dans l'article."),
            }
        ),
        "key_quotes": _list(
            _obj({"quote": _str("Citation mot pour mot."), "page": _str("Page, ex. « p. 3 ».")}),
            "2 à 4 citations exactes importantes.",
        ),
        "short_summary": _str("Résumé de 100 à 150 mots, fidèle à l'article."),
        "missing_information": _list(
            _str("Élément attendu mais absent."), "Ce que le document ne permet pas d'établir."
        ),
    }
)

SCHEMAS = {"course": COURSE_SCHEMA, "paper": PAPER_SCHEMA}

# Découpage de chaque fiche en deux appels plus légers, pour les modèles à budget réduit.
SCHEMA_PARTS = {
    "course": [
        ["title", "learning_objectives", "key_ideas", "definitions", "mechanism"],
        ["formulas", "applied_example", "common_mistakes", "review_questions", "missing_information", "sources_used"],
    ],
    "paper": [
        ["reference", "paper_type", "research_question", "contribution", "theoretical_framework",
         "data_method", "short_summary"],
        ["results", "interpretation", "limitations", "relevance", "key_quotes", "missing_information"],
    ],
}


def sub_schema(schema: dict, keys: list[str]) -> dict:
    return {**schema, "properties": {key: schema["properties"][key] for key in keys}, "required": keys}
