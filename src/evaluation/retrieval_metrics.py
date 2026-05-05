from __future__ import annotations


def hit_at_k(results: list[dict], expected_document_ids: list[str], k: int) -> float:
    """Return 1 when any expected document appears in top k results."""
    if not expected_document_ids:
        return 1.0 if not results else 0.0
    top_docs = {result["document_id"] for result in results[:k]}
    return 1.0 if top_docs & set(expected_document_ids) else 0.0


def reciprocal_rank(results: list[dict], expected_document_ids: list[str]) -> float:
    """Return reciprocal rank for the first expected document."""
    if not expected_document_ids:
        return 1.0
    expected = set(expected_document_ids)
    for result in results:
        if result["document_id"] in expected:
            return round(1.0 / int(result["rank"]), 4)
    return 0.0
