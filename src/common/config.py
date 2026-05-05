from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from src.common.paths import project_path


@lru_cache
def load_yaml(path: str) -> dict[str, Any]:
    """Load a YAML file from the repository."""
    with project_path(path).open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def get_settings() -> dict[str, Any]:
    """Return project settings."""
    return load_yaml("config/settings.yaml")


def get_path(name: str) -> Path:
    """Return a configured absolute project path."""
    configured = get_settings()["paths"][name]
    return project_path(configured)
