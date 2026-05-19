# D18 Batch 04 Draft Corpus Validation and Quality Review

## 1. Purpose
The purpose of D18 is to aggregate, validate, and quality-review the generated draft corpus candidates under:
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/`

This step remains draft-queue only.
It does not promote files into the formal corpus, does not enter formal `raw/synthetic_expanded`, does not run intake, does not train tokenizer artifacts, does not train models, and does not modify model code.

## 2. Input Batch
Reviewed input set:
- batch root: `data/real_corpus/draft_queue/domain_synthetic_batch_04/`
- worker directories reviewed: `6`
- expected topic draft files: `6000`
- expected markdown files: `3950`
- expected python files: `2050`

Worker targets:
- `CC-1`: `1000` total = `700` markdown + `300` python
- `CC-2`: `1000` total = `700` markdown + `300` python
- `CC-3`: `1000` total = `700` markdown + `300` python
- `CC-4`: `1000` total = `700` markdown + `300` python
- `CC-5`: `1000` total = `850` markdown + `150` python
- `CC-6`: `1000` total = `300` markdown + `700` python

D18 outputs created:
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/batch_04_validation_manifest.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/batch_04_validation_summary.json`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/batch_04_quality_review_manifest.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_04/batch_04_quality_review_summary.json`

## 3. Validation Method
D18 validation used:
- `scripts/validate_draft_corpus_batch_04.py`

The validator normalizes the observed worker-manifest variations before checking the batch:
- `filename` + `subdirectory` rows from `CC-1` / `CC-2`
- `proposed_filename` + `subcategory` rows from `CC-3`
- full repo-relative `path` rows plus `md` / `py` file-type tags from `CC-4`
- full repo-relative `filename` rows plus `subdir` from `CC-5`
- `relative_path` + `subcategory` rows from `CC-6`

Validation checks applied:
- manifest row parsing across all six workers
- worker-level target counts for total / markdown / python files
- batch-summary declared counts per worker
- presence of exactly `10` progress files per worker directory
- per-file metadata correctness
- topic-id and worker-scope consistency
- `approved_for_training`, `contains_external_text`, and `contains_private_data` must remain `false`
- secret-scan classification
- unexpected-file detection inside the batch scope
- git-scope enforcement so only D18 paths appear in `git status --short`

## 4. Validation Results
Observed validation totals:
- `validation_status`: `passed`
- total manifest rows: `6000`
- total topic files: `6000`
- markdown files: `3950`
- python files: `2050`
- passed validation records: `6000`
- failed validation records: `0`

Observed error counts:
- missing files: `0`
- metadata errors: `0`
- scope errors: `0`
- git-scope errors: `0`
- duplicate `topic_id` count: `0`
- duplicate file-path count: `0`

Secret-scan interpretation:
- `secret_scan.result`: `explanatory-only`
- credential-style secret hits: `0`

Worker-level result:
- every worker delivered the expected `1000` manifest rows
- every worker matched its expected markdown/python split
- every worker exposed `10` progress files
- every worker batch summary matched the validator-observed totals

## 5. Quality Review Method
D18 quality review used:
- `scripts/review_draft_corpus_quality_batch_04.py`

The quality script reads the validation manifest as its source of truth and then scores drafting patterns that matter for later human review.

Heuristics applied:
- repeated internal lines inside one file
- high-frequency templated opening families across a worker block
- dense boilerplate markers inside review-note sections
- external-reference style wording
- domain-drift terms outside the project backbone
- overly strong claim language
- bilingual markdown pair checks for `CC-5`

Quality states recorded:
- `quality_pass`
- `needs_edit`
- `reject`

## 6. Quality Review Results
Observed quality totals:
- total review records: `6000`
- `quality_pass`: `2850`
- `needs_edit`: `3150`
- `reject`: `0`
- `quality_gate_status`: `passed_with_notes`

Worker-level quality breakdown:
- `CC-1`: `1000` pass / `0` needs_edit / `0` reject
- `CC-2`: `0` pass / `1000` needs_edit / `0` reject
- `CC-3`: `0` pass / `1000` needs_edit / `0` reject
- `CC-4`: `1000` pass / `0` needs_edit / `0` reject
- `CC-5`: `150` pass / `850` needs_edit / `0` reject
- `CC-6`: `700` pass / `300` needs_edit / `0` reject

Dominant note categories:
- `templated_opening_family`: `1700`
- `boilerplate_density_high`: `1850`
- `repeated_internal_line`: `1300`

Interpretation:
- D18 did not find structurally invalid files after validation passed
- D18 did find concentrated template repetition in specific worker/style clusters
- the highest follow-up priority is not file recovery but targeted human editing review

## 7. JSONL Output Validation
Both D18 manifests were re-checked as line-delimited JSON:
- `batch_04_validation_manifest.jsonl`: `6000` valid rows
- `batch_04_quality_review_manifest.jsonl`: `6000` valid rows

No empty or malformed JSONL lines were found in the generated D18 manifests.

## 8. Governance and Scope
D18 scope outcome:
- work remained inside `data/real_corpus/draft_queue/domain_synthetic_batch_04/`
- no draft was copied into the formal corpus
- no formal `raw/synthetic_expanded` path was entered
- no intake pipeline was run
- no tokenizer training was run
- no model training was run
- no model code was modified

Approval-state outcome:
- all validated draft files remain `approved_for_training: false`
- all validated draft files remain `contains_external_text: false`
- all validated draft files remain `contains_private_data: false`
- all validated draft files remain review-only candidates

## 9. D18 Decision
D18 decision:
- structural validation passed
- automated quality review passed with notes
- the batch remains a draft-review asset, not a training-ready corpus asset

This means batch_04 is suitable for:
- continued draft-queue storage
- human sampling and qualitative inspection
- later promotion discussion only after note-heavy clusters are reviewed

## 10. What D18 Does Not Do
D18 does not:
- approve any file for training
- promote any file into the formal corpus
- enter `raw/synthetic_expanded`
- run intake
- train a tokenizer
- train a model
- download external data
- change draft files into formal corpus material

## 11. Next Step
Recommended next step:
- run targeted human sampling with priority on `CC-2`, `CC-3`, markdown-heavy `CC-5`, and markdown-heavy `CC-6`

Rationale:
- structural quality is already strong enough to trust the batch inventory
- quality notes are concentrated rather than uniform
- the best next review effort is a focused manual pass over the templating-heavy clusters instead of re-validating the whole batch
