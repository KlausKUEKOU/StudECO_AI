# Fiche de lecture académique

> Fiche générée par StudECO AI à partir de « {{ document_name }} » le {{ generated_at }}.
> Synthèse automatique : à vérifier avec le document original (abstract, méthode, tableaux, annexes).

## Référence
- **Auteurs :** {{ d.reference.authors }}
- **Année :** {{ d.reference.year }}
- **Titre :** {{ d.reference.title }}
- **Revue / éditeur :** {{ d.reference.journal }}
- **DOI ou URL :** {{ d.reference.doi_url }}
- **Domaine :** {{ d.reference.field }}
- **Type d'article :** {{ d.paper_type }}

## Résumé ultra-court
{{ d.short_summary }}

## 1. Question de recherche
{{ d.research_question.question }} *({{ d.research_question.source }})*

## 2. Problématique et contribution
- **Problème traité :** {{ d.contribution.problem }}
- **Lacune dans la littérature :** {{ d.contribution.literature_gap }}
- **Contribution annoncée :** {{ d.contribution.contribution }}
- **Source :** {{ d.contribution.source }}

## 3. Cadre théorique
- **Théories ou modèles mobilisés :** {{ d.theoretical_framework.theories }}
- **Mécanisme économique étudié :** {{ d.theoretical_framework.mechanism }}
- **Hypothèses principales :**
{% for item in d.theoretical_framework.hypotheses %}
  - {{ item }}
{% else %}
  - {{ NOT_FOUND }}
{% endfor %}
- **Source :** {{ d.theoretical_framework.source }}

## 4. Données et méthode
| Élément | Description |
|---|---|
| Données | {{ d.data_method.data|cell }} |
| Période / zone étudiée | {{ d.data_method.period_area|cell }} |
| Unité d'observation | {{ d.data_method.unit|cell }} |
| Méthode économétrique ou théorique | {{ d.data_method.method|cell }} |
| Variables principales | {{ d.data_method.variables|cell }} |
| Identification causale | {{ d.data_method.identification|cell }} |
| Tests de robustesse | {{ d.data_method.robustness|cell }} |
| Source | {{ d.data_method.source|cell }} |

## 5. Résultats principaux
{% for item in d.results %}
**Résultat {{ loop.index }}** - `{{ item.evidence_type }}` *({{ item.source }})*
- {{ item.result }}
- **Ampleur :** {{ item.magnitude }}
- **Significativité / incertitude :** {{ item.significance }}

{% endfor %}
## 6. Interprétation économique
- **Ce que les résultats signifient :** {{ d.interpretation.meaning }}
- **Mécanisme plausible :** {{ d.interpretation.mechanism }}
- **Ce que l'article ne permet pas de conclure :** {{ d.interpretation.cannot_conclude }}

## 7. Limites et discussion critique
- **Limites reconnues par les auteurs :**
{% for item in d.limitations.acknowledged %}
  - {{ item }}
{% else %}
  - Aucune limite explicitement reconnue.
{% endfor %}
- **Limites méthodologiques possibles** *(analyse de l'agent)* **:**
{% for item in d.limitations.methodological %}
  - {{ item }}
{% else %}
  - Aucune identifiée.
{% endfor %}
- **Généralisation des résultats :** {{ d.limitations.generalization }}
- **Risque de biais ou d'endogénéité :** {{ d.limitations.bias_endogeneity }}

## 8. Apport pour mes recherches
- **Utilité :** {{ d.relevance.usefulness }}
- **Idée réutilisable :** {{ d.relevance.reusable_idea }}
- **Liens avec d'autres travaux :** {{ d.relevance.related_work }}

## 9. Citations importantes
{% for item in d.key_quotes %}
> « {{ item.quote }} » ({{ item.page }})

{% else %}
Aucune citation extraite.
{% endfor %}
{% if d.missing_information %}

## Informations absentes ou incertaines
{% for item in d.missing_information %}
- {{ item }}
{% endfor %}
{% endif %}
