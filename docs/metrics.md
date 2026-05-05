# Metrics

This project uses deterministic metrics so reviewers can inspect exactly how retrieval and answer quality are judged. Scores are evidence signals for the synthetic lab, not production certification.

## Hit@1

Business meaning: whether the top-ranked result contains at least one expected supporting document.

Formula:

```text
Hit@1 = 1 if any expected_document_id appears in the top 1 retrieved document_ids, else 0
```

Input fields: `expected_document_ids`, top retrieved `document_id`.

Pass/fail interpretation: a pass means the first result is immediately useful for the question.

Example: expected `DOC-IT-001`, top result `DOC-IT-001` means Hit@1 is 1.

## Hit@3

Business meaning: whether the expected evidence appears in the first three results.

Formula:

```text
Hit@3 = 1 if any expected_document_id appears in the top 3 retrieved document_ids, else 0
```

Input fields: `expected_document_ids`, top three retrieved `document_id` values.

Pass/fail interpretation: a pass means a user or answer composer can likely find supporting evidence quickly.

Example: expected `DOC-FIN-001`, top three include `DOC-FIN-001`, so Hit@3 is 1.

## Hit@5

Business meaning: whether the expected evidence appears within the retrieval context sent to the answer layer.

Formula:

```text
Hit@5 = 1 if any expected_document_id appears in the top 5 retrieved document_ids, else 0
```

Input fields: `expected_document_ids`, top five retrieved `document_id` values.

Pass/fail interpretation: a fail is a retrieval miss that can cause unsupported or insufficient answers.

Example: expected `DOC-IR-001`, top five do not include it, so Hit@5 is 0.

## MRR

Business meaning: how high the first relevant document appears.

Formula:

```text
MRR = 1 / rank_of_first_expected_document
MRR = 0 when no expected document is retrieved
```

Input fields: ranked retrieved `document_id` values and `expected_document_ids`.

Pass/fail interpretation: higher MRR means less evidence-search friction.

Example: expected document appears at rank 2, so reciprocal rank is 0.5.

## Citation Coverage Score

Business meaning: whether cited evidence covers the expected supporting documents.

Formula:

```text
citation_coverage_score =
  cited_expected_document_count / expected_document_count * 100
```

Input fields: expected document IDs, cited document IDs, citation validation output.

Pass/fail interpretation: 100 means every expected supporting document was cited; 0 means no expected support was cited.

Example: expected `DOC-FIN-001` and `DOC-PRO-001`; cited only `DOC-FIN-001`; score is 50.

## Groundedness Score

Business meaning: whether the answer appears tied to retrieved evidence rather than unsupported generation.

Formula:

```text
groundedness_score = average(confidence_score, citation_coverage_score)
```

Input fields: answer `confidence_score`, citation coverage score.

Pass/fail interpretation: higher groundedness means stronger evidence linkage.

Example: confidence 70 and citation coverage 100 gives groundedness 85.

## Hallucination Risk Score

Business meaning: risk that the answer contains unsupported or unsafe claims.

Formula:

```text
base_risk = 100 if no citations exist else 100 - confidence_score
final_risk = min(100, base_risk + 8 * extra_risk_reason_count)
```

Input fields: citations, confidence score, expected evidence, retrieved evidence, warning flags.

Penalty logic: risk increases when answers lack citations, cite the wrong evidence, answer unanswerable questions, miss expected documents, or miss stale/conflict/sensitive warnings.

Example: confidence 55 with two extra risk reasons gives `45 + 16 = 61`.

## Stale Document Risk Score

Business meaning: risk that the system failed to warn when stale documents were expected.

Formula:

```text
stale_document_risk_score = 100 - stale_warning_accuracy
```

Input fields: golden question `should_flag_stale`, answer `stale_document_warning`.

Pass/fail interpretation: lower is better; 0 means stale warnings matched all expectations.

Example: 95% stale warning accuracy produces a stale risk score of 5.

## Sensitive Data Risk Score

Business meaning: risk that sensitive-data-like context was missed.

Formula:

```text
sensitive_data_risk_score = 100 - sensitive_data_warning_accuracy
```

Input fields: golden question `should_flag_sensitive_data`, answer `sensitive_data_warning`.

Pass/fail interpretation: lower is better; 0 means sensitive-data warnings matched all expectations.

Example: 95% warning accuracy produces sensitive data risk of 5.

## Answerability Accuracy

Business meaning: whether the answer layer answers answerable questions and abstains from unanswerable ones.

Formula:

```text
answerability_accuracy =
  correct_answer_or_abstain_count / total_questions * 100
```

Input fields: golden question `is_answerable`, answer text.

Pass/fail interpretation: a good enterprise assistant should say insufficient evidence when the corpus cannot support the answer.

Example: 39 correct answer/abstain decisions across 40 questions gives 97.5.

## Overall RAG Trust Score

Business meaning: a single portfolio score that summarizes retrieval, citation, groundedness, risk, and answerability evidence.

Formula:

```text
overall =
  Hit@3 * 20
  + MRR * 20
  + citation_coverage_score * 0.15
  + groundedness_score * 0.20
  + (100 - hallucination_risk_score) * 0.10
  + (100 - stale_document_risk_score) * 0.05
  + (100 - sensitive_data_risk_score) * 0.05
  + answerability_accuracy * 0.05
```

Input fields: retrieval report, answer quality report, risk scores.

Pass/fail interpretation: higher is better, but component metrics should be reviewed before trusting the aggregate.

Example interpretation: a score of 78.5 means the deterministic baseline is strong enough for portfolio demonstration while still showing realistic gaps such as missed retrievals or warning mismatches.
