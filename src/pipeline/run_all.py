from __future__ import annotations

import duckdb

from src.chunking.chunker import chunk_documents, save_chunks
from src.common.config import get_path
from src.common.logging import get_logger
from src.common.paths import ensure_directory
from src.data_generation.generate_documents import generate_documents
from src.data_generation.generate_golden_questions import generate_golden_questions
from src.evaluation.evaluator import run_evaluation
from src.ingestion.loaders import load_documents
from src.retrieval.index import build_retrieval_index

LOGGER = get_logger(__name__)


def run_pipeline() -> None:
    """Run the end-to-end local RAG evaluation pipeline."""
    generate_documents()
    generate_golden_questions()
    documents = load_documents()
    chunks = chunk_documents(documents)
    save_chunks(chunks)
    build_retrieval_index(chunks)
    _build_duckdb()
    run_evaluation()
    LOGGER.info("pipeline complete")


def _build_duckdb() -> None:
    processed_path = ensure_directory(get_path("processed"))
    db_path = processed_path / "rag_evaluation_lab.duckdb"
    chunks_path = get_path("chunks") / "chunks.csv"
    with duckdb.connect(str(db_path)) as connection:
        connection.execute(
            "CREATE OR REPLACE TABLE chunks AS SELECT * FROM read_csv_auto(?)",
            [str(chunks_path)],
        )
        connection.execute(
            """
            CREATE OR REPLACE TABLE corpus_health AS
            SELECT
                department,
                count(DISTINCT document_id) AS document_count,
                count(*) AS chunk_count
            FROM chunks
            GROUP BY department
            """
        )


if __name__ == "__main__":
    run_pipeline()
