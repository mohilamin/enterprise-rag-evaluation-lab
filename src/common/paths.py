from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def project_path(*parts: str) -> Path:
    """Return an absolute path inside the repository."""
    return PROJECT_ROOT.joinpath(*parts)


def ensure_directory(path: Path) -> Path:
    """Create a directory if needed and return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path
