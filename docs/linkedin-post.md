# LinkedIn Post Drafts

Status: DRAFT

## Version A: Recruiter-Friendly

I built an Enterprise Document Intelligence + RAG Evaluation Lab as a portfolio project.

The goal was to go beyond a generic "chat with PDF" demo. In real companies, AI assistants need more than a plausible answer. They need retrieval quality, citations, stale-document warnings, sensitive-data controls, hallucination-risk scoring, and repeatable evaluation evidence.

What I built:

- synthetic enterprise document corpus
- golden question evaluation set
- document ingestion, chunking, and metadata checks
- deterministic retrieval baseline
- cited answer service
- citation validation
- retrieval accuracy and answer quality reports
- FastAPI endpoints and Streamlit dashboard
- pytest, Ruff, Docker, and GitHub Actions

Current V0.2 evidence includes 40 golden questions, retrieval accuracy reports, answer quality reports, hallucination-risk reasons, and 44 passing tests.

Tech stack: Python 3.12, pandas, scikit-learn, DuckDB, FastAPI, Streamlit, pytest, Ruff, Docker.

GitHub: [link placeholder]

Screenshot: [screenshot placeholder]

## Version B: Technical Data Engineering / MLOps

I hardened my Enterprise Document Intelligence + RAG Evaluation Lab into a V0.2 evaluation-focused release.

This is not a generic chat-with-PDF app. The project focuses on the evidence layer enterprise RAG systems need before business users or AI agents can rely on answers.

V0.2 adds:

- 40 deterministic golden questions with expected source documents and risk flags
- retrieval accuracy reports with Hit@1, Hit@3, Hit@5, MRR, misses, and pass/fail by question
- answer quality reports with answerability accuracy, citation coverage, groundedness, stale/conflict/sensitive warning accuracy, and hallucination-risk reasons
- citation validation against retrieved chunks and expected supporting documents
- chunk quality reporting for metadata completeness, stale chunks, sensitive chunks, and empty chunks
- API responses designed for demos and scorecard inspection
- expanded tests, now 44 passing locally

The system uses a transparent TF-IDF baseline so results are reproducible without paid APIs. In a real deployment, the same evaluation design could wrap embeddings, vector databases, LangChain/LlamaIndex, Snowflake, Databricks, Airflow, or MLflow.

Tech stack: Python 3.12, pandas, scikit-learn, DuckDB, FastAPI, Streamlit, pytest, Ruff, Docker.

GitHub: [link placeholder]

Screenshot: [screenshot placeholder]
