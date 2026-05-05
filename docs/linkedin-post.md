# LinkedIn Post Drafts

Status: DRAFT

## Version A: Recruiter-Friendly

I built an Enterprise Document Intelligence + RAG Evaluation Lab as a portfolio project.

This is not a generic "chat with PDF" demo. The project focuses on a problem companies actually face: can an AI assistant answer from internal documents in a way that is trusted, cited, evaluated, and safe for business use?

What it includes:

- synthetic enterprise documents
- golden evaluation questions
- retrieval index and cited answer service
- citation validation
- retrieval accuracy reports
- answer quality reports
- hallucination-risk reasons
- stale/conflict/sensitive-data warning checks
- FastAPI endpoints and Streamlit dashboard
- 44 passing tests, Ruff, Docker, and GitHub Actions

Tech stack: Python 3.12, pandas, scikit-learn, DuckDB, FastAPI, Streamlit, pytest, Ruff, Docker.

What this project proves: I can build the evaluation and evidence layer around enterprise GenAI systems, not just a chatbot UI.

GitHub: [link placeholder]

Screenshot: [screenshot placeholder]

## Version B: Technical Data Engineering / MLOps Audience

I created an Enterprise Document Intelligence + RAG Evaluation Lab to demonstrate the evaluation layer around enterprise RAG.

The core idea: RAG quality should be measurable. Retrieval misses, missing citations, stale policy context, sensitive-data-like strings, and unsupported answers should show up in evidence files before a system reaches business users.

The project includes:

- deterministic synthetic document corpus across HR, IT security, claims, finance, audit, support, procurement, and governance
- 40-question golden evaluation set with expected document IDs and risk flags
- TF-IDF retrieval baseline for reproducible local evaluation
- citation-grounded deterministic answer composer
- citation validation against retrieved chunks and expected supporting documents
- retrieval accuracy reports with Hit@1, Hit@3, Hit@5, MRR, misses, and pass/fail by question
- answer quality reports with answerability accuracy, citation coverage, groundedness, stale/conflict/sensitive warning accuracy, and hallucination-risk reasons
- chunk quality reports for metadata completeness, stale chunks, sensitive chunks, and empty chunks
- FastAPI, Streamlit, pytest, Ruff, Docker, and CI

Current validation: 44 tests passing and Ruff clean.

This is intentionally a transparent baseline. In a real deployment, the same evaluation framework could wrap embeddings, vector databases, LangChain/LlamaIndex, OpenAI APIs, Snowflake, Databricks, Airflow, or MLflow.

GitHub: [link placeholder]

Screenshot: [screenshot placeholder]
