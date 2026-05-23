# MVP-4 FineWeb-Edu Public Corpus Intake

## 1. Purpose
The purpose of MVP-4 is to intake the bounded FineWeb-Edu `50MB` public slice into processed/train/val JSONL artifacts, preserve provenance metadata, record a tokenizer decision for the shortest MVP path, and prepare for MVP-5 data/model/loss smoke.

## 2. Input Slice
Input artifacts:
- raw slice: `data/public_corpus/fineweb_edu_sample10bt_50mb/raw.jsonl`
- manifest: `data/public_corpus/fineweb_edu_sample10bt_50mb/manifest.json`
- validation summary: `data/public_corpus/fineweb_edu_sample10bt_50mb/validation_summary.json`
- config: `configs/data/fineweb_edu_sample10bt_50mb.json`

Observed source metadata:
- dataset_id: `HuggingFaceFW/fineweb-edu`
- dataset_config: `sample-10BT`
- license: `odc-by`
- allowed_for_training: `true`

## 3. Intake Script
Script created:
- `scripts/intake_fineweb_edu_slice.py`

Behavior:
- read the config, manifest, and raw JSONL
- require a `text` field on every raw record
- apply lightweight cleaning only: `strip()` text, drop empty texts, drop exact duplicate text hashes
- preserve original text content without heavy normalization
- write provenance-rich processed records

Generated local artifacts:
- `data/public_corpus/fineweb_edu_sample10bt_50mb/processed/fineweb_edu_50mb.processed.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.val.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/intake_summary.json`

## 4. Split Strategy
Split strategy used:
- deterministic seed: `336`
- ratio: `95% train / 5% val`
- stable split method: hash of `seed:doc_id`

This keeps split assignment deterministic without introducing a separate split registry.

## 5. Intake Summary
Observed intake result:
- processed_count: `11070`
- train_count: `10503`
- val_count: `567`
- dropped_empty_count: `0`
- dropped_duplicate_count: `1`
- total_text_bytes: `52433758`
- train_text_bytes: `49654094`
- val_text_bytes: `2779664`

## 6. Validation Summary
Validation script created:
- `scripts/validate_fineweb_edu_intake.py`

Validation behavior:
- verify processed/train/val JSONL files are parseable
- verify `text` exists
- verify `allowed_for_training=true`
- verify `license=odc-by`
- verify `source_category=public_pretraining_corpus`
- verify train/val `doc_id` sets do not overlap
- verify processed `doc_id` set matches the train/val union

Observed validation result:
- processed_count: `11070`
- train_count: `10503`
- val_count: `567`
- dropped_empty_count: `0`
- dropped_duplicate_count: `1`
- total_text_bytes: `52433758`
- train_text_bytes: `49654094`
- val_text_bytes: `2779664`

The processed and split artifacts passed validation.

## 7. Gitignore / Artifact Policy
Artifact policy in this step:
- `raw.jsonl` was not committed
- `processed/` and `splits/` artifacts remain local artifacts unless explicitly approved for later commit
- this step commits only small metadata files, scripts, and documentation

This keeps large corpus artifacts out of git while preserving reproducible control-plane metadata.

## 8. Tokenizer Decision
Tokenizer decision recorded in:
- `docs/mvp_4_public_corpus_tokenizer_decision.md`

Decision summary:
- MVP short path: reuse `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`
- do not train a tokenizer in MVP-4
- later better path: train a public `16k` tokenizer after larger public slices, then consider `32k` only after further public-corpus scaling

## 9. What MVP-4 Does Not Do
MVP-4 does not:
- enter A100
- train a tokenizer
- train a model
- modify model code
- commit `raw.jsonl`
- commit processed/train/val local artifacts in this step

## 10. Next Step
Recommended next step:
- `MVP-5 data/model/loss smoke`

That step should reuse the existing mixed/domain tokenizer artifact for the shortest smoke path on this newly intaked public corpus line.