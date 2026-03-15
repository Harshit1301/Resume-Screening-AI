from __future__ import annotations

import io
import re
from typing import Tuple

from PyPDF2 import PdfReader


def clean_text(text: str) -> str:
    """Normalize whitespace and remove excessive blank lines."""
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from a PDF byte stream using PyPDF2."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text:
            pages.append(page_text)
    return clean_text("\n".join(pages))


def detect_candidate_name(text: str, fallback_filename: str) -> str:
    """Best-effort candidate name detection from resume content.

    Strategy:
    - use the first meaningful line
    - ensure line looks like a name (2-5 alpha words)
    - fallback to file stem
    """
    # Recover rough line boundaries from normalized text by splitting sentences.
    # For heavily cleaned text, this still gives a reasonable heuristic.
    tokens = re.split(r"[\n\r\.!?]+", text)
    for token in tokens[:15]:
        line = token.strip()
        if not line:
            continue
        words = line.split()
        if 1 < len(words) <= 5 and all(re.match(r"^[A-Za-z][A-Za-z\-']+$", w) for w in words):
            return " ".join(words)

    fallback = fallback_filename.rsplit(".", 1)[0]
    fallback = fallback.replace("_", " ").replace("-", " ")
    return fallback.title()


def parse_resume(pdf_bytes: bytes, filename: str) -> Tuple[str, str]:
    """Extract text and candidate name from a resume PDF."""
    text = extract_text_from_pdf(pdf_bytes)
    candidate_name = detect_candidate_name(text, filename)
    return candidate_name, text
