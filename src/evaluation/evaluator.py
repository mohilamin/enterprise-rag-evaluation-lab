from __future__ import annotations

import json

import pandas as pd

from src.common.config import get_path
from src.common.logging import get_logger
from src.common.paths import ensure_directory
from src.evaluation.answer_metrics import answerability_accuracy, flag_accuracy, overall_trust_score
from src.evaluation.retrieval_metrics import hit_at_k, reciprocal_rank
from src.rag.answer import answer_question, expected_aware_risk_reasons
from src.rag.citations import validate_citations
from src.retrieval.search import search

LOGGER = get_logger(__name__)


def load_golden_questions() -> list[dict[str, object]]:
    """Load golden evaluation questions."""
    path = get_path("evaluations") / "golden_questions.json"
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)["questions"]


def run_evaluation() -> dict[str, object]:
    """Run retrieval, answer, and evidence reporting over golden questions."""
    questions = load_golden_questions()
    retrieval_rows = []
    answer_rows = []
    for question in questions:
        text = str(question["question_text"])
        expected_docs = [str(doc_id) for doc_id in question["expected_document_ids"]]
        results = search(text, top_k=5)
        answer = answer_question(text, top_k=5)
        retrieved_docs = [str(result["document_id"]) for result in results]
        citation_validation = validate_citations(
            answer,
            results,
            expected_docs,
            bool(question["is_answerable"]),
        )
        risk_reasons = expected_aware_risk_reasons(
            answer,
            results,
            expected_docs,
            bool(question["is_answerable"]),
            bool(question["should_flag_stale"]),
            bool(question["should_flag_conflict"]),
            bool(question["should_flag_sensitive_data"]),
        )
        retrieval_pass = (
            bool(set(expected_docs) & set(retrieved_docs[:5])) if expected_docs else True
        )
        retrieval_rows.append(
            {
                "question_id": question["question_id"],
                "question_type": question["question_type"],
                "is_answerable": question["is_answerable"],
                "expected_document_ids": json.dumps(expected_docs),
                "top_retrieved_document_ids": json.dumps(retrieved_docs[:5]),
                "retrieval_pass_fail": "pass" if retrieval_pass else "fail",
                "hit_at_1": hit_at_k(results, expected_docs, 1),
                "hit_at_3": hit_at_k(results, expected_docs, 3),
                "hit_at_5": hit_at_k(results, expected_docs, 5),
                "mrr": reciprocal_rank(results, expected_docs),
            }
        )
        answer_pass = _answer_pass(question, answer, citation_validation)
        answer_rows.append(
            {
                "question_id": question["question_id"],
                "question_type": question["question_type"],
                "is_answerable": question["is_answerable"],
                "expected_document_ids": json.dumps(expected_docs),
                "answer_text": answer["answer_text"],
                "citations": json.dumps(answer["citations"]),
                "confidence_score": answer["confidence_score"],
                "groundedness_score": answer["groundedness_score"],
                "citation_coverage_score": citation_validation[
                    "expected_document_citation_coverage"
                ],
                "hallucination_risk_score": _risk_score_with_reasons(
                    float(answer["hallucination_risk_score"]),
                    risk_reasons,
                ),
                "hallucination_risk_reasons": json.dumps(risk_reasons),
                "expected_stale_flag": question["should_flag_stale"],
                "actual_stale_flag": answer["stale_document_warning"],
                "expected_conflict_flag": question["should_flag_conflict"],
                "actual_conflict_flag": answer["conflict_warning"],
                "expected_sensitive_flag": question["should_flag_sensitive_data"],
                "actual_sensitive_flag": answer["sensitive_data_warning"],
                "citation_validation_pass": citation_validation["citation_validation_pass"],
                "pass_fail": "pass" if answer_pass else "fail",
            }
        )

    retrieval_df = pd.DataFrame(retrieval_rows)
    answer_df = pd.DataFrame(answer_rows)
    eval_path = ensure_directory(get_path("evaluations"))
    retrieval_df.to_csv(eval_path / "retrieval_evaluation.csv", index=False)
    answer_df.to_csv(eval_path / "answer_evaluation.csv", index=False)

    retrieval_report = _retrieval_report(retrieval_df)
    answer_report = _answer_report(answer_df)
    summary_metrics = _summary(retrieval_report, answer_report)
    _write_scorecards(retrieval_report, retrieval_df, answer_report, answer_df, summary_metrics)
    LOGGER.info("evaluation complete", extra=summary_metrics)
    return summary_metrics


def _answer_pass(
    question: dict[str, object],
    answer: dict[str, object],
    citation_validation: dict[str, object],
) -> bool:
    insufficient = str(answer["answer_text"]).startswith("Insufficient evidence")
    if bool(question["is_answerable"]) and insufficient:
        return False
    if not bool(question["is_answerable"]) and not insufficient:
        return False
    return (
        bool(citation_validation["citation_validation_pass"])
        and bool(answer["stale_document_warning"]) == bool(question["should_flag_stale"])
        and bool(answer["conflict_warning"]) == bool(question["should_flag_conflict"])
        and bool(answer["sensitive_data_warning"]) == bool(question["should_flag_sensitive_data"])
    )


def _risk_score_with_reasons(base_score: float, reasons: list[str]) -> float:
    return round(min(100.0, base_score + max(0, len(reasons) - 1) * 8), 2)


def _retrieval_report(retrieval_df: pd.DataFrame) -> dict[str, object]:
    answerable = retrieval_df[retrieval_df["is_answerable"]]
    success_by_type = (
        retrieval_df.assign(success=retrieval_df["retrieval_pass_fail"].eq("pass"))
        .groupby("question_type")["success"]
        .mean()
        .round(4)
        .to_dict()
    )
    missed = retrieval_df.loc[
        retrieval_df["retrieval_pass_fail"].eq("fail"),
        ["question_id", "question_type", "expected_document_ids", "top_retrieved_document_ids"],
    ].to_dict("records")
    return {
        "total_questions": int(len(retrieval_df)),
        "answerable_questions": int(retrieval_df["is_answerable"].sum()),
        "unanswerable_questions": int((~retrieval_df["is_answerable"]).sum()),
        "hit_at_1": round(float(answerable["hit_at_1"].mean()), 4),
        "hit_at_3": round(float(answerable["hit_at_3"].mean()), 4),
        "hit_at_5": round(float(answerable["hit_at_5"].mean()), 4),
        "mrr": round(float(answerable["mrr"].mean()), 4),
        "retrieval_success_by_question_type": success_by_type,
        "missed_questions": missed,
    }


def _answer_report(answer_df: pd.DataFrame) -> dict[str, object]:
    answerability_scores = [
        answerability_accuracy({"answer_text": row["answer_text"]}, bool(row["is_answerable"]))
        for row in answer_df.to_dict("records")
    ]
    insufficient_scores = [
        100.0
        if bool(row["is_answerable"])
        != str(row["answer_text"]).startswith("Insufficient evidence")
        else 0.0
        for row in answer_df.to_dict("records")
    ]
    return {
        "total_questions": int(len(answer_df)),
        "answerability_accuracy": round(sum(answerability_scores) / len(answerability_scores), 2),
        "citation_coverage_average": round(float(answer_df["citation_coverage_score"].mean()), 2),
        "groundedness_average": round(float(answer_df["groundedness_score"].mean()), 2),
        "hallucination_risk_average": round(
            float(answer_df["hallucination_risk_score"].mean()),
            2,
        ),
        "stale_warning_accuracy": _flag_mean(answer_df, "expected_stale_flag", "actual_stale_flag"),
        "conflict_warning_accuracy": _flag_mean(
            answer_df,
            "expected_conflict_flag",
            "actual_conflict_flag",
        ),
        "sensitive_data_warning_accuracy": _flag_mean(
            answer_df,
            "expected_sensitive_flag",
            "actual_sensitive_flag",
        ),
        "insufficient_evidence_accuracy": round(
            sum(insufficient_scores) / len(insufficient_scores),
            2,
        ),
    }


def _flag_mean(answer_df: pd.DataFrame, expected_col: str, actual_col: str) -> float:
    scores = [
        flag_accuracy(bool(row[actual_col]), bool(row[expected_col]))
        for row in answer_df.to_dict("records")
    ]
    return round(sum(scores) / len(scores), 2)


def _summary(
    retrieval_report: dict[str, object],
    answer_report: dict[str, object],
) -> dict[str, float]:
    metrics = {
        "hit_at_1": float(retrieval_report["hit_at_1"]),
        "hit_at_3": float(retrieval_report["hit_at_3"]),
        "hit_at_5": float(retrieval_report["hit_at_5"]),
        "mrr": float(retrieval_report["mrr"]),
        "citation_coverage_score": float(answer_report["citation_coverage_average"]),
        "citation_coverage_average": float(answer_report["citation_coverage_average"]),
        "groundedness_score": float(answer_report["groundedness_average"]),
        "groundedness_average": float(answer_report["groundedness_average"]),
        "hallucination_risk_score": float(answer_report["hallucination_risk_average"]),
        "hallucination_risk_average": float(answer_report["hallucination_risk_average"]),
        "stale_document_risk_score": 100.0 - float(answer_report["stale_warning_accuracy"]),
        "conflict_warning_accuracy": float(answer_report["conflict_warning_accuracy"]),
        "sensitive_data_warning_accuracy": float(answer_report["sensitive_data_warning_accuracy"]),
        "sensitive_data_risk_score": 100.0
        - float(answer_report["sensitive_data_warning_accuracy"]),
        "answerability_accuracy": float(answer_report["answerability_accuracy"]),
    }
    metrics["overall_rag_trust_score"] = overall_trust_score(metrics)
    return metrics


def _write_scorecards(
    retrieval_report: dict[str, object],
    retrieval_df: pd.DataFrame,
    answer_report: dict[str, object],
    answer_df: pd.DataFrame,
    summary_metrics: dict[str, float],
) -> None:
    scorecard_path = ensure_directory(get_path("scorecards"))
    retrieval_df.to_csv(scorecard_path / "retrieval_accuracy_report.csv", index=False)
    answer_df.to_csv(scorecard_path / "answer_quality_report.csv", index=False)
    answer_report["overall_rag_trust_score"] = summary_metrics["overall_rag_trust_score"]
    (scorecard_path / "retrieval_accuracy_report.json").write_text(
        json.dumps(retrieval_report, indent=2),
        encoding="utf-8",
    )
    (scorecard_path / "answer_quality_report.json").write_text(
        json.dumps(answer_report, indent=2),
        encoding="utf-8",
    )
    pd.DataFrame([summary_metrics]).to_csv(scorecard_path / "rag_trust_scorecard.csv", index=False)
    (scorecard_path / "rag_trust_summary.json").write_text(
        json.dumps(summary_metrics, indent=2),
        encoding="utf-8",
    )
