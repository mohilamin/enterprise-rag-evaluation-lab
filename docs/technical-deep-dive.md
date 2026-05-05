# Technical Deep Dive

## Retrieval Baseline

V0.1 uses scikit-learn TF-IDF vectors and cosine similarity. This keeps the system deterministic and free of paid API dependencies.

## Reranking

Reranking adds small metadata adjustments for freshness, department match, and title keyword overlap. This demonstrates how enterprise retrieval often blends vector relevance with governance metadata.

## Answer Composition

The answer layer only uses retrieved chunks. It includes citations, abstains when evidence is weak, and returns stale, conflict, and sensitive-data warnings.

## Evaluation

Golden questions define expected supporting documents and risk flags. The evaluator calculates Hit@K, MRR, citation coverage, groundedness, hallucination risk, stale-document risk, sensitive-data risk, answerability accuracy, and an overall RAG trust score.

## Enterprise Scaling Path

- Replace local files with object storage.
- Replace DuckDB with Snowflake, Databricks, or BigQuery.
- Replace TF-IDF with a vector database such as ChromaDB, LanceDB, Pinecone, or pgvector.
- Add Airflow or Dagster orchestration.
- Add MLflow evaluation tracking.
- Add access controls and prompt logging.
- Add OpenLineage for data and document lineage.
