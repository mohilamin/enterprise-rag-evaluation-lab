# Technical Deep Dive

## Architecture Decisions

The project is split into explicit layers: generation, ingestion, chunking, retrieval, RAG answer composition, evaluation, API, dashboard, and tests. That keeps the V0.2 implementation small enough to run locally while still resembling an enterprise document intelligence platform.

Synthetic documents are used so the project can demonstrate sensitive-data controls and risk scoring without using real customer, employee, contract, or policy data.

## Why TF-IDF Was Used

V0.1 and V0.2 use scikit-learn TF-IDF with cosine similarity because it is deterministic, inspectable, free, and easy to run in CI. That makes evaluation evidence reproducible: the same golden questions produce the same retrieval reports across local runs.

This is not meant to outperform modern embeddings. It is a transparent baseline that makes retrieval quality measurable before introducing a model-dependent retrieval layer.

## Mapping to Embeddings and Vector Databases

In a real enterprise deployment, TF-IDF would likely be replaced or supplemented by:

- embedding models from OpenAI, Cohere, Voyage, or local sentence-transformer models
- vector stores such as Chroma, LanceDB, pgvector, Pinecone, Weaviate, or Milvus
- hybrid search with keyword plus vector retrieval
- metadata filters for department, confidentiality, version, effective dates, and jurisdiction
- reranking with cross-encoders or LLM-based evidence scoring

The golden question dataset and retrieval accuracy reports would still apply. Only the retrieval implementation would change.

## How Citation Validation Works

Every answerable answer is expected to include citations. Citation validation checks that:

- each citation includes `document_id` and `chunk_id`
- cited chunks came from retrieved results
- cited chunks exist in `data/chunks/chunks.csv`
- unanswerable questions do not pretend to cite evidence
- cited documents cover expected supporting documents where feasible

This creates audit-friendly evidence that an answer is tied to retrieved source chunks rather than invented text.

## How Hallucination Risk Is Calculated

The answer layer starts with a base risk from confidence and citation presence. Risk increases when:

- answerable questions have no citations
- unanswerable questions receive a fabricated answer
- cited documents do not match expected evidence
- retrieval misses expected documents
- stale, conflict, or sensitive-data warnings are expected but absent

The output includes `hallucination_risk_reasons` so reviewers can inspect why a score increased.

## Stale, Conflict, and Sensitive Risk Detection

Stale risk uses `last_reviewed_date` and the configured stale threshold. Chunks and answers carry stale warning flags when retrieved evidence is older than the threshold.

Conflict risk uses the injected issue manifest and conflict-language patterns in retrieved chunks. This is deterministic and explainable for a local V0.2 baseline.

Sensitive risk uses synthetic sensitive-data-like patterns such as fake SSNs, fake account numbers, fake tokens, and fake secrets. No real sensitive data is used.

## DuckDB and Local Outputs

DuckDB is used as a lightweight local analytical store for processed document and evaluation tables. It gives the project SQL-friendly outputs without requiring Snowflake, Databricks, BigQuery, or a local database server.

## What Would Change With LangChain, LlamaIndex, or OpenAI

LangChain or LlamaIndex could orchestrate loaders, chunkers, retrievers, tools, and agents. OpenAI or another LLM provider could replace the deterministic answer composer with generative answer synthesis.

The evaluation design would remain the same: golden questions, expected documents, citation validation, groundedness checks, risk warnings, and scorecards.

## What Would Change With Snowflake, Databricks, or Airflow

In an enterprise deployment:

- raw documents would land in object storage
- metadata and chunks would be stored in warehouse tables
- vector indexes would live in a managed vector database or lakehouse feature
- Airflow or Dagster would orchestrate scheduled ingestion and evaluation
- Snowflake or Databricks would host curated evaluation and audit tables
- access controls would enforce confidentiality and role-based retrieval
- observability would track drift, stale documents, and failed refreshes over time

## Current Limitations

- Synthetic corpus only.
- TF-IDF baseline instead of embeddings.
- Deterministic answer composer instead of an LLM.
- Basic local dashboard.
- No authentication or role-based access.
- No cloud deployment, managed orchestration, or enterprise secrets management yet.
