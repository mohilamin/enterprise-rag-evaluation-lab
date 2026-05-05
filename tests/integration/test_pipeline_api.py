from __future__ import annotations

from fastapi.testclient import TestClient

from src.api.main import app
from src.common.config import get_path
from src.pipeline.run_all import run_pipeline


def test_full_pipeline_execution() -> None:
    run_pipeline()
    assert get_path("scorecards").joinpath("rag_trust_summary.json").exists()


def test_evaluation_outputs_exist() -> None:
    run_pipeline()
    assert get_path("evaluations").joinpath("retrieval_evaluation.csv").exists()
    assert get_path("evaluations").joinpath("answer_evaluation.csv").exists()


def test_duckdb_output_exists() -> None:
    run_pipeline()
    assert get_path("processed").joinpath("rag_evaluation_lab.duckdb").exists()


def test_api_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_api_search_endpoint() -> None:
    run_pipeline()
    client = TestClient(app)
    response = client.post("/search", json={"query": "privileged access controls", "top_k": 3})
    assert response.status_code == 200
    assert isinstance(response.json()["results"], list)


def test_api_answer_endpoint() -> None:
    run_pipeline()
    client = TestClient(app)
    response = client.post(
        "/answer",
        json={"question": "How quickly must vendors report a confirmed data incident?", "top_k": 3},
    )
    assert response.status_code == 200
    assert "citations" in response.json()


def test_api_rag_trust_summary_endpoint() -> None:
    run_pipeline()
    client = TestClient(app)
    response = client.get("/rag-trust-summary")
    assert response.status_code == 200
    assert "overall_rag_trust_score" in response.json()


def test_api_scorecards_endpoint() -> None:
    run_pipeline()
    client = TestClient(app)
    response = client.get("/scorecards")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_search_schema() -> None:
    run_pipeline()
    client = TestClient(app)
    response = client.post("/search", json={"query": "audit evidence", "top_k": 2})
    payload = response.json()
    assert {"query", "top_k", "results"}.issubset(payload)
    assert {"rank", "document_id", "chunk_id", "title", "score", "snippet"}.issubset(
        payload["results"][0]
    )


def test_api_answer_schema() -> None:
    run_pipeline()
    client = TestClient(app)
    response = client.post("/answer", json={"question": "What fields must audit evidence include?"})
    payload = response.json()
    assert "hallucination_risk_reasons" in payload
    assert "sensitive_data_warning" in payload
