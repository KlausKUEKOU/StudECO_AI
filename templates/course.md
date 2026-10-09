# {{ d.title or "Fiche de cours" }}

> Fiche générée par StudECO AI à partir de « {{ document_name }} » le {{ generated_at }}.
> Synthèse automatique : à vérifier avec le document original.

## 1. Objectif pédagogique
{% for objective in d.learning_objectives %}
- {{ objective }}
{% else %}
- {{ NOT_FOUND }}
{% endfor %}

## 2. Résumé en 5 idées
{% for item in d.key_ideas %}
{{ loop.index }}. {{ item.idea }} *({{ item.source }})*
{% endfor %}

## 3. Notions et définitions
{% if d.definitions %}
| Notion | Définition fidèle au cours | Exemple | Source |
|---|---|---|---|
{% for item in d.definitions %}
| **{{ item.notion|cell }}** | {{ item.definition|cell }} | {{ item.example|cell }} | {{ item.source|cell }} |
{% endfor %}
{% else %}
Aucune définition explicite dans le document.
{% endif %}

## 4. Mécanisme à comprendre
{% for item in d.mechanism %}
{{ loop.index }}. {{ item.step }} *({{ item.source }})*
{% else %}
{{ NOT_FOUND }}.
{% endfor %}

## 5. Formules, indicateurs ou méthodes
{% for item in d.formulas %}
### {{ item.element }}
{{ item.formula }}

- **Variables :** {{ item.variables }}
- **Interprétation :** {{ item.interpretation }}
- **Conditions / limites :** {{ item.conditions }}
- **Source :** {{ item.source }}

{% else %}
Aucune formule ni méthode formalisée dans le document.
{% endfor %}

## 6. Exemple appliqué{% if d.applied_example.origin %} ({{ d.applied_example.origin }}){% endif %}

- **Contexte :** {{ d.applied_example.context }}
- **Raisonnement :** {{ d.applied_example.reasoning }}
- **Résultat :** {{ d.applied_example.result }}
- **Interprétation :** {{ d.applied_example.interpretation }}
- **Source :** {{ d.applied_example.source }}

## 7. Erreurs fréquentes
{% for item in d.common_mistakes %}
- {{ item }}
{% else %}
- Aucune signalée.
{% endfor %}

## 8. Questions de révision
{% for item in d.review_questions %}
{{ loop.index }}. {{ item }}
{% endfor %}

## 9. Sources dans le document
{% for item in d.sources_used %}
- {{ item }}
{% else %}
- {{ NOT_FOUND }}
{% endfor %}
{% if d.missing_information %}

## Informations absentes ou incertaines
{% for item in d.missing_information %}
- {{ item }}
{% endfor %}
{% endif %}
