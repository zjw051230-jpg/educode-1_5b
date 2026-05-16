# D17.1 Draft Corpus Generation Validation

## 1. Purpose
The purpose of D17.1 is to aggregate and validate the generated draft corpus candidates under:
- `data/real_corpus/draft_queue/domain_synthetic_batch_03/`

This step validates the draft queue only.
It does not enter formal `raw` or `synthetic_expanded` corpus paths, does not run intake, does not train tokenizer artifacts, and does not run model training.

## 2. Worker Completion Summary
Observed D17.1 completion state:
- 6 worker directories contain generated draft outputs
- 120 draft topic files are present
- 6 `batch_summary.md` files are present
- generated topic coverage spans:
  - `MLF-001` to `MLF-020`
  - `PDS-001` to `PDS-020`
  - `TRF-001` to `TRF-020`
  - `RTS-001` to `RTS-020`
  - `BIL-001` to `BIL-020`
  - `COD-001` to `COD-020`

## 3. Topic Registry Validation
Validated file:
- `data/real_corpus/draft_queue/domain_synthetic_batch_03/00_framework/topic_registry.jsonl`

Validation result:
- JSONL parse: passed
- registry row count: `120`
- `topic_id` uniqueness: passed
- registry target-path uniqueness: passed
- worker distribution: passed
  - `CC-1 = 20`
  - `CC-2 = 20`
  - `CC-3 = 20`
  - `CC-4 = 20`
  - `CC-5 = 20`
  - `CC-6 = 20`

## 4. File Count Summary
Validated batch totals:
- total topic files: `120`
- markdown topic files: `78`
- python topic files: `42`
- batch summaries: `6`
- missing files: `0`

Line-count summary across the 120 topic files:
- min lines: `26`
- max lines: `63`
- mean lines: `44.02`

## 5. Worker Breakdown
Observed topic-file counts by worker from the registry-aligned file set:
- `CC-1`: `20` topic files = `16` markdown / `4` python
- `CC-2`: `20` topic files = `12` markdown / `8` python
- `CC-3`: `20` topic files = `15` markdown / `5` python
- `CC-4`: `20` topic files = `14` markdown / `6` python
- `CC-5`: `20` topic files = `16` markdown / `4` python
- `CC-6`: `20` topic files = `5` markdown / `15` python

These counts reflect the actual draft files validated in D17.1.

## 6. Metadata Validation
Metadata validation checks passed for all 120 topic files.

For markdown files, the required YAML metadata fields were present and valid:
- `draft_status: candidate`
- `topic_id`
- `source_category: synthetic_examples`
- `project_backbone: cs_ml_python_transformer_training_systems`
- `worker_id`
- `approved_for_training: false`
- `contains_external_text: false`
- `contains_private_data: false`
- `target_use: draft_review_only`

For python files, the required top-of-file comment metadata fields were present and valid with the same values.

Additional validation checks passed:
- metadata `topic_id` matched the registry topic id
- metadata `worker_id` matched the expected worker after worker-id normalization
- `approved_for_training` remained false for all topic files
- `contains_external_text` remained false for all topic files
- `contains_private_data` remained false for all topic files

Metadata error count:
- `0`

## 7. File Type Validation
Registry-to-file validation passed:
- all 120 registry topics resolved to existing files
- file extensions matched the declared registry `file_type`
- no required topic file was missing
- no scope-path mismatch was recorded

Scope error count:
- `0`

## 8. Secret Scan Result
Secret scan result:
- `explanatory-only`

Observed result:
- no credential-style secrets were found
- explanatory-only hits remained in educational text where words such as `token` appeared in a teaching context
- validation therefore remained `passed`

Examples of explanatory-only hits:
- next-token discussion in training explanations
- tokenizer helper examples using names like `token_to_id`
- worker summary notes describing prior secret-scan behavior

## 9. Scope Check
Scope check result:
- passed

D17.1 now includes a repository-state scope gate based on `git status --short`.
The validator allows only the expected D17.1 paths:
- `data/real_corpus/draft_queue/domain_synthetic_batch_03/`
- `scripts/validate_draft_corpus_batch_03.py`
- `docs/d17_1_draft_corpus_generation_validation.md`
- `docs/d17_1_worker_aggregation_summary.md`
- `README.md`
- `docs/experiment_index.md`

Observed result:
- no out-of-scope git-status paths were found
- the draft queue contents matched the registry-aligned validation scope
- D17.1 therefore remained bounded to draft-queue validation plus its required reporting files

## 10. Current Approval State
Current approval state remains intentionally constrained:
- all 120 files remain draft candidates
- `approved_for_training` remains `false`
- no file in this batch is approved for training
- no promotion into the formal corpus has occurred

## 11. What D17.1 Does Not Do
D17.1 does not:
- enter formal `raw` corpus paths
- enter formal `synthetic_expanded` corpus paths
- run intake
- retrain tokenizer artifacts
- run model training
- download external data
- copy external corpus text
- mark any draft candidate as training-approved

## 12. Next Step
Recommended next step:
- D17.2 draft corpus review gate

Rationale:
- the draft generation batch is now aggregated and validated
- all files remain review-only draft candidates
- the next project need is a structured review gate before any future promotion discussion
