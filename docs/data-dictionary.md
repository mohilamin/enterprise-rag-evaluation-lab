# Data Dictionary

## Documents

- `document_id`: Stable synthetic document identifier.
- `title`: Business-readable document title.
- `department`: Owning department.
- `effective_date`: Date the document became active.
- `last_reviewed_date`: Date of last policy review.
- `version`: Synthetic document version.
- `owner`: Business owner or steward.
- `confidentiality_level`: Internal, confidential, or restricted.
- `key_facts`: Pipe-delimited facts used for evaluation.
- `related_controls`: Synthetic control references.

## Chunks

- `chunk_id`: Stable chunk identifier.
- `chunk_index`: Position within the source document.
- `text`: Chunk text.
- `is_stale`: Whether document freshness exceeds the threshold.
- `has_sensitive_pattern`: Whether synthetic sensitive-data-like patterns appear.
- `has_conflict_language`: Whether text contains conflict language.

## Golden Questions

- `question_id`: Stable evaluation identifier.
- `question_text`: Business question.
- `expected_document_ids`: Documents expected to support the answer.
- `expected_facts`: Expected answer evidence.
- `is_answerable`: Whether the answer should be present in the corpus.
