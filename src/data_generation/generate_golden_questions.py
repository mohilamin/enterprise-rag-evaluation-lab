from __future__ import annotations

import json
from itertools import cycle

from src.common.config import get_path
from src.common.logging import get_logger
from src.common.paths import ensure_directory

LOGGER = get_logger(__name__)


BASE_QUESTIONS = [
    (
        "Q001",
        "When may employees request hybrid work?",
        "answerable_one_document",
        ["DOC-HR-001"],
        ["90 days of employment"],
    ),
    (
        "Q002",
        "What controls are required for privileged access?",
        "answerable_one_document",
        ["DOC-IT-001"],
        ["multi-factor authentication", "manager approval", "quarterly access review"],
    ),
    (
        "Q003",
        "How quickly must vendors report a confirmed data incident?",
        "answerable_one_document",
        ["DOC-VEN-001"],
        ["48 hours"],
    ),
    (
        "Q004",
        "What claim files require senior adjuster review?",
        "answerable_one_document",
        ["DOC-CLM-001"],
        ["Claims above 25000"],
    ),
    (
        "Q005",
        "When are account reconciliations due?",
        "answerable_one_document",
        ["DOC-FIN-001"],
        ["business day five"],
    ),
    (
        "Q006",
        "What must certified data products include?",
        "answerable_one_document",
        ["DOC-DG-001"],
        ["owner", "data dictionary", "lineage record", "quality score"],
    ),
    (
        "Q007",
        "How quickly should severity one support escalations be acknowledged?",
        "answerable_one_document",
        ["DOC-SUP-001"],
        ["15 minutes"],
    ),
    (
        "Q008",
        "What is required for critical security incidents?",
        "stale_document_trap",
        ["DOC-IR-001"],
        ["commander assignment", "evidence preservation", "post-incident review"],
    ),
    (
        "Q009",
        "What approvals are required for purchases above 50000?",
        "answerable_one_document",
        ["DOC-PRO-001"],
        ["sourcing review", "finance approval"],
    ),
    (
        "Q010",
        "What fields must audit evidence include?",
        "sensitive_data_risk_question",
        ["DOC-AUD-001"],
        ["source report name", "extraction date", "preparer", "reviewer", "control ID"],
    ),
    (
        "Q011",
        "What is the company travel reimbursement meal limit?",
        "unanswerable",
        [],
        [],
    ),
    (
        "Q012",
        "Do password policies conflict on monthly rotation?",
        "conflict_detection_question",
        ["DOC-CON-001"],
        ["conflicts with older training", "should not be rotated on a fixed schedule"],
    ),
]


def generate_golden_questions() -> None:
    """Generate a deterministic golden evaluation set."""
    output_path = ensure_directory(get_path("evaluations"))
    questions = []
    type_cycle = cycle(
        [
            "answerable_with_one_document",
            "answerable_with_multiple_documents",
            "department_specific_policy_question",
        ]
    )
    for question_id, text, answer_type, docs, facts in BASE_QUESTIONS:
        questions.append(_question(question_id, text, answer_type, docs, facts))

    templates = [
        ("What evidence is needed before closing a claim?", ["DOC-CLM-001"], ["coverage decision"]),
        (
            "Which data governance reviews happen quarterly?",
            ["DOC-DG-001"],
            ["critical data elements"],
        ),
        ("What vendor evidence retention period is required?", ["DOC-VEN-001"], ["seven years"]),
        (
            "What is the executive complaint update cadence?",
            ["DOC-SUP-001"],
            ["daily status updates"],
        ),
        (
            "What documents discuss approval or review obligations?",
            ["DOC-FIN-001", "DOC-PRO-001"],
            ["approval"],
        ),
        (
            "Which security documents mention emergency or incident handling?",
            ["DOC-IT-001", "DOC-IR-001"],
            ["incident"],
        ),
    ]
    for index in range(13, 31):
        text, docs, facts = templates[(index - 13) % len(templates)]
        answer_type = next(type_cycle)
        questions.append(_question(f"Q{index:03d}", text, answer_type, docs, facts))

    (output_path / "golden_questions.json").write_text(
        json.dumps({"questions": questions}, indent=2),
        encoding="utf-8",
    )
    LOGGER.info("golden questions generated", extra={"question_count": len(questions)})


def _question(
    question_id: str,
    text: str,
    answer_type: str,
    document_ids: list[str],
    facts: list[str],
) -> dict[str, object]:
    return {
        "question_id": question_id,
        "question_text": text,
        "expected_answer_type": answer_type,
        "expected_document_ids": document_ids,
        "expected_facts": facts,
        "should_have_citation": bool(document_ids),
        "should_flag_stale": "stale" in answer_type or "DOC-IR-001" in document_ids,
        "should_flag_conflict": "conflict" in answer_type,
        "should_flag_sensitive_data": "sensitive" in answer_type or "DOC-AUD-001" in document_ids,
        "is_answerable": bool(document_ids),
    }


if __name__ == "__main__":
    generate_golden_questions()
