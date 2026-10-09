"""Client minimal pour les API compatibles OpenAI, avec sortie JSON validée par schéma."""

import json
import re
import time
from dataclasses import dataclass, field

import requests
from jsonschema import Draft202012Validator

from src.prompts import REPAIR_PROMPT


class LLMError(Exception):
    """Erreur lisible par l'utilisateur lors d'un appel au modèle."""


class _BadRequest(LLMError):
    pass


@dataclass
class LLMSettings:
    base_url: str
    model: str
    api_key: str = ""
    temperature: float = 0.2
    extra_body: dict = field(default_factory=dict)
    timeout: int = 600


_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def _clean(content: str) -> str:
    """Retire le raisonnement interne (<think>) que certains modèles Qwen renvoient."""
    content = _THINK_RE.sub("", content)
    # Bloc <think> non refermé (réponse tronquée) : on garde ce qui suit.
    if "</think>" in content:
        content = content.split("</think>", 1)[1]
    return content.strip()


def _post(settings: LLMSettings, payload: dict) -> str:
    url = settings.base_url.rstrip("/") + "/chat/completions"
    headers = {"Content-Type": "application/json"}
    if settings.api_key:
        headers["Authorization"] = f"Bearer {settings.api_key}"

    for attempt in range(6):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=settings.timeout)
        except requests.ConnectionError as exc:
            raise LLMError(
                f"Impossible de joindre {settings.base_url}. "
                "Vérifiez l'adresse du serveur (Ollama est-il lancé ?) et votre connexion."
            ) from exc
        except requests.Timeout as exc:
            raise LLMError(f"Le modèle n'a pas répondu en {settings.timeout} s.") from exc

        retryable = response.status_code == 429 or response.status_code >= 500
        if retryable and attempt < 5:
            delay = response.headers.get("retry-after")
            time.sleep(min(float(delay) if delay else 5 * 2**attempt, 60))
            continue
        if response.status_code == 400:
            raise _BadRequest(f"Requête refusée (400) : {response.text[:500]}")
        if response.status_code in (401, 403):
            raise LLMError("Clé API absente ou invalide pour ce fournisseur.")
        if response.status_code == 413:
            raise LLMError(
                "Passage trop long pour ce fournisseur (413). "
                "Réduisez la taille des blocs dans les paramètres."
            )
        if not response.ok:
            raise LLMError(f"Erreur {response.status_code} : {response.text[:500]}")

        try:
            choice = response.json()["choices"][0]
        except (ValueError, KeyError, IndexError) as exc:
            raise LLMError(f"Réponse inattendue du fournisseur : {response.text[:500]}") from exc
        content = _clean(choice["message"].get("content") or "")
        if not content:
            raise LLMError("Le modèle a renvoyé une réponse vide.")
        if choice.get("finish_reason") == "length":
            content += "\n[RÉPONSE TRONQUÉE]"
        return content

    raise LLMError("Limite de débit atteinte : réessayez dans quelques instants.")


def chat(settings: LLMSettings, messages: list[dict], json_mode: bool = False) -> str:
    payload = {
        "model": settings.model,
        "messages": messages,
        "temperature": settings.temperature,
        **settings.extra_body,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    try:
        return _post(settings, payload)
    except _BadRequest:
        # Certains modèles refusent response_format ou les options spécifiques :
        # on réessaie avec une requête minimale, le schéma restant imposé par le prompt.
        minimal = {k: payload[k] for k in ("model", "messages", "temperature")}
        if minimal == payload:
            raise
        return _post(settings, minimal)


def parse_json(text: str) -> dict:
    text = _FENCE_RE.sub("", text.strip())
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("aucun objet JSON trouvé dans la réponse")
    try:
        data = json.loads(text[start : end + 1])
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON mal formé ({exc.msg}, position {exc.pos})") from exc
    if not isinstance(data, dict):
        raise ValueError("la racine du JSON doit être un objet")
    return data


def generate_structured(
    settings: LLMSettings, messages: list[dict], schema: dict, max_attempts: int = 3
) -> dict:
    """Appelle le modèle jusqu'à obtenir un JSON conforme au schéma (avec auto-correction)."""
    validator = Draft202012Validator(schema)
    messages = list(messages)
    problem = ""

    for _ in range(max_attempts):
        raw = chat(settings, messages, json_mode=True)
        try:
            data = parse_json(raw)
        except ValueError as exc:
            problem = f"JSON invalide : {exc}"
        else:
            errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
            if not errors:
                return data
            problem = "\n".join(
                f"- {'/'.join(map(str, e.path)) or 'racine'} : {e.message}" for e in errors[:15]
            )
        messages += [
            {"role": "assistant", "content": raw[:20_000]},
            {"role": "user", "content": REPAIR_PROMPT.format(problem=problem)},
        ]

    raise LLMError(f"Sortie non conforme au schéma après {max_attempts} tentatives :\n{problem}")
