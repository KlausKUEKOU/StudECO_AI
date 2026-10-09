"""Configuration : lecture du fichier .env et préréglages des fournisseurs IA."""

import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def load_env(path: Path = ROOT_DIR / ".env") -> None:
    """Charge un fichier .env simple (CLE=valeur) sans écraser l'environnement existant."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass
class ProviderPreset:
    label: str
    base_url: str
    default_model: str
    api_key_env: str | None
    help: str
    extra_body: dict = field(default_factory=dict)
    # Taille d'un bloc de lecture adaptée aux limites du fournisseur.
    max_chars: int = 30_000


# Tous ces fournisseurs exposent une API compatible OpenAI (/chat/completions).
PROVIDERS: dict[str, ProviderPreset] = {
    "groq": ProviderPreset(
        label="Groq (gratuit avec clé)",
        base_url="https://api.groq.com/openai/v1",
        default_model="qwen/qwen3.8-27b",
        api_key_env="GROQ_API_KEY",
        help="Offre gratuite limitée à 8 000 tokens/min : les longs articles sont lus par petits "
        "blocs, avec des pauses (≈ 10 min pour 40 pages). Clé sur https://console.groq.com/keys",
        extra_body={"reasoning_format": "hidden"},
        max_chars=10_000,
    ),
    "ollama": ProviderPreset(
        label="Ollama (local, 100 % gratuit)",
        base_url="http://localhost:11434/v1",
        default_model="qwen3:8b",
        api_key_env=None,
        help="Installez Ollama puis `ollama pull qwen3:8b`. Les documents ne quittent pas votre machine.",
        max_chars=8_000,
    ),
    "openrouter": ProviderPreset(
        label="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        default_model="qwen/qwen3.7-flash",
        api_key_env="OPENROUTER_API_KEY",
        help="Qwen y est payant mais très bon marché ; les modèles « :free » sont gratuits.",
    ),
    "dashscope": ProviderPreset(
        label="Alibaba Model Studio (Qwen officiel)",
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        default_model="qwen-plus",
        api_key_env="DASHSCOPE_API_KEY",
        help="Quota gratuit à l'inscription. Clé sur https://modelstudio.console.alibabacloud.com",
    ),
    "custom": ProviderPreset(
        label="Personnalisé (compatible OpenAI)",
        base_url=os.getenv("STUDECO_BASE_URL", "http://localhost:8000/v1"),
        default_model="qwen3",
        api_key_env="STUDECO_API_KEY",
        help="Tout serveur compatible OpenAI : vLLM, LM Studio, llama.cpp, etc.",
    ),
}

DEFAULT_PROVIDER = "groq"

# En dessous de cette taille de bloc, on considère le budget du modèle comme réduit :
# la fiche est alors générée en deux parties plus légères au lieu d'un seul appel.
SMALL_BUDGET_CHARS = 20_000

load_env()
