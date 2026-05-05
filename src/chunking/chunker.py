from __future__ import annotations

import json
from dataclasses import asdict

import pandas as pd

from src.chunking.metadata import is_stale
from src.common.config import get_path, get_settings
from src.common.logging import get_logger
from src.common.paths import ensure_directory
from src.ingestion.loaders import DocumentRecord

LOGGER = get_logger(__name__)


def chunk_documents(documents: list[DocumentRecord]) -> pd.DataFrame:
    """Split documents into deterministic word chunks with inherited metadata."""
    settings = get_settings()["chunking"]
    chunk_size = int(settings["chunk_size_words"])
    overlap = int(settings["chunk_overlap_words"])
    rows: list[dict[str, object]] = []
    for document in documents:
        chunk_index = 0
        for section_heading, section_text in _sections(document.body):
            words = section_text.split()
            step = max(1, chunk_size - overlap)
            for start in range(0, len(words), step):
                chunk_words = words[start : start + chunk_size]
                if not chunk_words:
                    continue
                rows.append(
                    _chunk_row(document, chunk_index, " ".join(chunk_words), section_heading)
                )
                chunk_index += 1
                if start + chunk_size >= len(words):
                    break
    return pd.DataFrame(rows)


def save_chunks(chunks: pd.DataFrame) -> None:
    """Write chunk outputs and chunk quality evidence."""
    output_path = ensure_directory(get_path("chunks"))
    chunks.to_csv(output_path / "chunks.csv", index=False)
    (output_path / "chunks.json").write_text(
        json.dumps(chunks.to_dict("records"), indent=2),
        encoding="utf-8",
    )
    write_chunk_quality_report(chunks)
    LOGGER.info("saved chunks", extra={"chunk_count": len(chunks)})


def write_chunk_quality_report(chunks: pd.DataFrame) -> dict[str, object]:
    """Write chunk quality report and summary scorecard."""
    scorecard_path = ensure_directory(get_path("scorecards"))
    metadata_fields = [
        "document_id",
        "title",
        "department",
        "version",
        "owner",
        "effective_date",
        "last_reviewed_date",
        "confidentiality_level",
        "section_heading",
    ]
    report = chunks.copy()
    report["missing_metadata_count"] = report[metadata_fields].eq("").sum(axis=1)
    report["chunk_quality_pass"] = (
        (report["token_or_word_count"] > 0) & (report["missing_metadata_count"] == 0)
    )
    summary = {
        "total_chunks": int(len(report)),
        "average_chunk_length": round(float(report["token_or_word_count"].mean()), 2),
        "empty_chunks": int((report["token_or_word_count"] == 0).sum()),
        "chunks_missing_metadata": int((report["missing_metadata_count"] > 0).sum()),
        "stale_chunks": int(report["stale_flag"].sum()),
        "sensitive_chunks": int(report["sensitive_data_flag"].sum()),
    }
    report.to_csv(scorecard_path / "chunk_quality_report.csv", index=False)
    (scorecard_path / "chunk_quality_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    return summary


def _sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_heading = "Document Header"
    current_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current_lines:
                sections.append((current_heading, "\n".join(current_lines).strip()))
            current_heading = line.replace("## ", "").strip()
            current_lines = []
        elif line.startswith("# "):
            continue
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_heading, "\n".join(current_lines).strip()))
    return [(heading, body) for heading, body in sections if body]


def _chunk_row(
    document: DocumentRecord,
    chunk_index: int,
    text: str,
    section_heading: str,
) -> dict[str, object]:
    base = asdict(document)
    base.pop("body")
    base["chunk_id"] = f"{document.document_id}-CHUNK-{chunk_index:03d}"
    base["chunk_index"] = chunk_index
    base["text"] = text
    base["token_or_word_count"] = len(text.split())
    base["section_heading"] = section_heading
    base["stale_flag"] = is_stale(document.last_reviewed_date)
    base["sensitive_data_flag"] = _has_sensitive_pattern(text)
    base["is_stale"] = base["stale_flag"]
    base["has_sensitive_pattern"] = base["sensitive_data_flag"]
    base["has_conflict_language"] = "conflict" in text.lower() or "conflicts" in text.lower()
    base["key_facts"] = "|".join(document.key_facts)
    base["related_controls"] = "|".join(document.related_controls)
    base["metadata_issues"] = "|".join(document.metadata_issues)
    return base


def _has_sensitive_pattern(text: str) -> bool:
    lowered = text.lower()
    return (
        "123-45-6789" in lowered
        or "sk_test_" in lowered
        or "acct-" in lowered
        or "secret" in lowered
    )
