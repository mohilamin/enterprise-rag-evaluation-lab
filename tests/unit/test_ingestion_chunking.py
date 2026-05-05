from __future__ import annotations

from src.chunking.chunker import chunk_documents
from src.data_generation.generate_documents import generate_documents
from src.ingestion.loaders import load_documents


def test_document_ingestion() -> None:
    generate_documents()
    documents = load_documents()
    assert len(documents) >= 10
    assert documents[0].document_id


def test_missing_metadata_detection() -> None:
    generate_documents()
    documents = load_documents()
    procurement = next(doc for doc in documents if doc.document_id == "DOC-PRO-001")
    assert "missing_owner" in procurement.metadata_issues


def test_chunk_creation() -> None:
    generate_documents()
    chunks = chunk_documents(load_documents())
    assert not chunks.empty
    assert {"chunk_id", "document_id", "text"}.issubset(chunks.columns)


def test_metadata_extraction_flags() -> None:
    generate_documents()
    chunks = chunk_documents(load_documents())
    audit = chunks.loc[chunks["document_id"] == "DOC-AUD-001"]
    assert bool(audit["has_sensitive_pattern"].any())
