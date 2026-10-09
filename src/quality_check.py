"""Contrôles automatiques de fidélité d'une fiche par rapport au document source."""

import re
import unicodedata
from collections.abc import Iterator
from dataclasses import dataclass

from src.pdf_extractor import ExtractedDocument
from src.schemas import NOT_FOUND


@dataclass
class Finding:
    level: str  # "error", "warning" ou "info"
    message: str


_PAGE_RE = re.compile(r"\bp(?:p|ages?)?\.?\s*(\d+)(?:\s*(?:-|–|à)\s*(\d+))?", re.IGNORECASE)
_NUMBER_RE = re.compile(r"(?<![\w.])-?\d+(?:[.,]\d+)?%?")
_SOURCE_KEYS = {"source", "page", "sources_used"}


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"[‘’´`]", "'", text)
    text = re.sub(r"[«»“”„]", '"', text)
    text = re.sub(r"(\d)\s?,\s?(\d)", r"\1.\2", text)  # 1,5 -> 1.5
    text = re.sub(r"(\d)[\s ](\d{3})\b", r"\1\2", text)  # 12 500 -> 12500
    return re.sub(r"\s+", " ", text)


def _walk(value, path: tuple = ()) -> Iterator[tuple[tuple, str]]:
    if isinstance(value, dict):
        for key, item in value.items():
            yield from _walk(item, path + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk(item, path + (index,))
    elif isinstance(value, str):
        yield path, value


def _is_source(path: tuple) -> bool:
    return any(key in _SOURCE_KEYS for key in path if isinstance(key, str))


def _check_pages(data: dict, document: ExtractedDocument) -> list[Finding]:
    findings = []
    sources = [(path, text) for path, text in _walk(data) if _is_source(path)]
    out_of_range = set()
    unsourced = 0
    for _, text in sources:
        pages = [int(n) for match in _PAGE_RE.finditer(text) for n in match.groups() if n]
        out_of_range.update(p for p in pages if p < 1 or p > document.page_count)
        if not pages and (not text.strip() or NOT_FOUND.lower() in text.lower()):
            unsourced += 1

    if out_of_range:
        findings.append(Finding(
            "error",
            f"Pages citées inexistantes (le document en compte {document.page_count}) : "
            + ", ".join(map(str, sorted(out_of_range))),
        ))
    if sources and unsourced:
        findings.append(Finding(
            "warning", f"{unsourced} élément(s) sur {len(sources)} sans page d'origine identifiée."
        ))
    elif sources:
        findings.append(Finding("info", f"Tous les éléments sourcés ({len(sources)}) renvoient à une page."))
    return findings


def _check_numbers(data: dict, source_text: str) -> list[Finding]:
    missing = []
    # « 1,240 » (anglais) devient « 1.240 » après normalisation : on accepte aussi « 1240 ».
    source_without_thousands = re.sub(r"(\d)\.(\d{3})(?!\d)", r"\1\2", source_text)
    for path, text in _walk(data):
        if _is_source(path):
            continue
        for raw in _NUMBER_RE.findall(_normalize(text)):
            number = raw.rstrip("%").lstrip("-")
            if len(number.replace(".", "")) < 2:  # on ignore les chiffres isolés (1, 2, 3...)
                continue
            if number not in source_text and number not in source_without_thousands and raw not in missing:
                missing.append(raw)
    if missing:
        return [Finding(
            "warning",
            "Chiffres absents du texte extrait - à vérifier dans le document : " + ", ".join(missing[:15]),
        )]
    return [Finding("info", "Tous les chiffres de la fiche figurent dans le texte extrait.")]


def _check_quotes(data: dict, source_text: str) -> list[Finding]:
    quotes = [q.get("quote", "") for q in data.get("key_quotes", []) if isinstance(q, dict)]
    findings = []
    for quote in quotes:
        cleaned = _normalize(quote).strip(' "….')
        if cleaned and cleaned not in source_text:
            findings.append(Finding("warning", f"Citation introuvable mot pour mot : « {quote[:120]} »"))
    if quotes and not findings:
        findings.append(Finding("info", f"Les {len(quotes)} citations ont été retrouvées dans le texte."))
    return findings


def _check_causality(data: dict) -> list[Finding]:
    identification = str(data.get("data_method", {}).get("identification", ""))
    no_identification = not identification.strip() or NOT_FOUND.lower() in identification.lower()
    results = [r for r in data.get("results", []) if isinstance(r, dict)]
    findings = []
    causal = [r for r in results if r.get("evidence_type") == "causal sous hypothèses"]
    if causal and no_identification:
        findings.append(Finding(
            "error",
            f"{len(causal)} résultat(s) présenté(s) comme causal(aux) alors qu'aucune "
            "stratégie d'identification n'est décrite.",
        ))
    unlabeled = sum(r.get("evidence_type") == "non précisé" for r in results)
    if unlabeled:
        findings.append(Finding("info", f"{unlabeled} résultat(s) sans nature de preuve établie."))
    return findings


def run_checks(kind: str, data: dict, document: ExtractedDocument) -> list[Finding]:
    source_text = _normalize(document.full_text)
    findings: list[Finding] = []

    if document.ocr_pages:
        findings.append(Finding(
            "warning",
            f"{len(document.ocr_pages)} page(s) sans texte extractible (scan probable) : leur contenu "
            "n'a pas été lu - " + ", ".join(map(str, document.ocr_pages[:20])),
        ))

    findings += _check_pages(data, document)
    findings += _check_numbers(data, source_text)

    if kind == "course":
        count = len(data.get("key_ideas", []))
        if count != 5:
            findings.append(Finding("info", f"{count} idées clés au lieu des 5 demandées."))
    else:
        findings += _check_quotes(data, source_text)
        findings += _check_causality(data)

    missing = data.get("missing_information", [])
    if missing:
        findings.append(Finding("info", "Informations signalées absentes par l'agent : " + " ; ".join(missing)))

    order = {"error": 0, "warning": 1, "info": 2}
    return sorted(findings, key=lambda f: order[f.level])
