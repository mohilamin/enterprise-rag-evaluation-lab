# Three-Minute Demo Script

## 0:00-0:30 - Business Problem

Open with the point: enterprise RAG is not just chat over files. A business user needs to know whether the assistant retrieved the right document, cited evidence, avoided stale policies, and refused questions the corpus cannot answer.

Say: "This project evaluates whether a RAG answer can be trusted, cited, audited, and safely used by a business user or AI agent."

## 0:30-1:00 - Synthetic Corpus and Golden Questions

Run:

```bash
python -m src.data_generation.generate_documents
python -m src.data_generation.generate_golden_questions
```

Show:

- `data/raw_documents/`
- `data/raw_documents/injected_document_issue_manifest.json`
- `data/evaluations/golden_questions.json`

Explain that the corpus includes HR, IT security, vendor contract, claims, finance, data governance, support, incident response, procurement, and audit documents. The golden set has 40 questions with expected document IDs and risk flags.

## 1:00-1:45 - Retrieval and Cited Answers

Run:

```bash
python -m src.pipeline.run_all
```

Show:

- `data/chunks/chunks.csv`
- `data/index/retrieval_index_metadata.json`
- `POST /search`
- `POST /answer`

Explain that retrieval uses deterministic TF-IDF so evaluation is reproducible. The answer composer only uses retrieved chunks, cites evidence, and returns "Insufficient evidence in retrieved documents" when support is weak.

## 1:45-2:30 - Evaluation Reports

Show:

- `data/scorecards/retrieval_accuracy_report.json`
- `data/scorecards/answer_quality_report.json`
- `data/scorecards/chunk_quality_summary.json`
- `data/scorecards/rag_trust_summary.json`

Call out:

- Hit@1, Hit@3, Hit@5, and MRR for retrieval quality.
- Citation coverage and groundedness for answer evidence.
- Hallucination-risk reasons for auditability.
- Stale, conflict, and sensitive-data warning accuracy.

## 2:30-3:00 - Dashboard/API and Business Value

Launch:

```bash
python -m uvicorn src.api.main:app --reload
python -m streamlit run src/dashboard/app.py
```

Show the dashboard sections:

- Executive Overview
- Retrieval Metrics
- Answer Quality Metrics
- Hallucination Risk
- Golden Question Result Explorer
- Search Lab
- Example Answer With Citations

Close with: "The value is not that this is the most advanced RAG system. The value is that it makes RAG quality measurable, explainable, and reviewable before a company scales AI assistants."
