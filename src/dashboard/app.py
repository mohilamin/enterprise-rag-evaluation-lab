from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.common.config import get_path
from src.rag.answer import answer_question
from src.retrieval.search import search


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    st.set_page_config(page_title="Enterprise RAG Evaluation Lab", layout="wide")
    st.title("Enterprise Document Intelligence + RAG Evaluation Lab")

    summary_path = get_path("scorecards") / "rag_trust_summary.json"
    summary = json.loads(summary_path.read_text()) if summary_path.exists() else {}
    documents = read_csv(get_path("raw_documents") / "documents_metadata.csv")
    chunks = read_csv(get_path("chunks") / "chunks.csv")
    retrieval_eval = read_csv(get_path("evaluations") / "retrieval_evaluation.csv")
    answer_eval = read_csv(get_path("evaluations") / "answer_evaluation.csv")

    st.header("Executive Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("RAG Trust Score", summary.get("overall_rag_trust_score", "Run pipeline"))
    col2.metric("Hit@3", summary.get("hit_at_3", "Run pipeline"))
    col3.metric("Documents", len(documents))

    st.header("Corpus Health")
    st.dataframe(documents, use_container_width=True)
    if not chunks.empty:
        st.bar_chart(chunks.groupby("department").size())

    st.header("Document Issues")
    manifest_path = get_path("raw_documents") / "injected_document_issue_manifest.json"
    st.json(json.loads(manifest_path.read_text()) if manifest_path.exists() else {})

    st.header("Search Lab")
    query = st.text_input("Search query", "What controls are required for privileged access?")
    if query:
        st.dataframe(pd.DataFrame(search(query)), use_container_width=True)

    st.header("Answer With Citations")
    question = st.text_input(
        "Question",
        "How quickly must vendors report a confirmed data incident?",
    )
    if question:
        st.json(answer_question(question))

    st.header("RAG Evaluation Metrics")
    st.json(summary)
    st.dataframe(retrieval_eval, use_container_width=True)

    st.header("Hallucination Risk")
    if not answer_eval.empty:
        st.line_chart(answer_eval["hallucination_risk_score"])

    st.header("Stale Document Risk")
    if not answer_eval.empty:
        st.bar_chart(answer_eval["stale_document_flag_accuracy"])

    st.header("Sensitive Data Risk")
    if not answer_eval.empty:
        st.bar_chart(answer_eval["sensitive_data_flag_accuracy"])

    st.header("Golden Question Results")
    st.dataframe(answer_eval, use_container_width=True)


if __name__ == "__main__":
    main()
