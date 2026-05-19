# D20.1 Batch 05 Promotion Subset Candidate Selection

## 1. Purpose
The purpose of D20.1 is to create a bounded promotion-subset candidate manifest for:
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/`

This step is candidate selection only.
It does not perform formal promotion, does not copy files into formal `raw/synthetic_expanded`, does not run intake, does not train tokenizer artifacts or models, and does not modify any batch_05 draft source file.

## 2. Input Review Source
Authoritative D20.1 input sources:
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_targeted_sample_review_manifest.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_targeted_sample_review_summary.json`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_targeted_sampling_manifest.jsonl`
- `docs/d19_3_batch_05_targeted_sampling_review.md`
- `docs/d20_promotion_subset_plan.md`

Automation created for this step:
- `scripts/select_batch_05_promotion_subset_candidates.py`
- `tests/test_select_batch_05_promotion_subset_candidates.py`

Outputs created for D20.1:
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_promotion_subset_candidates.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_promotion_subset_summary.json`

## 3. Selection Rule
D20.1 applies one strict selection rule:
- select only records where `promotion_decision == strong_candidate_for_promotion`

D20.1 excludes every record labeled:
- `keep_as_candidate`
- `needs_rewrite`
- `reject`

Additional file-level checks enforced during selection:
- the source file must still exist
- metadata must still be readable
- `batch_id == domain_synthetic_batch_05`
- `approved_for_training == false`
- `contains_external_text == false`
- `contains_private_data == false`
- `source_category == synthetic_examples`
- `worker_id` must exist
- `topic_id` must exist

Important D20.1 invariant:
- the selector reads source draft metadata but does not modify source files

## 4. Selected Candidate Count
Observed selected candidate count:
- `selected_count = 92`

This matches the D19.3 sampled review total for:
- `strong_candidate_for_promotion = 92`

Interpretation:
- every D19.3 strong candidate was carried into the D20.1 candidate manifest
- no non-strong record was added by extrapolation or worker-level guesswork

## 5. Excluded Records
Observed excluded counts:
- `excluded_keep_as_candidate = 17`
- `excluded_needs_rewrite = 11`
- `excluded_reject = 0`

This means D20.1 preserved the D19.3 review boundary exactly:
- keepers remain draft candidates only
- rewrites remain outside the candidate subset
- no rejected record exists in the reviewed slice

## 6. Worker Breakdown
Observed selected candidates by worker:
- `CC-1`: `20`
- `CC-2`: `11`
- `CC-3`: `20`
- `CC-4`: `20`
- `CC-5`: `11`
- `CC-6`: `10`

Interpretation:
- the clean sampled baseline from `CC-1`, `CC-3`, and `CC-4` contributes `60` candidates
- the more note-heavy workers `CC-2`, `CC-5`, and `CC-6` still contribute `32` strong reviewed candidates
- D20.1 keeps this as one candidate ledger only; it does not convert conditional workers into formally promoted content

## 7. File Type Breakdown
Observed selected file-type counts:
- markdown: `45`
- python: `47`

Interpretation:
- the candidate subset remains balanced across markdown and Python
- D20.1 did not collapse into a single file-type preference despite the mixed worker profiles

## 8. Current Approval State
Current candidate-state fields written into the D20.1 manifest:
- `selected_for_promotion_subset = true`
- `approved_for_training = false`
- `formal_promotion_status = candidate_only_not_promoted`
- `required_next_step = D20.2 formal promotion copy/review`

Important hold state:
- all batch_05 draft source files remain `approved_for_training: false`
- D20.1 does not upgrade approval state in place
- D20.1 only creates a manifest of reviewed candidate records

## 9. Why This Is Not Formal Promotion
D20.1 is not formal promotion because it does **not**:
- copy any file into formal `raw/synthetic_expanded`
- update formal source manifests
- change draft metadata to `approved_for_training: true`
- run intake
- create processed formal-corpus artifacts
- trigger tokenizer or model training

The D20.1 candidate manifest is an evidence-backed staging ledger only.
A later D20.2 step is still required before any formal corpus movement can happen.

## 10. What D20.1 Does Not Do
D20.1 does not:
- perform formal corpus promotion
- copy files into formal `raw/synthetic_expanded`
- run intake
- train a tokenizer
- train a model
- modify model code
- download external data
- modify batch_05 draft source files
- push to a remote repository

## 11. Next Step
Required next step:
- D20.2 formal promotion copy/review

Recommended D20.2 shape:
- review the `92` candidate records as the maximum first-pass promotion pool
- preserve source provenance during any later formal copy step
- run post-copy validation before any intake or training discussion

D20.1 conclusion:
- `selected_count = 92`
- only `strong_candidate_for_promotion` records were selected
- no formal corpus copy was performed
- no intake or tokenizer/model training was run
- batch_05 draft files remain `approved_for_training: false`
- D20.2 is required before formal promotion can happen
