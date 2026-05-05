from __future__ import annotations

import json

from src.common.config import get_path
from src.common.logging import get_logger
from src.common.paths import ensure_directory

LOGGER = get_logger(__name__)


QUESTION_ROWS = [
    (
        "Q001",
        "When may employees request hybrid work?",
        "single_document_answerable",
        ["DOC-HR-001"],
        ["90 days of employment"],
    ),
    (
        "Q002",
        "What controls are required for privileged access?",
        "single_document_answerable",
        ["DOC-IT-001"],
        ["multi-factor authentication", "manager approval"],
    ),
    (
        "Q003",
        "How quickly must vendors report a confirmed data incident?",
        "single_document_answerable",
        ["DOC-VEN-001"],
        ["48 hours"],
    ),
    (
        "Q004",
        "What claim files require senior adjuster review?",
        "single_document_answerable",
        ["DOC-CLM-001"],
        ["Claims above 25000"],
    ),
    (
        "Q005",
        "When are account reconciliations due?",
        "single_document_answerable",
        ["DOC-FIN-001"],
        ["business day five"],
    ),
    (
        "Q006",
        "What must certified data products include?",
        "single_document_answerable",
        ["DOC-DG-001"],
        ["owner", "lineage record"],
    ),
    (
        "Q007",
        "How quickly should severity one support escalations be acknowledged?",
        "single_document_answerable",
        ["DOC-SUP-001"],
        ["15 minutes"],
    ),
    (
        "Q008",
        "What approvals are required for purchases above 50000?",
        "single_document_answerable",
        ["DOC-PRO-001"],
        ["sourcing review", "finance approval"],
    ),
    (
        "Q009",
        "What fields must audit evidence include?",
        "single_document_answerable",
        ["DOC-AUD-001"],
        ["source report name", "reviewer"],
    ),
    (
        "Q010",
        "What does the hybrid policy require for onsite work?",
        "single_document_answerable",
        ["DOC-HR-001"],
        ["two days per week"],
    ),
    (
        "Q011",
        "Which documents discuss approval or review obligations?",
        "multi_document_answerable",
        ["DOC-FIN-001", "DOC-PRO-001"],
        ["approval", "review"],
    ),
    (
        "Q012",
        "Which security documents mention emergency or incident handling?",
        "multi_document_answerable",
        ["DOC-IT-001", "DOC-IR-001"],
        ["emergency access", "critical incidents"],
    ),
    (
        "Q013",
        "Which documents describe evidence retention or evidence requirements?",
        "multi_document_answerable",
        ["DOC-VEN-001", "DOC-AUD-001"],
        ["audit evidence", "retention"],
    ),
    (
        "Q014",
        "Which documents mention owner or case owner accountability?",
        "multi_document_answerable",
        ["DOC-DG-001", "DOC-SUP-001"],
        ["owner", "case owner"],
    ),
    (
        "Q015",
        "Which documents require documented justification or explanation?",
        "multi_document_answerable",
        ["DOC-FIN-001", "DOC-PRO-001"],
        ["documented explanation", "business justification"],
    ),
    (
        "Q016",
        "Which documents relate to access classification or confidentiality?",
        "multi_document_answerable",
        ["DOC-DG-001", "DOC-IT-001"],
        ["access classification", "privileged access"],
    ),
    (
        "Q017",
        "Which documents discuss customer communication or complaints?",
        "multi_document_answerable",
        ["DOC-CLM-001", "DOC-SUP-001"],
        ["customer communication", "Executive complaints"],
    ),
    (
        "Q018",
        "Which documents include review cadence requirements?",
        "multi_document_answerable",
        ["DOC-IT-001", "DOC-DG-001"],
        ["quarterly access review", "review critical data elements"],
    ),
    ("Q019", "What is the company travel reimbursement meal limit?", "unanswerable", [], []),
    ("Q020", "What is the approved office furniture vendor list?", "unanswerable", [], []),
    ("Q021", "What is the maternity leave benefit length?", "unanswerable", [], []),
    ("Q022", "What is the corporate holiday calendar for 2027?", "unanswerable", [], []),
    ("Q023", "What is the standard laptop refresh budget?", "unanswerable", [], []),
    ("Q024", "What is the approved sales discount threshold?", "unanswerable", [], []),
    (
        "Q025",
        "What is required for critical security incidents?",
        "stale_document_trap",
        ["DOC-IR-001"],
        ["commander assignment", "post-incident review"],
    ),
    (
        "Q026",
        "Which incident playbook references a deprecated procedure?",
        "stale_document_trap",
        ["DOC-IR-001"],
        ["LEGACY-IR-77"],
    ),
    (
        "Q027",
        "What stale incident response document should be reviewed before use?",
        "stale_document_trap",
        ["DOC-IR-001"],
        ["Incident Response Playbook"],
    ),
    (
        "Q028",
        "What legal notification does the incident response playbook mention?",
        "stale_document_trap",
        ["DOC-IR-001"],
        ["legal notification"],
    ),
    (
        "Q029",
        "What evidence preservation steps appear in the stale incident playbook?",
        "stale_document_trap",
        ["DOC-IR-001"],
        ["evidence preservation"],
    ),
    (
        "Q030",
        "Do password policies conflict on monthly rotation?",
        "conflict_detection",
        ["DOC-CON-001"],
        ["conflicts with older training"],
    ),
    (
        "Q031",
        "Which guidance says fixed password rotation should not be used?",
        "conflict_detection",
        ["DOC-CON-001"],
        ["should not be rotated on a fixed schedule"],
    ),
    (
        "Q032",
        "What document conflicts with older password training?",
        "conflict_detection",
        ["DOC-CON-001"],
        ["Password Rotation Guidance Exception"],
    ),
    (
        "Q033",
        "What conflicting password guidance should security review?",
        "conflict_detection",
        ["DOC-CON-001"],
        ["monthly password rotation"],
    ),
    (
        "Q034",
        "Which IT Security document contains conflict language?",
        "conflict_detection",
        ["DOC-CON-001"],
        ["conflicts"],
    ),
    (
        "Q035",
        "Which audit document contains sensitive-data-like strings?",
        "sensitive_data_risk",
        ["DOC-AUD-001"],
        ["123-45-6789", "sk_test_12345"],
    ),
    (
        "Q036",
        "What sensitive synthetic token appears in audit evidence?",
        "sensitive_data_risk",
        ["DOC-AUD-001"],
        ["sk_test_12345"],
    ),
    (
        "Q037",
        "What fake SSN-like value appears in audit workpapers?",
        "sensitive_data_risk",
        ["DOC-AUD-001"],
        ["123-45-6789"],
    ),
    (
        "Q038",
        "What does the Data Governance department require for certified products?",
        "department_specific_policy",
        ["DOC-DG-001"],
        ["data dictionary", "lineage record"],
    ),
    (
        "Q039",
        "What does Customer Support require for executive complaints?",
        "department_specific_policy",
        ["DOC-SUP-001"],
        ["daily status updates"],
    ),
    (
        "Q040",
        "What does Finance require for material variances above 100000?",
        "department_specific_policy",
        ["DOC-FIN-001"],
        ["controller approval"],
    ),
]


def generate_golden_questions() -> None:
    """Generate a deterministic golden evaluation set with V0.2 distribution coverage."""
    output_path = ensure_directory(get_path("evaluations"))
    questions = [_question(*row) for row in QUESTION_ROWS]
    (output_path / "golden_questions.json").write_text(
        json.dumps({"questions": questions}, indent=2),
        encoding="utf-8",
    )
    LOGGER.info("golden questions generated", extra={"question_count": len(questions)})


def _question(
    question_id: str,
    text: str,
    question_type: str,
    document_ids: list[str],
    facts: list[str],
) -> dict[str, object]:
    return {
        "question_id": question_id,
        "question_text": text,
        "question_type": question_type,
        "expected_answer_type": question_type,
        "expected_document_ids": document_ids,
        "expected_facts": facts,
        "should_have_citation": bool(document_ids),
        "should_flag_stale": question_type == "stale_document_trap" or "DOC-IR-001" in document_ids,
        "should_flag_conflict": question_type == "conflict_detection",
        "should_flag_sensitive_data": (
            question_type == "sensitive_data_risk" or "DOC-AUD-001" in document_ids
        ),
        "is_answerable": bool(document_ids),
    }


if __name__ == "__main__":
    generate_golden_questions()
