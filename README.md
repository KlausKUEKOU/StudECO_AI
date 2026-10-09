## StudECO_AI

Cet agent a pour but de faire un résumé des cours et articles économiques, selon un cannevas de présentations des articles Job market papers et la stucture du cours proposé (en présentant la question de recherche / cours, la contribution, les données, la méthode d’identification / technique à retenir, les principaux résultats et la conclusion).

### Fonctionnement

1. **Extraction** (`src/pdf_extractor.py`) : texte lu page par page avec PyMuPDF ; les pages sans texte (scans) sont signalées.
2. **Lecture** (`src/summarizer.py`) : si le document dépasse la taille d'un bloc, il est d'abord résumé en notes fidèles, bloc par bloc, avec références de pages.
3. **Fiche structurée** (`src/schemas.py`, `src/prompts.py`, `src/llm.py`) : le modèle remplit un JSON Schema imposé ; la réponse est validée et corrigée automatiquement si besoin.
4. **Rendu** (`templates/course.md`, `templates/paper.md`) : modèles Jinja2 modifiables pour adapter la mise en forme des fiches.
5. **Contrôle qualité** (`src/quality_check.py`) : pages citées existantes, chiffres présents dans le document, citations retrouvées mot pour mot, aucun résultat présenté comme causal sans stratégie d'identification.

### Modèle IA (Qwen, gratuit)

L'application parle à toute API compatible OpenAI. Préréglages disponibles :

| Fournisseur | Coût | Modèle par défaut |
|---|---|---|
| Groq | gratuit avec clé (débit limité) | `qwen/qwen3.8-27b` |
| Ollama | gratuit, local, sans clé | `qwen3:8b` |
| OpenRouter | Qwen très bon marché | `qwen/qwen3.7-flash` |
| Alibaba Model Studio | quota gratuit à l'inscription | `qwen-plus` |

### Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # puis renseignez GROQ_API_KEY (ou choisissez ollama)
streamlit run app.py
```

Avec Ollama : installez-le, lancez `ollama pull qwen3:8b`, puis choisissez « Ollama » dans le panneau « 🤖 Modèle IA ».
Les petits modèles locaux ont un contexte réduit : baissez la « taille max. d'un bloc » (ex. 8 000) ou augmentez `OLLAMA_CONTEXT_LENGTH`.
