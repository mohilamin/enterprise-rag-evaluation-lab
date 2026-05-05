from __future__ import annotations

import json

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from src.common.config import get_path
from src.common.logging import get_logger
from src.common.paths import ensure_directory

LOGGER = get_logger(__name__)


def build_retrieval_index(chunks: pd.DataFrame) -> dict[str, object]:
    """Build a deterministic TF-IDF index summary."""
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(chunks["text"].fillna(""))
    metadata = {
        "index_type": "tfidf_cosine",
        "chunk_count": int(len(chunks)),
        "vocabulary_size": int(len(vectorizer.vocabulary_)),
    }
    output_path = ensure_directory(get_path("index"))
    (output_path / "retrieval_index_metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )
    LOGGER.info("built retrieval index", extra=metadata)
    return {"vectorizer": vectorizer, "matrix": matrix, "metadata": metadata}
