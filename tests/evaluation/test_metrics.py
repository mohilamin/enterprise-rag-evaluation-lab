from __future__ import annotations

from src.evaluation.answer_metrics import answerability_accuracy, flag_accuracy, overall_trust_score
from src.evaluation.retrieval_metrics import hit_at_k, reciprocal_rank


def test_retrieval_metric_calculation() -> None:
    results = [{"document_id": "DOC-A", "rank": 1}, {"document_id": "DOC-B", "rank": 2}]
    assert hit_at_k(results, ["DOC-B"], 2) == 1.0
    assert reciprocal_rank(results, ["DOC-B"]) == 0.5


def test_answer_metric_calculation() -> None:
    answer = {"answer_text": "Based on retrieved evidence"}
    assert answerability_accuracy(answer, True) == 100.0
    assert flag_accuracy(True, True) == 100.0


def test_overall_trust_score_bounds() -> None:
    score = overall_trust_score(
        {
            "hit_at_3": 1.0,
            "mrr": 1.0,
            "citation_coverage_score": 100.0,
            "groundedness_score": 90.0,
            "hallucination_risk_score": 10.0,
            "stale_document_risk_score": 0.0,
            "sensitive_data_risk_score": 0.0,
            "answerability_accuracy": 100.0,
        }
    )
    assert 0 <= score <= 100
