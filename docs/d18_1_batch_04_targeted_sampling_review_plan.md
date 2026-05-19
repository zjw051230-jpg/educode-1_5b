# D18.1 Batch 04 Targeted Sampling Review Plan

## 1. Purpose
The purpose of D18.1 is to create a targeted human sampling review pack for:
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/`

This step creates a bounded manual-review set and a review framework.
It does not promote any file into the formal corpus, does not change training approval state, and does not run intake, tokenizer training, or model training.

## 2. Why D18.1 Is Needed
D18 structural validation already passed for all `6000` draft files, so the next bottleneck is not file recovery.
The remaining uncertainty is concentrated drafting quality risk:
- template-heavy openings
- repeated internal lines
- markdown scaffolding that may be too formulaic

A full manual review of all `6000` files would be wasteful at this stage.
D18.1 therefore creates a focused `240`-file sampling pack that over-samples the note-heavy worker/style clusters while preserving cleaner baselines for comparison.

## 3. D18 Quality Summary
Authoritative D18 outcome:
- validation status: `passed`
- total draft files: `6000`
- markdown files: `3950`
- python files: `2050`
- quality pass: `2850`
- needs_edit: `3150`
- reject: `0`
- quality gate status: `passed_with_notes`

D18.1 sampling pack outcome:
- total sampled files: `240`
- sampled quality_pass files: `100`
- sampled needs_edit files: `140`
- sampled markdown files: `216`
- sampled python files: `24`

## 4. Main Risks
The main D18 risks carried into D18.1 are:
- `boilerplate_density_high`: `1850` in D18; `99` represented in the D18.1 sample pack
- `templated_opening_family`: `1700` in D18; `108` represented in the D18.1 sample pack
- `repeated_internal_line`: `1300` in D18; `41` represented in the D18.1 sample pack

Interpretation:
- markdown-heavy worker clusters remain the first manual-review target
- the human review should decide whether these patterns are acceptable drafting scaffolds or over-concentrated template families

## 5. Worker Priority
Priority order for D18.1 human review:
1. `CC-2`
2. `CC-3`
3. `CC-5` markdown
4. `CC-6` markdown
5. `CC-1` / `CC-4` as cleaner baselines

This priority follows the D18 note concentration rather than the worker delivery counts.

## 6. Sampling Method
Sampling input:
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/batch_04_quality_review_manifest.jsonl`

Sampling output files:
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/batch_04_targeted_sampling_manifest.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/batch_04_targeted_sampling_summary.json`

Selection method per worker:
- include at least one sample from every subcategory
- include the longest file from the worker sample pool
- include the shortest file from the worker sample pool
- prioritize `needs_edit` records
- prioritize files carrying:
  - `boilerplate_density_high`
  - `templated_opening_family`
  - `repeated_internal_line`
- preserve a smaller cleaner-control slice from available `quality_pass` records
- for `CC-5` and `CC-6`, prioritize markdown-heavy review exposure

Important implementation note:
- the requested worker-level pass/risk ratios are treated as target shapes
- when a worker has no available files in one state, the script fills the remaining slots from the available within-worker pool and records the constraint in the sampling summary
- this affects:
  - `CC-1` / `CC-4`: no D18 risk records available
  - `CC-2` / `CC-3`: no D18 quality_pass records available

## 7. Sampling Counts by Worker
Requested and observed pack size:
- `CC-1`: `40` sampled (`40` quality_pass / `0` risk sampled; no risk files existed)
- `CC-2`: `40` sampled (`0` quality_pass / `40` risk sampled; no quality_pass files existed)
- `CC-3`: `40` sampled (`0` quality_pass / `40` risk sampled; no quality_pass files existed)
- `CC-4`: `40` sampled (`40` quality_pass / `0` risk sampled; no risk files existed)
- `CC-5`: `40` sampled (`10` quality_pass / `30` risk sampled)
- `CC-6`: `40` sampled (`10` quality_pass / `30` risk sampled)

Total sampled files:
- `240`

## 8. Review Rubric
For each sampled file, review:
- metadata correctness
- topic alignment
- originality / synthetic educational value
- template repetition
- practical usefulness
- misleading claim risk
- external-copy risk

Promotion decision choices:
- `keep_as_candidate`
- `needs_rewrite`
- `reject`
- `strong_candidate_for_promotion`

Suggested interpretation:
- `keep_as_candidate`: structurally acceptable draft that can remain in the review pool without immediate rewrite
- `needs_rewrite`: core teaching idea is useful, but templating, repetition, or scaffolding should be revised before any promotion discussion
- `reject`: draft should not be considered for later promotion without major replacement
- `strong_candidate_for_promotion`: unusually clean, distinct, and useful draft that could seed a later promotion subset discussion

## 9. What D18.1 Does Not Do
D18.1 does not:
- approve any file for training
- promote any file into the formal corpus
- enter `raw/synthetic_expanded`
- run intake
- train a tokenizer
- train a model
- download external data
- modify model code
- change any draft record away from `approved_for_training: false`

## 10. Next Step
Recommended next step:
- run human review on the `240`-file D18.1 sampling pack using the provided review template

If the sampling review confirms high template concentration:
- keep note-heavy workers in draft-only status
- plan targeted rewrite families before any promotion subset is proposed

If the sampling review shows acceptable quality in a subset:
- proceed to D18.2 as a bounded promotion-candidate subset exercise rather than a whole-batch promotion step
