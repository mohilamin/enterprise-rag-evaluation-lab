# Sample Outputs

## Search Result

```json
{
  "document_id": "DOC-IT-001",
  "chunk_id": "DOC-IT-001-CHUNK-000",
  "rank": 1,
  "final_score": 0.42,
  "snippet": "Privileged access requires multi-factor authentication..."
}
```

## Answer Result

```json
{
  "answer_text": "Based on retrieved evidence...",
  "citations": [{"document_id": "DOC-IT-001", "chunk_id": "DOC-IT-001-CHUNK-000"}],
  "groundedness_score": 82.5,
  "hallucination_risk_score": 35.0
}
```

## Trust Summary

```json
{
  "hit_at_3": 0.9,
  "mrr": 0.82,
  "overall_rag_trust_score": 78.4
}
```
