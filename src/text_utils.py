from __future__ import annotations

import re
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "you",
    "your",
    "are",
    "our",
    "job",
    "role",
    "will",
    "have",
    "has",
    "in",
    "on",
    "to",
    "of",
    "a",
    "an",
    "as",
    "or",
    "is",
    "be",
}


def normalize_for_match(text: str) -> str:
    """Lowercase and strip non-word characters for fast keyword checks."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_job_keywords(job_description: str, top_k: int = 15) -> List[str]:
    """Extract top keywords from job description via TF-IDF."""
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", max_features=2000)
    matrix = vectorizer.fit_transform([job_description])
    terms = vectorizer.get_feature_names_out()
    scores = matrix.toarray().ravel()

    ranked = sorted(zip(terms, scores), key=lambda item: item[1], reverse=True)
    keywords = []
    for term, _ in ranked:
        if term in STOPWORDS:
            continue
        if len(term) < 3:
            continue
        keywords.append(term)
        if len(keywords) >= top_k:
            break
    return keywords


def matched_keywords(text: str, keywords: List[str], top_k: int = 8) -> List[str]:
    """Return matched job keywords found in resume text."""
    text_norm = normalize_for_match(text)
    matches = [kw for kw in keywords if kw in text_norm]
    return matches[:top_k]
