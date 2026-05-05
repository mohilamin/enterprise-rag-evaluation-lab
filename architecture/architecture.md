# Architecture

The lab is a local production-style RAG evaluation system with inspectable layers:

1. Synthetic document generation creates enterprise-style markdown files and metadata.
2. Golden question generation creates deterministic evaluation cases.
3. Ingestion loads documents, validates metadata, and normalizes text.
4. Chunking creates stable chunk IDs and preserves document metadata.
5. Retrieval uses TF-IDF cosine similarity with simple metadata-aware reranking.
6. Answer composition creates citation-grounded responses or abstains when evidence is weak.
7. Evaluation calculates retrieval and answer trust metrics.
8. FastAPI and Streamlit expose the results for technical and business users.

V0.1 avoids paid APIs and external vector databases so reviewers can clone and run the project locally.
