# Sample Outputs

These examples show the shape of the V0.2 evidence files and API responses. Values may change slightly when the corpus or scoring rules evolve.

## Golden Question Record

```json
{
  "question_id": "Q002",
  "question_text": "What controls are required for privileged access?",
  "question_type": "single_document_answerable",
  "expected_document_ids": ["DOC-IT-001"],
  "expected_facts": ["multi-factor authentication", "manager approval"],
  "should_have_citation": true,
  "should_flag_stale": false,
  "should_flag_conflict": false,
  "should_flag_sensitive_data": false,
  "is_answerable": true
}
```

## Search Response

```json
{
  "query": "What controls are required for privileged access?",
  "top_k": 3,
  "results": [
    {
      "rank": 1,
      "document_id": "DOC-IT-001",
      "chunk_id": "DOC-IT-001-CHUNK-003",
      "title": "IT Security Access Control Policy",
      "score": 0.74,
      "snippet": "Privileged access requires multi-factor authentication..."
    }
  ]
}
```

## Answer Response With Citations

```json
{
  "question": "What controls are required for privileged access?",
  "answer_text": "Based on retrieved evidence: privileged access requires multi-factor authentication and manager approval.",
  "citations": [
    {"document_id": "DOC-IT-001", "chunk_id": "DOC-IT-001-CHUNK-003"}
  ],
  "confidence_score": 70.0,
  "groundedness_score": 85.0,
  "citation_coverage_score": 100.0,
  "hallucination_risk_score": 30.0,
  "hallucination_risk_reasons": [],
  "stale_document_warning": false,
  "conflict_warning": false,
  "sensitive_data_warning": false
}
```

## Insufficient Evidence Response

```json
{
  "question": "What is the approved office furniture vendor list?",
  "answer_text": "Insufficient evidence in retrieved documents.",
  "citations": [],
  "confidence_score": 0.0,
  "groundedness_score": 0.0,
  "citation_coverage_score": 0.0,
  "hallucination_risk_score": 100.0
}
```

## Retrieval Accuracy Report

```json
{
  "total_questions": 40,
  "answerable_questions": 34,
  "unanswerable_questions": 6,
  "hit_at_1": 0.8529,
  "hit_at_3": 0.9706,
  "hit_at_5": 0.9706,
  "mrr": 0.9069,
  "missed_questions": [
    {
      "question_id": "Q027",
      "question_type": "stale_document_trap",
      "expected_document_ids": "[\"DOC-IR-001\"]"
    }
  ]
}
```

## Answer Quality Report

```json
{
  "total_questions": 40,
  "answerability_accuracy": 97.5,
  "citation_coverage_average": 87.5,
  "groundedness_average": 54.35,
  "hallucination_risk_average": 74.19,
  "stale_warning_accuracy": 95.0,
  "conflict_warning_accuracy": 87.5,
  "sensitive_data_warning_accuracy": 95.0,
  "overall_rag_trust_score": 78.5
}
```

## Chunk Quality Summary

```json
{
  "total_chunks": 156,
  "average_chunk_length": 18.12,
  "empty_chunks": 0,
  "chunks_missing_metadata": 24,
  "stale_chunks": 24,
  "sensitive_chunks": 1
}
```

## RAG Trust Summary

```json
{
  "hit_at_3": 0.9706,
  "mrr": 0.9069,
  "citation_coverage_average": 87.5,
  "answerability_accuracy": 97.5,
  "overall_rag_trust_score": 78.5
}
```
