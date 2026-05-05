# STAR Story

## Situation

Enterprise teams want GenAI assistants over internal documents, but answers become risky when retrieval is weak, citations are missing, documents are stale, or sensitive content leaks into prompts.

## Task

Build a document intelligence and RAG evaluation platform that can ingest enterprise-style documents, retrieve grounded evidence, generate cited answers, and measure trustworthiness.

## Action

Created deterministic synthetic documents, injected known document issues, generated golden questions, built ingestion and chunking layers, implemented TF-IDF retrieval, composed answers with citations, calculated RAG evaluation metrics, exposed results through FastAPI and Streamlit, and added tests, CI, and Docker.

## Result

Delivered a reproducible local project that demonstrates enterprise RAG foundations: retrieval metrics, citation coverage, groundedness, hallucination-risk scoring, stale-document warnings, sensitive-data warnings, and audit-friendly evidence.
