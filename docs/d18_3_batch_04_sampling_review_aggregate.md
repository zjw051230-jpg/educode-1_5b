# D18.3 Batch 04 Sampling Review Aggregate

## 1. Purpose
The purpose of D18.3 is to aggregate the completed D18.2 human sampling review outputs for:
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/`

This step is a review aggregation and decision step only.
It does not promote any draft into the formal corpus, does not enter formal `raw/synthetic_expanded`, does not run intake, does not train tokenizer artifacts, does not train models, and does not modify the original draft files.

## 2. D18.2 Inputs
D18.3 input files:
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-1_sampling_review.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-2_sampling_review.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-3_sampling_review.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-4_sampling_review.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-5_sampling_review.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-6_sampling_review.jsonl`

Companion review summaries:
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-1_sampling_review_summary.md`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-2_sampling_review_summary.md`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-3_sampling_review_summary.md`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-4_sampling_review_summary.md`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-5_sampling_review_summary.md`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/CC-6_sampling_review_summary.md`

Sampling review scope:
- `6` workers reviewed
- `40` samples per worker
- `240` reviewed samples total

D18.3 aggregate outputs created:
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/batch_04_sampling_review_aggregate.json`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/reviews/batch_04_sampling_review_aggregate.jsonl`

## 3. Aggregate Review Counts
Observed aggregate decision totals:
- reviewed samples: `240`
- `strong_candidate_for_promotion`: `0`
- `keep_as_candidate`: `24`
- `needs_rewrite`: `216`
- `reject`: `0`

Observed rates:
- `needs_rewrite = 216 / 240`
- `needs_rewrite_rate = 0.90`

Readiness result:
- `promotion_readiness = not_ready_for_promotion`

## 4. Worker-by-worker Summary
Observed worker-level decision counts:
- `CC-1`: `0` strong / `7` keep / `33` needs_rewrite / `0` reject
- `CC-2`: `0` strong / `6` keep / `34` needs_rewrite / `0` reject
- `CC-3`: `0` strong / `0` keep / `40` needs_rewrite / `0` reject
- `CC-4`: `0` strong / `1` keep / `39` needs_rewrite / `0` reject
- `CC-5`: `0` strong / `10` keep / `30` needs_rewrite / `0` reject
- `CC-6`: `0` strong / `0` keep / `40` needs_rewrite / `0` reject

Template repetition remained effectively maximal across the batch sample:
- average template repetition risk by worker:
  - `CC-1`: `3.00`
  - `CC-2`: `3.00`
  - `CC-3`: `3.00`
  - `CC-4`: `2.98`
  - `CC-5`: `3.00`
  - `CC-6`: `3.00`

## 5. Main Quality Finding
The main D18.3 finding is that batch_04 is blocked by quality/template repetition, not by safety, metadata, or approval-state hygiene.

Supporting observations:
- `strong_candidate_for_promotion = 0`, so the sampled set did not produce a trustworthy seed subset for promotion.
- `needs_rewrite = 216 / 240`, so rewrite pressure dominates the sample rather than appearing as a small edge case.
- external-copy risk remained low across the full sample.
- misleading-claim risk remained low across the full sample.
- the sampled files generally stayed inside the intended project backbone.

Interpretation:
- the batch problem is not policy failure, private-data risk, external-text carryover, or broken draft metadata
- the batch problem is low originality, repeated scaffolding, shallow topic-specific examples, and weak distinction across many neighboring files

## 6. Promotion Readiness Decision
D18.3 decision:
- batch_04 is `not_ready_for_promotion`
- batch_04 is not ready for formal promotion
- no bounded promotion subset should be created from this D18.2 review result

Decision rationale:
- `strong_candidate_for_promotion = 0`
- `needs_rewrite` clearly dominates the review set
- the sampled keepers are queue candidates only, not promotion-ready assets
- the current quality ceiling is too low for formal corpus movement even when safety and metadata are acceptable

## 7. Why Batch 04 Cannot Be Promoted Yet
Batch_04 cannot be promoted yet because the human review confirms a broad originality and specificity problem across the sampled corpus.

Observed failure pattern:
- repeated scaffold families dominate too many markdown files
- titles and topic phrases often change more than the instructional substance
- several Python samples remain structural wrappers rather than genuinely topic-specific teaching artifacts
- cleaner drafts exist only as limited queue candidates and do not form a strong promotion-ready subset

This means the next bottleneck is not more validation and not more blind generation.
The next bottleneck is repair-aware regeneration with stronger anti-template constraints.

## 8. Repair / Regeneration Direction
Recommended direction after D18.3:
- do not promote batch_04 into the formal corpus
- do not push the sampled keepers into a promotion subset yet
- use the D18.2 worker notes plus the D18.3 aggregate to define a repair-aware generation strategy
- prioritize topic-specific examples, runtime artifacts, tensor shapes, formulas, debugging traces, concrete failure modes, and reduced scaffold reuse

Immediate worker-level repair direction:
- `CC-1`: rewrite curriculum, optimization, and regularization clusters with more topic-specific substance
- `CC-2`: add concrete failure scenarios, review decisions, and invariant examples
- `CC-3`: add tensor shapes, formulas, traces, and debugging steps instead of generic transformer scaffolds
- `CC-4`: add runtime artifacts, diagnostic signals, and concrete failure modes
- `CC-5`: reduce bilingual Q&A template reuse and make explanations more natural and topic-specific
- `CC-6`: rewrite `source_category_tools` to actually count, group, and report source categories rather than using generic numeric-summary scaffolds

## 9. What D18.3 Does Not Do
D18.3 does not:
- perform formal corpus promotion
- copy any draft into the formal corpus
- change any batch_04 draft away from `approved_for_training: false`
- enter formal `raw/synthetic_expanded`
- run intake
- train a tokenizer
- train a model
- download external data
- modify original draft files

Explicitly confirmed outcome:
- no formal corpus promotion
- no intake
- no tokenizer/model training

## 10. Next Step
Recommended next step:
- D19 repair-aware regeneration plan, not more blind generation

Recommended implementation shape:
- start with a small repair-aware generation batch rather than another full `6000`-file sweep
- validate the repaired batch again before discussing any promotion subset

D18.3 conclusion:
- batch_04 remains a draft-queue asset only
- current problem is quality/template repetition, not safety or metadata
- the correct next move is controlled repair-aware regeneration, not promotion
