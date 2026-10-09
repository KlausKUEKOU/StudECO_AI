"""Conversion des fiches JSON en Markdown à partir des modèles du dossier templates/."""

from datetime import datetime

from jinja2 import ChainableUndefined, Environment, FileSystemLoader

from src.config import ROOT_DIR
from src.schemas import NOT_FOUND


def _cell(value) -> str:
    """Rend une valeur sûre pour une cellule de tableau Markdown."""
    text = str(value or "").strip() or "-"
    return text.replace("|", "\\|").replace("\n", " ")


_env = Environment(
    loader=FileSystemLoader(ROOT_DIR / "templates"),
    undefined=ChainableUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)
_env.filters["cell"] = _cell
_env.globals["NOT_FOUND"] = NOT_FOUND


def render_markdown(kind: str, data: dict, document_name: str) -> str:
    template = _env.get_template(f"{kind}.md")
    return template.render(
        d=data,
        document_name=document_name,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
