from __future__ import annotations

import json
from collections import Counter

import pandas as pd

from src.chunking.chunker import chunk_documents, save_chunks
from src.common.config import get_path
from src.data_generation.generate_documents import generate_documents
from src.data_generation.generate_golden_questions import generate_golden_questions
from src.ingestion.loaders import load_documents
from src.pipeline.run_all import run_pipeline
from src.rag.answer import answer_question, expected_aware_risk_reasons
from src.rag.citations import validate_citations
from src.retrieval.search import search


def test_golden_question_distribution() -> None:
    generate_golden_questions()
    questions = json.loads((get_path("evaluations") / "golden_questions.json").read_text())[
        "questions"
    ]
    counts = Counter(question["question_type"] for question in questions)
    assert len(questions) == 40
    assert counts["single_document_answerable"] == 10
    assert counts["multi_document_answerable"] == 8
    assert counts["unanswerable"] == 6
    assert counts["stale_document_trap"] == 5
    assert counts["conflict_detection"] == 5
    assert counts["sensitive_data_risk"] == 3
    assert counts["department_specific_policy"] == 3


def test_chunk_quality_report_creation() -> None:
    generate_documents()
    chunks = chunk_documents(load_documents())
    save_chunks(chunks)
    assert (get_path("scorecards") / "chunk_quality_report.csv").exists()
    assert (get_path("scorecards") / "chunk_quality_summary.json").exists()


def test_chunk_metadata_fields_exist() -> None:
    generate_documents()
    chunks = chunk_documents(load_documents())
    expected = {
        "token_or_word_count",
        "section_heading",
        "stale_flag",
        "sensitive_data_flag",
    }
    assert expected.issubset(chunks.columns)


def test_retrieval_accuracy_report_creation() -> None:
    run_pipeline()
    assert (get_path("scorecards") / "retrieval_accuracy_report.json").exists()
    assert (get_path("scorecards") / "retrieval_accuracy_report.csv").exists()


def test_answer_quality_report_creation() -> None:
    run_pipeline()
    assert (get_path("scorecards") / "answer_quality_report.json").exists()
    assert (get_path("scorecards") / "answer_quality_report.csv").exists()


def test_retrieval_report_contains_missed_questions() -> None:
    run_pipeline()
    report = json.loads((get_path("scorecards") / "retrieval_accuracy_report.json").read_text())
    assert "missed_questions" in report
    assert "retrieval_success_by_question_type" in report


def test_answer_quality_report_contains_risk_reasons() -> None:
    run_pipeline()
    report = pd.read_csv(get_path("scorecards") / "answer_quality_report.csv")
    assert "hallucination_risk_reasons" in report.columns


def test_citation_validation_passes_for_answerable_question() -> None:
    run_pipeline()
    results = search("How quickly must vendors report a confirmed data incident?")
    answer = answer_question("How quickly must vendors report a confirmed data incident?")
    validation = validate_citations(answer, results, ["DOC-VEN-001"], True)
    assert validation["citations_have_required_fields"] is True
    assert validation["cited_chunks_exist"] is True


def test_citation_validation_blocks_unanswerable_citations() -> None:
    run_pipeline()
    results = search("What is the company travel reimbursement meal limit?")
    answer = {"citations": [{"document_id": "DOC-VEN-001", "chunk_id": results[0]["chunk_id"]}]}
    validation = validate_citations(answer, results, [], False)
    assert validation["unanswerable_has_no_citations"] is False


def test_hallucination_risk_reasons_for_unanswerable_question() -> None:
    run_pipeline()
    answer = answer_question("What is the company travel reimbursement meal limit?")
    reasons = expected_aware_risk_reasons(answer, [], [], False, False, False, False)
    assert "no_citations" in reasons


def test_expected_document_retrieval() -> None:
    run_pipeline()
    results = search("What controls are required for privileged access?")
    assert results[0]["document_id"] == "DOC-IT-001"


def test_score_range_validation() -> None:
    run_pipeline()
    summary = json.loads((get_path("scorecards") / "rag_trust_summary.json").read_text())
    score_keys = [key for key in summary if key.endswith("_score") or key.endswith("_average")]
    assert all(0 <= float(summary[key]) <= 100 for key in score_keys)


def test_full_pipeline_output_files() -> None:
    run_pipeline()
    expected_files = [
        get_path("scorecards") / "retrieval_accuracy_report.json",
        get_path("scorecards") / "answer_quality_report.json",
        get_path("scorecards") / "chunk_quality_summary.json",
        get_path("scorecards") / "rag_trust_summary.json",
    ]
    assert all(path.exists() for path in expected_files)
