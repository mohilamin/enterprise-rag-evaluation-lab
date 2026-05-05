from __future__ import annotations

from pathlib import Path

from src.dashboard.app import read_csv, read_json


def test_dashboard_read_csv_missing_file() -> None:
    assert read_csv(Path("missing-dashboard-file.csv")).empty


def test_dashboard_read_json_missing_file() -> None:
    assert read_json(Path("missing-dashboard-file.json")) == {}
