# Implementation Plan

## Phase 1 - Repository Foundation

Create a Python 3.12 project with deterministic local dependencies, Makefile commands, Docker files, GitHub Actions, configuration files, and the required folder structure.

## Phase 2 - Synthetic Corpus and Golden Questions

Generate synthetic enterprise documents across HR, IT security, legal, claims, finance, data governance, support, incident response, procurement, and audit. Record controlled document issues in an injected issue manifest. Generate at least 30 golden questions across answerable, unanswerable, stale, conflict, sensitive-data, and department-specific scenarios.

## Phase 3 - Ingestion, Normalization, and Chunking

Load document metadata and markdown files, normalize text, validate required metadata, split documents into deterministic chunks, preserve metadata, and write chunk outputs.

## Phase 4 - Retrieval and Answer Composition

Build a local TF-IDF retrieval baseline with cosine similarity and metadata-aware reranking. Compose deterministic answers using only retrieved evidence, with citations and risk warnings.

## Phase 5 - Evaluation and Scorecards

Evaluate retrieval using Hit@1, Hit@3, Hit@5, and MRR. Evaluate answers using citation coverage, groundedness, hallucination risk, stale-document risk, sensitive-data risk, answerability accuracy, and an overall RAG trust score.

## Phase 6 - API, Dashboard, and Tests

Expose generated outputs through FastAPI and a Streamlit dashboard. Add pytest coverage for generation, ingestion, chunking, retrieval, answers, metrics, pipeline, and API endpoints.
