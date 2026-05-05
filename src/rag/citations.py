from __future__ import annotations

import json

import pandas as pd

from src.common.config import get_path


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


def validate_citations(
    answer: dict[str, object],
    retrieved_results: list[dict],
    expected_document_ids: list[str] | None = None,
    is_answerable: bool = True,
) -> dict[str, object]:
    """Validate citation structure, existence, retrieval membership, and expected coverage."""
    expected_document_ids = expected_document_ids or []
    citations = list(answer.get("citations", []))
    retrieved_chunk_ids = {result["chunk_id"] for result in retrieved_results}
    chunk_ids = set(_load_chunk_ids())
    cited_document_ids = {str(citation.get("document_id", "")) for citation in citations}
    citation_chunk_ids = {str(citation.get("chunk_id", "")) for citation in citations}
    citations_have_required_fields = all(
        citation.get("document_id") and citation.get("chunk_id") for citation in citations
    )
    citations_reference_retrieved_chunks = citation_chunk_ids.issubset(retrieved_chunk_ids)
    cited_chunks_exist = citation_chunk_ids.issubset(chunk_ids)
    unanswerable_has_no_citations = is_answerable or not citations
    expected_coverage = 100.0
    if expected_document_ids:
        expected_coverage = round(
            len(cited_document_ids & set(expected_document_ids)) / len(expected_document_ids) * 100,
            2,
        )
    valid = (
        citations_have_required_fields
        and citations_reference_retrieved_chunks
        and cited_chunks_exist
        and unanswerable_has_no_citations
        and (bool(citations) if is_answerable else True)
    )
    return {
        "citation_validation_pass": valid,
        "citations_have_required_fields": citations_have_required_fields,
        "citations_reference_retrieved_chunks": citations_reference_retrieved_chunks,
        "cited_chunks_exist": cited_chunks_exist,
        "unanswerable_has_no_citations": unanswerable_has_no_citations,
        "expected_document_citation_coverage": expected_coverage,
        "cited_document_ids": sorted(cited_document_ids),
        "citation_json": json.dumps(citations),
    }


def _load_chunk_ids() -> list[str]:
    path = get_path("chunks") / "chunks.csv"
    if not path.exists():
        return []
    return pd.read_csv(path)["chunk_id"].astype(str).tolist()
