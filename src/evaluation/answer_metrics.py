from __future__ import annotations


def answerability_accuracy(answer: dict[str, object], is_answerable: bool) -> float:
    """Score whether the answer correctly answered or abstained."""
    insufficient = str(answer["answer_text"]).startswith("Insufficient evidence")
    return 100.0 if insufficient != is_answerable else 0.0


def flag_accuracy(actual: bool, expected: bool) -> float:
    """Score whether a boolean risk flag matched expectation."""
    return 100.0 if bool(actual) == bool(expected) else 0.0


def overall_trust_score(metrics: dict[str, float]) -> float:
    """Calculate a compact overall RAG trust score."""
    score = (
        metrics["hit_at_3"] * 20
        + metrics["mrr"] * 20
        + metrics["citation_coverage_score"] * 0.15
        + metrics["groundedness_score"] * 0.20
        + (100 - metrics["hallucination_risk_score"]) * 0.10
        + (100 - metrics["stale_document_risk_score"]) * 0.05
        + (100 - metrics["sensitive_data_risk_score"]) * 0.05
        + metrics["answerability_accuracy"] * 0.05
    )
    return round(max(0.0, min(100.0, score)), 2)
