from __future__ import annotations

import re

from src.rag.citations import build_citations
from src.rag.risk import (
    conflict_warning,
    hallucination_risk,
    sensitive_data_warning,
    stale_warning,
)
from src.retrieval.search import search

INSUFFICIENT = "Insufficient evidence in retrieved documents."
STOP_WORDS = {
    "the",
    "is",
    "are",
    "what",
    "when",
    "which",
    "how",
    "must",
    "for",
    "with",
    "and",
    "company",
}


def answer_question(question: str, top_k: int = 5) -> dict[str, object]:
    """Compose a deterministic citation-grounded answer from retrieved chunks."""
    results = search(question, top_k=top_k)
    evidence = [
        result
        for result in results
        if result["final_score"] > 0.05 and _has_query_evidence(question, str(result["snippet"]))
    ]
    citations = build_citations(evidence[:3])
    if not citations:
        return {
            "question": question,
            "answer_text": INSUFFICIENT,
            "citations": [],
            "confidence_score": 0.0,
            "groundedness_score": 0.0,
            "citation_coverage_score": 0.0,
            "hallucination_risk_score": 100.0,
            "stale_document_warning": False,
            "conflict_warning": False,
            "sensitive_data_warning": False,
        }

    snippets = " ".join(str(result["snippet"]) for result in evidence[:2])
    answer_text = f"Based on retrieved evidence: {snippets[:500]}"
    confidence = round(min(100.0, evidence[0]["final_score"] * 100), 2)
    citation_coverage = 100.0 if citations else 0.0
    groundedness = round((confidence + citation_coverage) / 2, 2)
    return {
        "question": question,
        "answer_text": answer_text,
        "citations": citations,
        "confidence_score": confidence,
        "groundedness_score": groundedness,
        "citation_coverage_score": citation_coverage,
        "hallucination_risk_score": hallucination_risk(citations, confidence),
        "stale_document_warning": stale_warning(evidence),
        "conflict_warning": conflict_warning(evidence),
        "sensitive_data_warning": sensitive_data_warning(evidence),
    }


def _has_query_evidence(question: str, snippet: str) -> bool:
    query_terms = {
        term
        for term in re.findall(r"[a-z0-9]+", question.lower())
        if len(term) > 2 and term not in STOP_WORDS
    }
    snippet_terms = set(re.findall(r"[a-z0-9]+", snippet.lower()))
    return len(query_terms & snippet_terms) >= 2
