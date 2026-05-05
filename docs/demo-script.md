# Demo Script

## 0:00-0:30 - Business Problem

Explain that enterprise RAG is not just chat over PDFs. Business users need citations, retrieval metrics, stale-document warnings, sensitive-data controls, and evidence that answers are grounded.

## 0:30-1:00 - Generate Corpus

```bash
python -m src.data_generation.generate_documents
python -m src.data_generation.generate_golden_questions
```

Show `data/raw_documents/` and `data/evaluations/golden_questions.json`.

## 1:00-1:45 - Run Pipeline

```bash
python -m src.pipeline.run_all
```

Show `data/chunks/chunks.csv` and `data/index/retrieval_index_metadata.json`.

## 1:45-2:30 - Evaluation Evidence

Show:

- `data/evaluations/retrieval_evaluation.csv`
- `data/evaluations/answer_evaluation.csv`
- `data/scorecards/rag_trust_summary.json`

Explain Hit@K, MRR, citation coverage, groundedness, and risk scores.

## 2:30-3:00 - API and Dashboard

```bash
python -m uvicorn src.api.main:app --reload
python -m streamlit run src/dashboard/app.py
```

Show `/search`, `/answer`, and the Streamlit evaluation dashboard.
