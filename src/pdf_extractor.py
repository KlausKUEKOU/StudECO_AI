"""Extraction du texte des PDF, page par page, avec détection des pages à OCRiser."""

import re
from dataclasses import dataclass, field

import pymupdf

# En dessous de ce nombre de caractères, une page est considérée comme sans texte
# exploitable (scan, image, page de garde vide).
MIN_CHARS_PER_PAGE = 40


@dataclass
class PageText:
    number: int
    text: str
    image_count: int = 0

    @property
    def needs_ocr(self) -> bool:
        return len(self.text.strip()) < MIN_CHARS_PER_PAGE


@dataclass
class ExtractedDocument:
    filename: str
    pages: list[PageText]
    metadata: dict = field(default_factory=dict)

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def full_text(self) -> str:
        return "\n".join(page.text for page in self.pages)

    @property
    def word_count(self) -> int:
        return len(self.full_text.split())

    @property
    def ocr_pages(self) -> list[int]:
        return [page.number for page in self.pages if page.needs_ocr]

    @property
    def is_probably_scanned(self) -> bool:
        return bool(self.pages) and len(self.ocr_pages) > self.page_count / 2


def _clean_text(text: str) -> str:
    text = text.replace("­", "")  # tirets conditionnels
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)  # mots coupés en fin de ligne
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf(data: bytes, filename: str) -> ExtractedDocument:
    try:
        document = pymupdf.open(stream=data, filetype="pdf")
    except Exception as exc:  # PyMuPDF lève plusieurs types selon la corruption
        raise ValueError(f"Impossible d'ouvrir « {filename} » : fichier PDF invalide.") from exc

    with document:
        if document.needs_pass:
            raise ValueError(f"« {filename} » est protégé par un mot de passe.")
        pages = [
            PageText(
                number=index + 1,
                text=_clean_text(page.get_text("text", sort=True)),
                image_count=len(page.get_images()),
            )
            for index, page in enumerate(document)
        ]
        metadata = {key: value for key, value in (document.metadata or {}).items() if value}

    return ExtractedDocument(filename=filename, pages=pages, metadata=metadata)


def format_pages(pages: list[PageText]) -> str:
    """Texte balisé par page, pour que le modèle puisse citer ses sources."""
    blocks = []
    for page in pages:
        body = page.text if not page.needs_ocr else "(aucun texte extractible - scan ou image probable)"
        blocks.append(f"[Page {page.number}]\n{body}")
    return "\n\n".join(blocks)


def chunk_pages(pages: list[PageText], max_chars: int) -> list[list[PageText]]:
    """Regroupe les pages en blocs d'au plus max_chars caractères ; découpe les pages trop longues."""
    chunks: list[list[PageText]] = []
    current: list[PageText] = []
    size = 0

    for page in pages:
        parts = [page]
        if len(page.text) > max_chars:
            parts = [
                PageText(page.number, page.text[start : start + max_chars], page.image_count)
                for start in range(0, len(page.text), max_chars)
            ]
        for part in parts:
            if current and size + len(part.text) > max_chars:
                chunks.append(current)
                current, size = [], 0
            current.append(part)
            size += len(part.text)

    if current:
        chunks.append(current)
    return chunks


_TYPE_MARKERS = {
    "article": [
        "abstract", "jel", "keywords", "mots-clés", "this paper", "we find", "we show",
        "our results", "robustness", "identification", "literature", "nous montrons",
        "cet article", "references", "working paper", "journal",
    ],
    "cours": [
        "chapitre", "chapter", "cours", "lecture", "séance", "exercice", "exercise",
        "définition", "objectifs", "td ", "travaux dirigés", "rappel", "à retenir",
    ],
    "rapport": [
        "rapport", "report", "recommandation", "recommendation", "executive summary",
        "synthèse", "note de conjoncture", "policy brief",
    ],
}


def guess_document_type(document: ExtractedDocument) -> str:
    """Estimation heuristique du type de document : « article », « cours », « rapport » ou « inconnu »."""
    head = " ".join(page.text for page in document.pages[:3]).lower()
    scores = {
        kind: sum(head.count(marker) for marker in markers)
        for kind, markers in _TYPE_MARKERS.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] >= 2 else "inconnu"
