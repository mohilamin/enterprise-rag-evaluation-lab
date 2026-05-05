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

## V0.3 Showcase Polish

- Reframed the README for public portfolio review with first-screen business context, proof points, architecture, quickstart, evidence outputs, and recruiter-friendly positioning.
- Added a cleaner Mermaid architecture diagram focused on the RAG evaluation flow from synthetic documents to API/dashboard.
- Added screenshot instruction docs for executive overview, search lab, answer with citations, RAG evaluation metrics, hallucination risk, and golden question results.
- Reworked the demo script into a timed three-minute walkthrough.
- Added GitHub profile setup guidance with repo description, topics, pinned repo blurb, and README headline.
- Polished LinkedIn draft versions for recruiter and technical data engineering/MLOps audiences.
- Preserved the existing working code path while improving public presentation and demo readiness.
