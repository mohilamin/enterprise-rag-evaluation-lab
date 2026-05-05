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
        words = document.body.split()
        step = max(1, chunk_size - overlap)
        chunk_index = 0
        for start in range(0, len(words), step):
            chunk_words = words[start : start + chunk_size]
            if not chunk_words:
                continue
            rows.append(_chunk_row(document, chunk_index, " ".join(chunk_words)))
            chunk_index += 1
            if start + chunk_size >= len(words):
                break
    return pd.DataFrame(rows)


def save_chunks(chunks: pd.DataFrame) -> None:
    """Write chunk outputs for API, dashboard, and evaluation."""
    output_path = ensure_directory(get_path("chunks"))
    chunks.to_csv(output_path / "chunks.csv", index=False)
    (output_path / "chunks.json").write_text(
        json.dumps(chunks.to_dict("records"), indent=2),
        encoding="utf-8",
    )
    LOGGER.info("saved chunks", extra={"chunk_count": len(chunks)})


def _chunk_row(document: DocumentRecord, chunk_index: int, text: str) -> dict[str, object]:
    base = asdict(document)
    base.pop("body")
    base["chunk_id"] = f"{document.document_id}-CHUNK-{chunk_index:03d}"
    base["chunk_index"] = chunk_index
    base["text"] = text
    base["is_stale"] = is_stale(document.last_reviewed_date)
    base["has_sensitive_pattern"] = "123-45-6789" in text or "sk_test_" in text
    base["has_conflict_language"] = "conflict" in text.lower() or "conflicts" in text.lower()
    base["key_facts"] = "|".join(document.key_facts)
    base["related_controls"] = "|".join(document.related_controls)
    base["metadata_issues"] = "|".join(document.metadata_issues)
    return base
