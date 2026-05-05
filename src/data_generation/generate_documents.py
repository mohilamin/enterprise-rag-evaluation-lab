from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date

import pandas as pd

from src.common.config import get_path, get_settings
from src.common.logging import get_logger
from src.common.paths import ensure_directory

LOGGER = get_logger(__name__)


@dataclass(frozen=True)
class SyntheticDocument:
    document_id: str
    title: str
    department: str
    effective_date: str
    last_reviewed_date: str
    version: str
    owner: str
    confidentiality_level: str
    body: str
    key_facts: list[str]
    related_controls: list[str]


def _documents() -> list[SyntheticDocument]:
    return [
        SyntheticDocument(
            "DOC-HR-001",
            "Hybrid Work Eligibility Policy",
            "HR",
            "2025-01-15",
            "2026-02-01",
            "2.1",
            "HR Operations",
            "internal",
            "Employees may request hybrid work after 90 days of employment. Managers must "
            "review requests within five business days. Approved hybrid employees must work "
            "onsite at least two days per week and complete annual policy attestation.",
            ["Hybrid requests require 90 days tenure", "Managers respond within five days"],
            ["HR-CTRL-01", "HR-CTRL-04"],
        ),
        SyntheticDocument(
            "DOC-IT-001",
            "Privileged Access Security Policy",
            "IT Security",
            "2025-03-01",
            "2026-01-20",
            "3.0",
            "Security Governance",
            "restricted",
            "Privileged access requires multi-factor authentication, manager approval, and "
            "quarterly access review. Shared administrator accounts are prohibited. Emergency "
            "access must be revoked within 24 hours after incident closure.",
            ["Privileged access requires MFA", "Emergency access revoked within 24 hours"],
            ["SEC-CTRL-07", "SEC-CTRL-12"],
        ),
        SyntheticDocument(
            "DOC-VEN-001",
            "Vendor Data Processing Contract",
            "Legal",
            "2024-07-10",
            "2025-11-18",
            "1.4",
            "Commercial Legal",
            "confidential",
            "Vendors processing company data must encrypt data at rest and in transit. Vendors "
            "must notify the company within 48 hours of a confirmed data incident and retain "
            "audit evidence for seven years.",
            [
                "Vendor incident notice required within 48 hours",
                "Audit evidence retained seven years",
            ],
            ["VEN-CTRL-02", "PRIV-CTRL-08"],
        ),
        SyntheticDocument(
            "DOC-CLM-001",
            "Claims Handling Standard Operating Procedure",
            "Claims",
            "2025-04-05",
            "2026-03-10",
            "4.2",
            "Claims Excellence",
            "internal",
            "Claims above 25000 require senior adjuster review. Claim files must include loss "
            "summary, coverage decision, payment rationale, and customer communication log before "
            "closure.",
            ["Claims above 25000 require senior review", "Closure requires four evidence items"],
            ["CLM-CTRL-03", "CLM-CTRL-09"],
        ),
        SyntheticDocument(
            "DOC-FIN-001",
            "Monthly Finance Close Procedure",
            "Finance",
            "2025-02-01",
            "2026-01-05",
            "5.0",
            "Corporate Accounting",
            "internal",
            "Business units must submit accruals by business day three. Account reconciliations "
            "are due by business day five. Material variances above 100000 require controller "
            "approval and documented explanation.",
            ["Accruals due business day three", "Reconciliations due business day five"],
            ["FIN-CTRL-01", "FIN-CTRL-06"],
        ),
        SyntheticDocument(
            "DOC-DG-001",
            "Enterprise Data Governance Policy",
            "Data Governance",
            "2025-05-20",
            "2026-02-12",
            "2.5",
            "Chief Data Office",
            "internal",
            "Certified data products must have an owner, data dictionary, lineage record, quality "
            "score, and access classification. Data stewards review critical data elements every "
            "quarter.",
            [
                "Certified data products need owner and lineage",
                "Critical elements reviewed quarterly",
            ],
            ["DG-CTRL-01", "DG-CTRL-05"],
        ),
        SyntheticDocument(
            "DOC-SUP-001",
            "Customer Support Escalation Guide",
            "Customer Support",
            "2025-06-01",
            "2026-01-30",
            "1.8",
            "Support Operations",
            "internal",
            "Severity one customer escalations must be acknowledged within 15 minutes. Executive "
            "complaints require case owner assignment and daily status updates until closure.",
            [
                "Severity one acknowledged within 15 minutes",
                "Executive complaints need daily updates",
            ],
            ["SUP-CTRL-02", "SUP-CTRL-07"],
        ),
        SyntheticDocument(
            "DOC-IR-001",
            "Incident Response Playbook",
            "IT Security",
            "2023-01-01",
            "2023-02-01",
            "0.9",
            "Security Operations",
            "restricted",
            "Security incidents are triaged by severity. This deprecated procedure references "
            "LEGACY-IR-77. Critical incidents require commander assignment, evidence preservation, "
            "legal notification, and post-incident review.",
            [
                "Critical incidents require commander assignment",
                "References deprecated LEGACY-IR-77",
            ],
            ["IR-CTRL-01", "IR-CTRL-04"],
        ),
        SyntheticDocument(
            "DOC-PRO-001",
            "Procurement Approval Policy",
            "Procurement",
            "2025-02-15",
            "2026-02-15",
            "2.0",
            "",
            "internal",
            "Purchases above 50000 require sourcing review and finance approval. Sole-source "
            "purchases require documented business justification before purchase order release.",
            ["Purchases above 50000 require sourcing review", "Sole source needs justification"],
            ["PRO-CTRL-02", "FIN-CTRL-06"],
        ),
        SyntheticDocument(
            "DOC-AUD-001",
            "Audit Evidence Checklist",
            "Internal Audit",
            "",
            "2026-01-10",
            "1.2",
            "Internal Audit",
            "confidential",
            "Audit evidence must include source report name, extraction date, preparer, reviewer, "
            "control ID, and retention location. Evidence should not include synthetic SSN "
            "123-45-6789 or token sk_test_12345 in shared workpapers.",
            ["Audit evidence needs source and reviewer", "Contains sensitive-data-like strings"],
            ["AUD-CTRL-01", "PRIV-CTRL-02"],
        ),
        SyntheticDocument(
            "DOC-HR-002",
            "Hybrid Work Eligibility Policy Duplicate",
            "HR",
            "2025-01-15",
            "2026-02-01",
            "2.1",
            "HR Operations",
            "internal",
            "Employees may request hybrid work after 90 days of employment. Managers must "
            "review requests within five business days. Approved hybrid employees must work "
            "onsite at least two days per week and complete annual policy attestation.",
            ["Duplicate of hybrid policy", "Managers respond within five days"],
            ["HR-CTRL-01", "HR-CTRL-04"],
        ),
        SyntheticDocument(
            "DOC-CON-001",
            "Password Rotation Guidance Exception",
            "IT Security",
            "2025-08-01",
            "2026-01-01",
            "1.0",
            "Security Governance",
            "internal",
            "For standard users, passwords should not be rotated on a fixed schedule unless a "
            "credential is suspected to be compromised. This guidance conflicts with older "
            "training that required monthly password rotation.",
            ["Standard users should not rotate passwords monthly", "Conflicts with older training"],
            ["SEC-CTRL-05"],
        ),
        SyntheticDocument(
            "DOC-LOW-001",
            "Legacy Bulletin",
            "Operations",
            "2024-01-01",
            "2024-01-02",
            "0.1",
            "Operations",
            "internal",
            "Do the thing soon. Use judgment. Details pending.",
            ["Low-quality short document"],
            ["OPS-CTRL-00"],
        ),
    ]


def generate_documents() -> None:
    """Generate deterministic synthetic enterprise documents."""
    settings = get_settings()
    raw_path = ensure_directory(get_path("raw_documents"))
    documents = _documents()
    metadata_rows = []
    manifest = {
        "generated_at": date(2026, 5, 5).isoformat(),
        "random_seed": settings["random_seed"],
        "issues": [
            {"issue_type": "stale_policy_versions", "document_id": "DOC-IR-001"},
            {"issue_type": "conflicting_policy_guidance", "document_id": "DOC-CON-001"},
            {"issue_type": "missing_owner_metadata", "document_id": "DOC-PRO-001"},
            {"issue_type": "missing_effective_date", "document_id": "DOC-AUD-001"},
            {"issue_type": "sensitive_data_like_strings", "document_id": "DOC-AUD-001"},
            {"issue_type": "deprecated_procedure_references", "document_id": "DOC-IR-001"},
            {"issue_type": "duplicate_documents", "document_id": "DOC-HR-002"},
            {"issue_type": "low_quality_short_document", "document_id": "DOC-LOW-001"},
            {"issue_type": "ambiguous_wording", "document_id": "DOC-LOW-001"},
            {"issue_type": "no_answer_document_gap", "document_id": "DOC-GAP-001"},
        ],
    }

    for doc in documents:
        raw_path.joinpath(f"{doc.document_id}.md").write_text(
            _render_markdown(doc),
            encoding="utf-8",
        )
        row = asdict(doc)
        row.pop("body")
        row["key_facts"] = "|".join(doc.key_facts)
        row["related_controls"] = "|".join(doc.related_controls)
        row["file_name"] = f"{doc.document_id}.md"
        metadata_rows.append(row)

    pd.DataFrame(metadata_rows).to_csv(raw_path / "documents_metadata.csv", index=False)
    (raw_path / "injected_document_issue_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    LOGGER.info("synthetic document generation complete", extra={"document_count": len(documents)})


def _render_markdown(doc: SyntheticDocument) -> str:
    facts = "\n".join(f"- {fact}" for fact in doc.key_facts)
    controls = "\n".join(f"- {control}" for control in doc.related_controls)
    return (
        f"# {doc.title}\n\n"
        f"Document ID: {doc.document_id}\n"
        f"Department: {doc.department}\n"
        f"Version: {doc.version}\n\n"
        f"## Body\n\n{doc.body}\n\n"
        f"## Key Facts\n\n{facts}\n\n"
        f"## Related Controls\n\n{controls}\n"
    )


if __name__ == "__main__":
    generate_documents()
