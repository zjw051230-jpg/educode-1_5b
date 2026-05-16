# D17.2 Draft Corpus Review Gate

## 1. Purpose
The purpose of D17.2 is to run an automated review gate over the generated draft corpus candidates under:
- `data/real_corpus/draft_queue/domain_synthetic_batch_03/`

This step evaluates draft-review readiness only.
It does not promote files into the formal corpus, does not enter formal `raw` or `synthetic_expanded` paths, does not run intake, does not train tokenizer artifacts, and does not run model training.

## 2. Input Draft Queue
Reviewed input set:
- topic registry: `data/real_corpus/draft_queue/domain_synthetic_batch_03/00_framework/topic_registry.jsonl`
- topic registry rows: `120`
- draft topic files reviewed: `120`
- worker categories reviewed: `6`
- batch root: `data/real_corpus/draft_queue/domain_synthetic_batch_03/`

Review outputs created in D17.2:
- `data/real_corpus/draft_queue/domain_synthetic_batch_03/00_framework/draft_review_manifest.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_03/00_framework/draft_review_summary.json`

## 3. Review Method
D17.2 used:
- `scripts/review_draft_corpus_batch_03.py`

For each registered topic file, the script recorded:
- topic identity and path information
- line count and character count
- metadata validity
- topic-id match status
- worker/category scope status
- in-file governance flags
- secret-scan result
- length status
- duplicate-title / duplicate-filename review note status
- final `review_state`
- review notes

Automatic review rules applied:
- metadata must be valid
- `topic_id` must match and remain unique
- worker/category scope must match
- `approved_for_training` must remain `false`
- `contains_external_text` must remain `false`
- `contains_private_data` must remain `false`
- no credential-style secret may be present
- files must be non-empty
- line count is reviewed against the recommended range `20` to `160`
- duplicate `proposed_filename` values are flagged for manual follow-up

`review_state` meanings:
- `approved_for_promotion_candidate`
- `needs_edit`
- `rejected`

Important interpretation:
- `approved_for_promotion_candidate` is not formal corpus approval
- it only means the file may proceed to a later D17.3 promotion discussion

## 4. Review State Summary
Observed D17.2 review totals:
- total review records: `120`
- `approved_for_promotion_candidate`: `118`
- `needs_edit`: `2`
- `rejected`: `0`
- `review_gate_status`: `passed_with_notes`

Why `passed_with_notes`:
- no file was rejected
- two files were flagged `needs_edit` because a duplicate `proposed_filename` appeared across two different worker paths

## 5. Worker Breakdown
Per-worker review results:
- `CC-1`: `20` approved / `0` needs_edit / `0` rejected
- `CC-2`: `20` approved / `0` needs_edit / `0` rejected
- `CC-3`: `20` approved / `0` needs_edit / `0` rejected
- `CC-4`: `19` approved / `1` needs_edit / `0` rejected
- `CC-5`: `20` approved / `0` needs_edit / `0` rejected
- `CC-6`: `19` approved / `1` needs_edit / `0` rejected

The two `needs_edit` records are the duplicate-filename pair:
- `RTS-017` → `summary_data_dict_pattern.py`
- `COD-016` → `summary_data_dict_pattern.py`

## 6. Metadata Check
Metadata review outcome:
- all `120` reviewed files retained draft metadata structure
- all reviewed files kept `approved_for_training: false`
- all reviewed files kept `contains_external_text: false`
- all reviewed files kept `contains_private_data: false`
- no metadata-based rejection was triggered

This means all draft files remain review-only and are still not approved for training.

## 7. Scope Check
Scope check outcome:
- D17.2 operated only on the draft queue and D17.2 reporting artifacts
- no formal corpus promotion occurred
- no copy into formal `synthetic_expanded` occurred
- no intake pipeline was run
- no tokenizer or model training was run
- no model code was modified

D17.2 therefore remained a review-gate step only.

## 8. Secret Scan Result
Secret-scan summary from the review manifest:
- `passed`: `66`
- `explanatory-only`: `54`
- credential-style secret hits: `0`

Interpretation:
- explanatory-only hits remained educational in nature
- no file was rejected for credential-style secret content

## 9. Length / File Type Summary
Observed file-type totals:
- markdown files: `78`
- python files: `42`

Observed line-count summary:
- minimum lines: `26`
- maximum lines: `63`
- mean lines: `44.02`

Length interpretation:
- all reviewed files were non-empty
- all files stayed within the recommended line-count range for this automatic gate
- the only `needs_edit` cases came from duplicate filename follow-up rather than file length

## 10. Promotion Candidate Decision
D17.2 decision:
- `118` files are `approved_for_promotion_candidate`
- `2` files are `needs_edit`
- `0` files are `rejected`

This means:
- the automated review gate passed with notes
- the batch is not yet formal corpus material
- the two duplicate-filename items should be resolved or explicitly dispositioned before a later D17.3 promotion step

## 11. What D17.2 Does Not Do
D17.2 does not:
- enter formal corpus paths
- enter `raw/synthetic_expanded`
- copy any draft into the formal corpus
- run intake
- train tokenizer artifacts
- train models
- modify model code
- change draft files so they become training-approved

All draft files still remain `approved_for_training: false` after this step.

## 12. Next Step
Recommended next step:
- D17.3 promotion preparation with human sampling plus duplicate-filename disposition

Rationale:
- the automated review gate has completed for all `120` candidate files
- no file was rejected
- two candidate files still need manual naming/disposition follow-up
- human sampling should occur before any later promotion discussion
