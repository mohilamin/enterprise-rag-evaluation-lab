from __future__ import annotations


def rerank_score(query: str, row: dict[str, object], retrieval_score: float) -> float:
    """Apply lightweight metadata-aware reranking."""
    query_lower = query.lower()
    score = retrieval_score * 0.78
    if not bool(row.get("is_stale")):
        score += 0.04
    else:
        score -= 0.08
    department = str(row.get("department", "")).lower()
    if department and department in query_lower:
        score += 0.05
    title_tokens = set(str(row.get("title", "")).lower().split())
    query_tokens = set(query_lower.split())
    if title_tokens & query_tokens:
        score += 0.04
    return round(max(score, 0.0), 6)
