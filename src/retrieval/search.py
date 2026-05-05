from __future__ import annotations

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.common.config import get_path, get_settings
from src.retrieval.rerank import rerank_score


def load_chunks() -> pd.DataFrame:
    """Load generated chunks."""
    path = get_path("chunks") / "chunks.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def search(query: str, top_k: int | None = None, chunks: pd.DataFrame | None = None) -> list[dict]:
    """Search chunks using TF-IDF cosine similarity and deterministic reranking."""
    chunks = chunks if chunks is not None else load_chunks()
    if chunks.empty:
        return []
    top_k = top_k or int(get_settings()["retrieval"]["top_k"])
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(chunks["text"].fillna(""))
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, matrix).flatten()
    rows = []
    for index, score in enumerate(scores):
        row = chunks.iloc[index].fillna("").to_dict()
        final_score = rerank_score(query, row, float(score))
        rows.append(
            {
                "query": query,
                "chunk_id": row["chunk_id"],
                "document_id": row["document_id"],
                "title": row["title"],
                "retrieval_score": round(float(score), 6),
                "rerank_score": round(final_score - float(score), 6),
                "final_score": final_score,
                "snippet": str(row["text"])[:350],
                "metadata": {
                    "department": row["department"],
                    "version": row["version"],
                    "owner": row["owner"],
                    "confidentiality_level": row["confidentiality_level"],
                    "last_reviewed_date": row["last_reviewed_date"],
                    "is_stale": bool(row["is_stale"]),
                    "has_sensitive_pattern": bool(row["has_sensitive_pattern"]),
                    "has_conflict_language": bool(row["has_conflict_language"]),
                },
            }
        )
    ranked = sorted(rows, key=lambda item: item["final_score"], reverse=True)[:top_k]
    for rank, row in enumerate(ranked, start=1):
        row["rank"] = rank
    return ranked
