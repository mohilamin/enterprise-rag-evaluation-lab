from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.common.config import get_path
from src.rag.answer import answer_question
from src.retrieval.search import search


def read_csv(path: Path) -> pd.DataFrame:
    """Read a CSV for dashboard use, returning an empty frame if missing."""
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def read_json(path: Path) -> dict[str, object]:
    """Read a JSON object for dashboard use, returning an empty dict if missing."""
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    st.set_page_config(page_title="Enterprise RAG Evaluation Lab", layout="wide")
    st.title("Enterprise Document Intelligence + RAG Evaluation Lab")

    scorecards = get_path("scorecards")
    summary = read_json(scorecards / "rag_trust_summary.json")
    retrieval_report = read_json(scorecards / "retrieval_accuracy_report.json")
    answer_report = read_json(scorecards / "answer_quality_report.json")
    chunk_summary = read_json(scorecards / "chunk_quality_summary.json")
    documents = read_csv(get_path("raw_documents") / "documents_metadata.csv")
    chunks = read_csv(get_path("chunks") / "chunks.csv")
    retrieval_eval = read_csv(scorecards / "retrieval_accuracy_report.csv")
    answer_eval = read_csv(scorecards / "answer_quality_report.csv")

    st.header("Executive Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("RAG Trust Score", summary.get("overall_rag_trust_score", "Run pipeline"))
    col2.metric("Hit@3", summary.get("hit_at_3", "Run pipeline"))
    col3.metric("Answerability", summary.get("answerability_accuracy", "Run pipeline"))
    col4.metric("Citation Coverage", summary.get("citation_coverage_average", "Run pipeline"))
    st.caption(
        "Trust score combines retrieval accuracy, citation coverage, groundedness, risk warnings, "
        "and answerability behavior."
    )

    st.header("Retrieval Metrics")
    st.json(retrieval_report)
    st.dataframe(retrieval_eval, use_container_width=True)

    st.header("Answer Quality Metrics")
    st.json(answer_report)
    st.dataframe(answer_eval, use_container_width=True)

    st.header("Corpus and Chunk Health")
    c1, c2, c3 = st.columns(3)
    c1.metric("Documents", len(documents))
    c2.metric("Chunks", chunk_summary.get("total_chunks", len(chunks)))
    c3.metric("Stale Chunks", chunk_summary.get("stale_chunks", "Run pipeline"))
    st.dataframe(documents, use_container_width=True)

    st.header("Hallucination Risk")
    if not answer_eval.empty:
        risk_cols = [
            "question_id",
            "question_type",
            "hallucination_risk_score",
            "hallucination_risk_reasons",
            "pass_fail",
        ]
        st.dataframe(answer_eval[risk_cols], use_container_width=True)

    st.header("Stale, Conflict, and Sensitive Warnings")
    if not answer_eval.empty:
        warning_cols = [
            "question_id",
            "expected_stale_flag",
            "actual_stale_flag",
            "expected_conflict_flag",
            "actual_conflict_flag",
            "expected_sensitive_flag",
            "actual_sensitive_flag",
        ]
        st.dataframe(answer_eval[warning_cols], use_container_width=True)

    st.header("Golden Question Result Explorer")
    if not answer_eval.empty:
        question_id = st.selectbox("Question ID", answer_eval["question_id"].tolist())
        st.json(answer_eval.loc[answer_eval["question_id"] == question_id].iloc[0].to_dict())

    st.header("Search Lab")
    query = st.text_input("Search query", "What controls are required for privileged access?")
    if query:
        st.dataframe(pd.DataFrame(search(query)), use_container_width=True)

    st.header("Example Answer With Citations")
    question = st.text_input(
        "Question",
        "How quickly must vendors report a confirmed data incident?",
    )
    if question:
        st.json(answer_question(question))

    st.header("Metric Notes")
    st.markdown(
        "- Hit@K measures whether expected documents appear in the top K search results.\n"
        "- Citation coverage measures whether cited documents cover expected evidence.\n"
        "- Groundedness combines retrieval confidence and citation coverage.\n"
        "- Hallucination risk increases when evidence, citations, or expected warnings are missing."
    )


if __name__ == "__main__":
    main()
