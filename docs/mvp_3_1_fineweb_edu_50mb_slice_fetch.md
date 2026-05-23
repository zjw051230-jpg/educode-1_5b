# MVP-3.1 FineWeb-Edu 50MB Slice Fetch and Validation

## 1. Purpose
The purpose of MVP-3.1 is to execute the first bounded `50MB` public-corpus fetch from FineWeb-Edu, validate the fetched JSONL and manifest artifacts, and record the result without entering A100 execution or any tokenizer/model training step.

## 2. Input Dataset
- dataset_id: `HuggingFaceFW/fineweb-edu`
- dataset_config: `sample-10BT`
- split: `train`
- license: `odc-by`

## 3. Config Used
Config file:
- `configs/data/fineweb_edu_sample10bt_50mb.json`

Key config values:
- `target_size_mb=50`
- `streaming=true`
- `text_field=text`
- `allowed_for_training=true`
- output directory: `data/public_corpus/fineweb_edu_sample10bt_50mb`

## 4. Fetch Command
Command used:

```text
.venv/Scripts/python.exe scripts/fetch_fineweb_edu_slice.py --config configs/data/fineweb_edu_sample10bt_50mb.json --retries 2 --timeout-seconds 120
```

Observed fetch result:
- `dry_run=false`
- `record_count=11071`
- `size_mb=50.019822`
- `raw.jsonl` generated locally at `data/public_corpus/fineweb_edu_sample10bt_50mb/raw.jsonl`
- `manifest.json` generated locally at `data/public_corpus/fineweb_edu_sample10bt_50mb/manifest.json`

This step downloaded only a bounded `50MB` slice.

## 5. Manifest Summary
Observed manifest fields:
- `dataset_id=HuggingFaceFW/fineweb-edu`
- `dataset_config=sample-10BT`
- `split=train`
- `target_size_mb=50`
- `actual_size_bytes=52449585`
- `record_count=11071`
- `license=odc-by`
- `allowed_for_training=true`

## 6. Validation Summary
Validation command used:

```text
.venv/Scripts/python.exe scripts/validate_fineweb_edu_slice.py --config configs/data/fineweb_edu_sample10bt_50mb.json
```

Observed validation result:
- `record_count=11071`
- `total_text_bytes=52449585`
- `total_file_bytes=52867234`
- `min_text_chars=255`
- `max_text_chars=485117`
- `mean_text_chars=4717.187698`
- `empty_text_count=0`
- `duplicate_text_hash_count=1`
- `dataset_id=HuggingFaceFW/fineweb-edu`
- `dataset_config=sample-10BT`
- `license=odc-by`
- `allowed_for_training=True`
- `validation_summary.json` written to `data/public_corpus/fineweb_edu_sample10bt_50mb/validation_summary.json`

The JSONL was parseable, the required `text` field was present, the manifest was complete, and no empty text records were observed.

## 7. Gitignore Check
A targeted git status check on `data/public_corpus/fineweb_edu_sample10bt_50mb/` showed:
- `manifest.json` visible as an untracked metadata artifact
- `validation_summary.json` visible as an untracked metadata artifact
- `raw.jsonl` not shown by `git status`

This confirms that `raw.jsonl` remained git-ignored and was not prepared for commit.

## 8. What MVP-3.1 Does Not Do
MVP-3.1 does not:
- enter A100 execution
- run training
- train the tokenizer
- train the model
- modify model code
- submit `raw.jsonl` to git

## 9. Next Step
Recommended next step:
- `MVP-4 public corpus intake / tokenizer decision`

That next step should decide how this bounded public slice should be reviewed, integrated, or excluded before any later tokenizer or training action.