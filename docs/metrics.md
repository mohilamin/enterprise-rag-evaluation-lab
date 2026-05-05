# Metrics

## Hit@K

Business meaning: whether retrieval finds an expected supporting document in the top K results.

Formula:

```text
Hit@K = 1 if any expected_document_id appears in top K, else 0
```

## MRR

Business meaning: how high the first relevant document appears.

Formula:

```text
MRR = 1 / rank_of_first_expected_document
```

## Citation Coverage Score

Business meaning: whether an answer includes citations.

Formula:

```text
100 if citations are present, else 0
```

## Groundedness Score

Business meaning: whether the answer is based on retrieved evidence.

V0.1 formula:

```text
groundedness_score = average(confidence_score, citation_coverage_score)
```

## Hallucination Risk Score

Business meaning: risk that an answer is unsupported.

Formula:

```text
100 when no citations exist, else 100 - confidence_score
```

## Stale Document Risk Score

Business meaning: risk from using stale documents.

Formula:

```text
100 - average(stale_document_flag_accuracy)
```

## Sensitive Data Risk Score

Business meaning: risk from retrieved sensitive-data-like content.

Formula:

```text
100 - average(sensitive_data_flag_accuracy)
```

## Answerability Accuracy

Business meaning: whether the system answers answerable questions and abstains from unanswerable ones.

Formula:

```text
100 if answer/abstain behavior matches is_answerable, else 0
```

## Overall RAG Trust Score

Business meaning: aggregate portfolio signal for retrieval and answer quality.

V0.1 weighted formula:

```text
overall = Hit@3 * 20
        + MRR * 20
        + citation_coverage * 0.15
        + groundedness * 0.20
        + (100 - hallucination_risk) * 0.10
        + (100 - stale_document_risk) * 0.05
        + (100 - sensitive_data_risk) * 0.05
        + answerability_accuracy * 0.05
```
