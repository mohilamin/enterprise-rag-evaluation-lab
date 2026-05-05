from __future__ import annotations

import json

import pandas as pd

from src.common.config import get_path
from src.common.logging import get_logger
from src.common.paths import ensure_directory
from src.evaluation.answer_metrics import answerability_accuracy, flag_accuracy, overall_trust_score
from src.evaluation.retrieval_metrics import hit_at_k, reciprocal_rank
from src.rag.answer import answer_question
from src.retrieval.search import search

LOGGER = get_logger(__name__)


def load_golden_questions() -> list[dict[str, object]]:
    """Load golden evaluation questions."""
    path = get_path("evaluations") / "golden_questions.json"
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)["questions"]


def run_evaluation() -> dict[str, object]:
    """Run retrieval and answer evaluation over golden questions."""
    questions = load_golden_questions()
    retrieval_rows = []
    answer_rows = []
    for question in questions:
        text = str(question["question_text"])
        expected_docs = list(question["expected_document_ids"])
        results = search(text, top_k=5)
        answer = answer_question(text, top_k=5)
        retrieval_rows.append(
            {
                "question_id": question["question_id"],
                "hit_at_1": hit_at_k(results, expected_docs, 1),
                "hit_at_3": hit_at_k(results, expected_docs, 3),
                "hit_at_5": hit_at_k(results, expected_docs, 5),
                "mrr": reciprocal_rank(results, expected_docs),
                "top_document_id": results[0]["document_id"] if results else "",
            }
        )
        answer_rows.append(
            {
                "question_id": question["question_id"],
                "citation_coverage_score": answer["citation_coverage_score"],
                "groundedness_score": answer["groundedness_score"],
                "hallucination_risk_score": answer["hallucination_risk_score"],
                "stale_document_flag_accuracy": flag_accuracy(
                    bool(answer["stale_document_warning"]),
                    bool(question["should_flag_stale"]),
                ),
                "conflict_flag_accuracy": flag_accuracy(
                    bool(answer["conflict_warning"]),
                    bool(question["should_flag_conflict"]),
                ),
                "sensitive_data_flag_accuracy": flag_accuracy(
                    bool(answer["sensitive_data_warning"]),
                    bool(question["should_flag_sensitive_data"]),
                ),
                "answerability_accuracy": answerability_accuracy(
                    answer,
                    bool(question["is_answerable"]),
                ),
            }
        )

    retrieval_df = pd.DataFrame(retrieval_rows)
    answer_df = pd.DataFrame(answer_rows)
    eval_path = ensure_directory(get_path("evaluations"))
    retrieval_df.to_csv(eval_path / "retrieval_evaluation.csv", index=False)
    answer_df.to_csv(eval_path / "answer_evaluation.csv", index=False)

    summary_metrics = _summary(retrieval_df, answer_df)
    scorecard_path = ensure_directory(get_path("scorecards"))
    pd.DataFrame([summary_metrics]).to_csv(scorecard_path / "rag_trust_scorecard.csv", index=False)
    (scorecard_path / "rag_trust_summary.json").write_text(
        json.dumps(summary_metrics, indent=2),
        encoding="utf-8",
    )
    LOGGER.info("evaluation complete", extra=summary_metrics)
    return summary_metrics


def _summary(retrieval_df: pd.DataFrame, answer_df: pd.DataFrame) -> dict[str, float]:
    stale_risk = 100 - float(answer_df["stale_document_flag_accuracy"].mean())
    sensitive_risk = 100 - float(answer_df["sensitive_data_flag_accuracy"].mean())
    metrics = {
        "hit_at_1": round(float(retrieval_df["hit_at_1"].mean()), 4),
        "hit_at_3": round(float(retrieval_df["hit_at_3"].mean()), 4),
        "hit_at_5": round(float(retrieval_df["hit_at_5"].mean()), 4),
        "mrr": round(float(retrieval_df["mrr"].mean()), 4),
        "citation_coverage_score": round(float(answer_df["citation_coverage_score"].mean()), 2),
        "groundedness_score": round(float(answer_df["groundedness_score"].mean()), 2),
        "hallucination_risk_score": round(float(answer_df["hallucination_risk_score"].mean()), 2),
        "stale_document_risk_score": round(stale_risk, 2),
        "sensitive_data_risk_score": round(sensitive_risk, 2),
        "answerability_accuracy": round(float(answer_df["answerability_accuracy"].mean()), 2),
    }
    metrics["overall_rag_trust_score"] = overall_trust_score(metrics)
    return metrics
