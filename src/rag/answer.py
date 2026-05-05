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
            "hallucination_risk_reasons": ["no_citations", "insufficient_retrieved_evidence"],
            "stale_document_warning": False,
            "conflict_warning": False,
            "sensitive_data_warning": False,
        }

    snippets = " ".join(str(result["snippet"]) for result in evidence[:2])
    answer_text = f"Based on retrieved evidence: {snippets[:500]}"
    confidence = round(min(100.0, evidence[0]["final_score"] * 100), 2)
    citation_coverage = 100.0 if citations else 0.0
    groundedness = round((confidence + citation_coverage) / 2, 2)
    risk_reasons = _risk_reasons(citations, answer_text, evidence)
    return {
        "question": question,
        "answer_text": answer_text,
        "citations": citations,
        "confidence_score": confidence,
        "groundedness_score": groundedness,
        "citation_coverage_score": citation_coverage,
        "hallucination_risk_score": hallucination_risk(citations, confidence, risk_reasons),
        "hallucination_risk_reasons": risk_reasons,
        "stale_document_warning": stale_warning(evidence),
        "conflict_warning": conflict_warning(evidence),
        "sensitive_data_warning": sensitive_data_warning(evidence),
    }


def expected_aware_risk_reasons(
    answer: dict[str, object],
    retrieved_results: list[dict],
    expected_document_ids: list[str],
    is_answerable: bool,
    expected_stale_flag: bool,
    expected_conflict_flag: bool,
    expected_sensitive_flag: bool,
) -> list[str]:
    """Return evaluation-aware hallucination-risk reasons for reporting."""
    citations = list(answer.get("citations", []))
    reasons = list(answer.get("hallucination_risk_reasons", []))
    cited_docs = {str(citation.get("document_id", "")) for citation in citations}
    retrieved_docs = {str(result.get("document_id", "")) for result in retrieved_results}
    if is_answerable and not citations:
        reasons.append("answerable_question_without_citations")
    if not is_answerable and citations:
        reasons.append("unanswerable_question_with_citations")
    if expected_document_ids and not cited_docs.intersection(expected_document_ids):
        reasons.append("cited_documents_do_not_match_expected_evidence")
    if expected_document_ids and not retrieved_docs.intersection(expected_document_ids):
        reasons.append("retrieval_missed_expected_documents")
    if expected_stale_flag and not bool(answer.get("stale_document_warning")):
        reasons.append("missed_stale_document_warning")
    if expected_conflict_flag and not bool(answer.get("conflict_warning")):
        reasons.append("missed_conflict_warning")
    if expected_sensitive_flag and not bool(answer.get("sensitive_data_warning")):
        reasons.append("missed_sensitive_data_warning")
    return sorted(set(reasons))


def _risk_reasons(citations: list[dict], answer_text: str, evidence: list[dict]) -> list[str]:
    reasons: list[str] = []
    if not citations:
        reasons.append("no_citations")
    evidence_text = " ".join(str(result["snippet"]).lower() for result in evidence)
    answer_terms = {
        term
        for term in re.findall(r"[a-z0-9]+", answer_text.lower())
        if len(term) > 4 and term not in STOP_WORDS
    }
    missing_terms = [term for term in answer_terms if term not in evidence_text]
    if len(missing_terms) > 5:
        reasons.append("answer_contains_terms_not_present_in_retrieved_snippets")
    return reasons


def _has_query_evidence(question: str, snippet: str) -> bool:
    query_terms = {
        term
        for term in re.findall(r"[a-z0-9]+", question.lower())
        if len(term) > 2 and term not in STOP_WORDS
    }
    snippet_terms = set(re.findall(r"[a-z0-9]+", snippet.lower()))
    return len(query_terms & snippet_terms) >= 2
