from __future__ import annotations

import json

from src.common.config import get_path
from src.data_generation.generate_documents import generate_documents
from src.data_generation.generate_golden_questions import generate_golden_questions


def test_synthetic_document_generation() -> None:
    generate_documents()
    metadata = get_path("raw_documents") / "documents_metadata.csv"
    assert metadata.exists()
    assert get_path("raw_documents").joinpath("DOC-HR-001.md").exists()


def test_injected_issue_manifest_creation() -> None:
    generate_documents()
    manifest = json.loads(
        get_path("raw_documents").joinpath("injected_document_issue_manifest.json").read_text()
    )
    assert len(manifest["issues"]) >= 10


def test_golden_question_generation() -> None:
    generate_golden_questions()
    questions = json.loads(get_path("evaluations").joinpath("golden_questions.json").read_text())
    assert len(questions["questions"]) >= 30


def test_golden_questions_include_unanswerable_case() -> None:
    generate_golden_questions()
    questions = json.loads(get_path("evaluations").joinpath("golden_questions.json").read_text())
    assert any(not question["is_answerable"] for question in questions["questions"])
