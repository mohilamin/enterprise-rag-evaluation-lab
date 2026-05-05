from __future__ import annotations

from datetime import date

import pandas as pd

from src.common.config import get_settings


def is_stale(last_reviewed_date: str) -> bool:
    """Return whether a document is stale under configured freshness rules."""
    if not last_reviewed_date:
        return True
    reviewed = pd.to_datetime(last_reviewed_date, errors="coerce")
    if pd.isna(reviewed):
        return True
    threshold = get_settings()["freshness"]["stale_document_threshold_days"]
    return (pd.Timestamp(date(2026, 5, 5)) - reviewed).days > threshold


def metadata_flags(row: dict[str, object]) -> dict[str, bool]:
    """Infer retrieval and risk flags from chunk metadata."""
    text = str(row.get("text", ""))
    return {
        "is_stale": is_stale(str(row.get("last_reviewed_date", ""))),
        "has_sensitive_pattern": "123-45-6789" in text or "sk_test_" in text,
        "has_conflict_language": "conflict" in text.lower() or "conflicts" in text.lower(),
    }
