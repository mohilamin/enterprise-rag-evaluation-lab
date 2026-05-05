from __future__ import annotations

from src.chunking.chunker import chunk_documents, save_chunks
from src.data_generation.generate_documents import generate_documents
from src.ingestion.loaders import load_documents
from src.rag.answer import INSUFFICIENT, answer_question
from src.retrieval.index import build_retrieval_index
from src.retrieval.search import search


def _prepare() -> None:
    generate_documents()
    chunks = chunk_documents(load_documents())
    save_chunks(chunks)
    build_retrieval_index(chunks)


def test_retrieval_index_creation() -> None:
    generate_documents()
    chunks = chunk_documents(load_documents())
    metadata = build_retrieval_index(chunks)["metadata"]
    assert metadata["chunk_count"] == len(chunks)


def test_search_returns_ranked_results() -> None:
    _prepare()
    results = search("What controls are required for privileged access?")
    assert results
    assert results[0]["rank"] == 1


def test_answer_includes_citations() -> None:
    _prepare()
    answer = answer_question("How quickly must vendors report a confirmed data incident?")
    assert answer["citations"]


def test_insufficient_evidence_handling() -> None:
    _prepare()
    answer = answer_question("What is the company travel reimbursement meal limit?")
    assert str(answer["answer_text"]).startswith(INSUFFICIENT)


def test_stale_document_warning() -> None:
    _prepare()
    answer = answer_question("What is required for critical security incidents?")
    assert answer["stale_document_warning"] is True


def test_conflict_warning() -> None:
    _prepare()
    answer = answer_question("Do password policies conflict on monthly rotation?")
    assert answer["conflict_warning"] is True


def test_sensitive_data_warning() -> None:
    _prepare()
    answer = answer_question("What fields must audit evidence include?")
    assert answer["sensitive_data_warning"] is True
