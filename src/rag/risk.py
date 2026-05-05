from __future__ import annotations

import json

from src.common.config import get_path


def stale_warning(results: list[dict]) -> bool:
    """Return true if retrieved evidence contains stale documents."""
    return any(bool(result["metadata"].get("is_stale")) for result in results)


def conflict_warning(results: list[dict]) -> bool:
    """Return true if retrieved evidence maps to known conflicting document issues."""
    conflict_docs = _manifest_docs("conflicting_policy_guidance")
    return any(
        result["document_id"] in conflict_docs
        or bool(result["metadata"].get("has_conflict_language"))
        for result in results
    )


def sensitive_data_warning(results: list[dict]) -> bool:
    """Return true if retrieved evidence contains synthetic sensitive-data-like strings."""
    sensitive_docs = _manifest_docs("sensitive_data_like_strings")
    return any(
        result["document_id"] in sensitive_docs
        or bool(result["metadata"].get("has_sensitive_pattern"))
        for result in results
    )


def hallucination_risk(
    citations: list[dict],
    confidence_score: float,
    reasons: list[str] | None = None,
) -> float:
    """Estimate hallucination risk from confidence, citations, and explicit risk reasons."""
    reasons = reasons or []
    if not citations:
        return 100.0
    risk = max(0.0, 100.0 - confidence_score)
    risk += 10.0 * len(reasons)
    return round(min(100.0, risk), 2)


def _manifest_docs(issue_type: str) -> set[str]:
    path = get_path("raw_documents") / "injected_document_issue_manifest.json"
    if not path.exists():
        return set()
    manifest = json.loads(path.read_text(encoding="utf-8"))
    return {
        str(issue["document_id"])
        for issue in manifest.get("issues", [])
        if issue.get("issue_type") == issue_type
    }
