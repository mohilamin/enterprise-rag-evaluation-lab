from __future__ import annotations


def build_citations(results: list[dict]) -> list[dict[str, object]]:
    """Build citation records from retrieved chunks."""
    return [
        {
            "document_id": result["document_id"],
            "chunk_id": result["chunk_id"],
            "title": result["title"],
            "rank": result["rank"],
        }
        for result in results
        if result.get("final_score", 0) > 0
    ]
