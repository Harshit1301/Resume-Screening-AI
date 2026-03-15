from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class CandidateScore:
    rank: int
    candidate_name: str
    resume_name: str
    similarity_score: float
    matched_keywords: List[str]


class ResumeRanker:
    """Embeds resumes and computes relevance scores against a job description."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Generate embeddings efficiently in batches."""
        return self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=False,
            normalize_embeddings=True,
        )

    def rank(self, job_description: str, resume_texts: List[str]) -> np.ndarray:
        """Compute cosine similarity scores between JD and each resume."""
        jd_embedding = self.embed_texts([job_description], batch_size=1)
        resume_embeddings = self.embed_texts(resume_texts)
        similarities = cosine_similarity(jd_embedding, resume_embeddings).ravel()
        return similarities
