from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.common.config import get_path
from src.common.logging import get_logger
from src.ingestion.normalizer import normalize_text

LOGGER = get_logger(__name__)
REQUIRED_METADATA = [
    "document_id",
    "title",
    "department",
    "effective_date",
    "last_reviewed_date",
    "version",
    "owner",
    "confidentiality_level",
    "file_name",
]


@dataclass(frozen=True)
class DocumentRecord:
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
    metadata_issues: list[str]


def load_documents(raw_path: Path | None = None) -> list[DocumentRecord]:
    """Load raw markdown documents and metadata."""
    raw_path = raw_path or get_path("raw_documents")
    metadata_path = raw_path / "documents_metadata.csv"
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing metadata file: {metadata_path}")
    metadata = pd.read_csv(metadata_path, keep_default_na=False)
    missing_columns = sorted(set(REQUIRED_METADATA) - set(metadata.columns))
    if missing_columns:
        raise ValueError(f"Missing metadata columns: {missing_columns}")

    records = []
    for row in metadata.to_dict("records"):
        file_path = raw_path / str(row["file_name"])
        if not file_path.exists():
            raise FileNotFoundError(f"Missing document file: {file_path}")
        issues = _metadata_issues(row)
        records.append(
            DocumentRecord(
                document_id=str(row["document_id"]),
                title=str(row["title"]),
                department=str(row["department"]),
                effective_date=str(row["effective_date"]),
                last_reviewed_date=str(row["last_reviewed_date"]),
                version=str(row["version"]),
                owner=str(row["owner"]),
                confidentiality_level=str(row["confidentiality_level"]),
                body=normalize_text(file_path.read_text(encoding="utf-8")),
                key_facts=_split_list(row.get("key_facts", "")),
                related_controls=_split_list(row.get("related_controls", "")),
                metadata_issues=issues,
            )
        )
    LOGGER.info("loaded documents", extra={"document_count": len(records)})
    return records


def _split_list(value: object) -> list[str]:
    return [item.strip() for item in str(value).split("|") if item.strip()]


def _metadata_issues(row: dict[str, object]) -> list[str]:
    issues = []
    for field in REQUIRED_METADATA:
        if not str(row.get(field, "")).strip():
            issues.append(f"missing_{field}")
    return issues
