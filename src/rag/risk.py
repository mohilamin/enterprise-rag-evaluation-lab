from __future__ import annotations


def stale_warning(results: list[dict]) -> bool:
    """Return true if retrieved evidence contains stale documents."""
    return any(bool(result["metadata"].get("is_stale")) for result in results)


def conflict_warning(results: list[dict]) -> bool:
    """Return true if retrieved evidence contains conflict language."""
    return any(bool(result["metadata"].get("has_conflict_language")) for result in results)


def sensitive_data_warning(results: list[dict]) -> bool:
    """Return true if retrieved evidence contains sensitive-data-like strings."""
    return any(bool(result["metadata"].get("has_sensitive_pattern")) for result in results)


def hallucination_risk(citations: list[dict], confidence_score: float) -> float:
    """Estimate hallucination risk from missing citations and low confidence."""
    if not citations:
        return 100.0
    return round(max(0.0, 100.0 - confidence_score), 2)
