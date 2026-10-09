"""Orchestration : document extrait -> (notes par blocs) -> fiche JSON structurée."""

from collections.abc import Callable
from dataclasses import dataclass, field

from src.config import SMALL_BUDGET_CHARS
from src.llm import LLMSettings, chat, generate_structured
from src.pdf_extractor import ExtractedDocument, chunk_pages, format_pages
from src.prompts import build_condense_messages, build_notes_messages, build_summary_messages
from src.schemas import SCHEMA_PARTS, SCHEMAS, sub_schema

ProgressCallback = Callable[[float, str], None]

MAX_CONDENSE_ROUNDS = 3


@dataclass
class SummaryResult:
    data: dict
    mode: str  # "direct" ou "notes"
    notes: list[str] = field(default_factory=list)


def _group_by_size(texts: list[str], max_chars: int) -> list[list[str]]:
    groups: list[list[str]] = []
    size = 0
    for text in texts:
        if groups and size + len(text) <= max_chars:
            groups[-1].append(text)
            size += len(text)
        else:
            groups.append([text])
            size = len(text)
    return groups


def summarize(
    document: ExtractedDocument,
    kind: str,
    settings: LLMSettings,
    *,
    max_chars: int,
    level: str = "standard",
    research_focus: str = "",
    progress: ProgressCallback | None = None,
) -> SummaryResult:
    def report(fraction: float, message: str) -> None:
        if progress:
            progress(fraction, message)

    readable_pages = [page for page in document.pages if not page.needs_ocr]
    if not readable_pages:
        raise ValueError(
            "Aucun texte extractible : le PDF semble scanné. Passez-le d'abord dans un outil d'OCR."
        )

    small_budget = max_chars < SMALL_BUDGET_CHARS
    full_text = format_pages(document.pages)
    notes: list[str] = []

    if len(full_text) <= max_chars:
        source_text, mode = full_text, "direct"
    else:
        chunks = chunk_pages(readable_pages, max_chars)
        for index, chunk in enumerate(chunks):
            first, last = chunk[0].number, chunk[-1].number
            report(0.7 * index / len(chunks), f"Lecture des pages {first} à {last} ({index + 1}/{len(chunks)})")
            messages = build_notes_messages(
                kind, format_pages(chunk), first, last, max_lines=25 if small_budget else 40
            )
            notes.append(f"### Pages {first} à {last}\n{chat(settings, messages)}")
        source_text, mode = "\n\n".join(notes), "notes"

        # Si les notes cumulées dépassent encore un bloc, on les condense par groupes.
        condensed = notes
        for round_number in range(1, MAX_CONDENSE_ROUNDS + 1):
            if len(source_text) <= max_chars:
                break
            groups = _group_by_size(condensed, max_chars)
            target = max(max_chars // (len(groups) + 1), 1_500)
            condensed = []
            for index, group in enumerate(groups):
                report(0.7, f"Condensation des notes (passe {round_number}, {index + 1}/{len(groups)})")
                condensed.append(chat(settings, build_condense_messages(kind, "\n\n".join(group), target)))
            source_text = "\n\n".join(condensed)
        source_text = source_text[:max_chars]

    schema = SCHEMAS[kind]
    parts = SCHEMA_PARTS[kind] if small_budget else [list(schema["properties"])]
    data: dict = {}
    for index, keys in enumerate(parts):
        label = "Rédaction de la fiche structurée" + (f" ({index + 1}/{len(parts)})" if len(parts) > 1 else "")
        report(0.75 + 0.25 * index / len(parts), label)
        part_schema = sub_schema(schema, keys)
        messages = build_summary_messages(
            kind, source_text, part_schema,
            from_notes=mode == "notes", level=level, research_focus=research_focus,
        )
        data.update(generate_structured(settings, messages, part_schema))

    report(1.0, "Fiche générée")
    return SummaryResult(data=data, mode=mode, notes=notes)
