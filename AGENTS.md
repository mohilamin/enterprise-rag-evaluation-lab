# AGENTS.md

You are building a production-style Data Engineering + AI/MLOps portfolio project.

Project name:
Enterprise Document Intelligence + RAG Evaluation Lab

Primary goal:
Build a realistic enterprise document intelligence system that ingests synthetic business documents, chunks them, indexes them, retrieves relevant evidence, generates citation-grounded answers, and evaluates RAG quality.

## Business Context

Large enterprises want to use GenAI, AI agents, semantic search, and document intelligence across internal knowledge. But a basic "chat with PDF" app is not acceptable for enterprise use.

Enterprise RAG systems need:
- reliable ingestion
- metadata
- chunking
- retrieval quality metrics
- citations
- answer groundedness
- stale-document detection
- sensitive-data controls
- hallucination-risk scoring
- reproducible evaluation evidence

This project must show how a data engineer / AI data engineer would build the foundation for a trustworthy enterprise RAG system.

## Core Outcome

The system should answer:

"Can this AI-generated answer be trusted, cited, evaluated, and safely used by a business user?"

## Build Principles

- Write clean, modular, production-style Python.
- Use Python 3.12.
- Use type hints.
- Use docstrings for public functions.
- Use structured logging.
- Add error handling.
- Use synthetic documents only.
- Do not use real sensitive data.
- Do not require a paid API key for the first working version.
- Keep the first implementation deterministic and locally runnable.
- Avoid unnecessary heavy dependencies in V0.1.
- Prefer a deterministic retrieval and answer-composition baseline first.
- Every answer must include citations or explicitly say evidence is insufficient.
- Every evaluation metric must be documented.
- Every major pipeline stage must have tests.
- Keep README updated after major changes.

## Required Architecture

The repo should contain these layers:

1. Synthetic document corpus generation
2. Document ingestion
3. Text normalization
4. Chunking
5. Metadata extraction
6. Retrieval index
7. RAG-style cited answer service
8. Evaluation dataset
9. Retrieval evaluation
10. Answer groundedness evaluation
11. Hallucination-risk scoring
12. Sensitive-data leakage checks
13. FastAPI service
14. Streamlit dashboard
15. Tests
16. Documentation
17. CI/CD
18. Docker

## Required Commands

Use these commands where possible:

pip install -r requirements.txt
python -m src.data_generation.generate_documents
python -m src.data_generation.generate_golden_questions
python -m src.pipeline.run_all
python -m pytest
python -m ruff check .
streamlit run src/dashboard/app.py
uvicorn src.api.main:app --reload
