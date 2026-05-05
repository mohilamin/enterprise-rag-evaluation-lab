# Release Notes

## V0.1 Working Baseline

- Created the first local RAG evaluation lab.
- Added synthetic enterprise document generation.
- Added golden question generation.
- Implemented ingestion, normalization, chunking, TF-IDF retrieval, deterministic answer composition, evaluation metrics, API, dashboard, tests, Docker, and CI.
- Published the working baseline at commit `3afa640`.

## V0.2 Evaluation Hardening

- Expanded the golden question set to 40 questions with required distribution by question type.
- Added retrieval accuracy reports in JSON and CSV.
- Added answer quality reports in JSON and CSV.
- Added chunk quality reporting for metadata, stale chunks, sensitive chunks, and empty chunks.
- Improved enterprise realism in generated document sections.
- Added citation validation against retrieved chunks and expected supporting documents.
- Added hallucination-risk reasons for more explainable answer auditing.
- Improved stale, conflict, and sensitive-data warning logic.
- Improved API responses for demo-ready search, answer, scorecard, and trust-summary outputs.
- Improved Streamlit dashboard sections for retrieval metrics, answer quality, risks, golden question exploration, and example cited answers.
- Expanded tests to cover V0.2 reports, citation validation, API schemas, dashboard data loading, and pipeline outputs.
- Updated README, metrics, sample outputs, recruiter summary, technical deep dive, and LinkedIn draft documentation.
