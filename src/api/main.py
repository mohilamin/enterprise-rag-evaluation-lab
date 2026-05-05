from __future__ import annotations

import json

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from src.common.config import get_path
from src.rag.answer import answer_question
from src.retrieval.search import search

app = FastAPI(title="Enterprise RAG Evaluation Lab")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class AnswerRequest(BaseModel):
    question: str
    top_k: int = 5


def _csv_records(path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    return pd.read_csv(path).fillna("").to_dict("records")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "enterprise-rag-evaluation-lab"}


@app.get("/documents")
def documents() -> list[dict[str, object]]:
    return _csv_records(get_path("raw_documents") / "documents_metadata.csv")


@app.get("/chunks")
def chunks() -> list[dict[str, object]]:
    return _csv_records(get_path("chunks") / "chunks.csv")


@app.post("/search")
def search_endpoint(request: QueryRequest) -> list[dict]:
    return search(request.query, top_k=request.top_k)


@app.post("/answer")
def answer_endpoint(request: AnswerRequest) -> dict[str, object]:
    return answer_question(request.question, top_k=request.top_k)


@app.get("/evaluations")
def evaluations() -> dict[str, list[dict[str, object]]]:
    return {
        "retrieval": _csv_records(get_path("evaluations") / "retrieval_evaluation.csv"),
        "answer": _csv_records(get_path("evaluations") / "answer_evaluation.csv"),
    }


@app.get("/scorecards")
def scorecards() -> list[dict[str, object]]:
    return _csv_records(get_path("scorecards") / "rag_trust_scorecard.csv")


@app.get("/rag-trust-summary")
def rag_trust_summary() -> dict[str, object]:
    path = get_path("scorecards") / "rag_trust_summary.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))
