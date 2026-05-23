# MVP-11.1 FineWeb-Edu 500MB Fetch and Intake

## 1. Purpose

MVP-11.1 executes the bounded FineWeb-Edu 500MB public corpus expansion prepared in MVP-11.

This step fetches the 500MB slice, validates the raw JSONL, intakes it into processed train/validation splits, validates the intake outputs, and records only small metadata summaries for Git.

## 2. Input Config

- config: `configs/data/fineweb_edu_sample10bt_500mb.json`
- dataset: `HuggingFaceFW/fineweb-edu`
- dataset config: `sample-10BT`
- split: `train`
- streaming: `true`
- target size: `500MB`
- text field: `text`
- license: `odc-by`
- allowed for training: `true`
- output directory: `data/public_corpus/fineweb_edu_sample10bt_500mb/`

Readiness before fetch:

- `ready_for_500mb_fetch=true`
- `blockers=0`

## 3. Fetch Result

Command:

```text
.venv/Scripts/python.exe scripts/fetch_fineweb_edu_slice.py --config configs/data/fineweb_edu_sample10bt_500mb.json --retries 2 --timeout-seconds 180
```

Result:

- fetch completed successfully
- bounded slice downloaded: yes
- raw output: `data/public_corpus/fineweb_edu_sample10bt_500mb/raw.jsonl`
- manifest: `data/public_corpus/fineweb_edu_sample10bt_500mb/manifest.json`
- record count: `109130`
- actual text bytes: `524292588`
- reported size: `500.004375 MB`

The fetch log included an unauthenticated Hugging Face request warning and a remote data host reconnect retry message. The command still completed and wrote the expected bounded slice artifacts.

## 4. Raw Validation Summary

Command:

```text
.venv/Scripts/python.exe scripts/validate_fineweb_edu_slice.py --config configs/data/fineweb_edu_sample10bt_500mb.json
```

Summary path:

- `data/public_corpus/fineweb_edu_sample10bt_500mb/validation_summary.json`

Raw validation metrics:

| metric | value |
|---|---:|
| record_count | 109130 |
| total_text_bytes | 524292588 |
| total_file_bytes | 528394421 |
| min_text_chars | 241 |
| max_text_chars | 640136 |
| mean_text_chars | 4779.665976 |
| empty_text_count | 0 |
| duplicate_text_hash_count | 13 |

Source metadata:

| field | value |
|---|---|
| dataset_id | `HuggingFaceFW/fineweb-edu` |
| dataset_config | `sample-10BT` |
| license | `odc-by` |
| allowed_for_training | `true` |

## 5. Intake Result

Command:

```text
.venv/Scripts/python.exe scripts/intake_fineweb_edu_slice.py --config configs/data/fineweb_edu_sample10bt_500mb.json
```

Generated local-only corpus artifacts:

- `data/public_corpus/fineweb_edu_sample10bt_500mb/processed/fineweb_edu_500mb.processed.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl`

Generated committed summary candidate:

- `data/public_corpus/fineweb_edu_sample10bt_500mb/intake_summary.json`

Intake metrics:

| metric | value |
|---|---:|
| processed_count | 109117 |
| train_count | 103619 |
| val_count | 5498 |
| dropped_empty_count | 0 |
| dropped_duplicate_count | 13 |
| total_text_bytes | 524232621 |
| train_text_bytes | 496047319 |
| val_text_bytes | 28185302 |

## 6. Intake Validation Summary

Command:

```text
.venv/Scripts/python.exe scripts/validate_fineweb_edu_intake.py --config configs/data/fineweb_edu_sample10bt_500mb.json
```

Summary path:

- `data/public_corpus/fineweb_edu_sample10bt_500mb/intake_validation_summary.json`

Validation confirmed:

- processed records are valid JSONL objects;
- train and validation splits do not overlap;
- processed `doc_id` values are unique;
- train plus validation `doc_id` sets match the processed set;
- required provenance fields preserve `license=odc-by`, `allowed_for_training=true`, and `source_category=public_pretraining_corpus`.

## 7. Output Basename Fix

MVP-11 identified that the existing intake scripts used 50MB output basenames even though output directories were config-driven.

MVP-11.1 fixes this by deriving output basenames from `config["target_size_mb"]`:

- 50MB config keeps `fineweb_edu_50mb.*` outputs;
- 500MB config now writes `fineweb_edu_500mb.*` outputs.

The fix affects only output filenames. It does not change text normalization, duplicate handling, split seed, split ratio, license handling, `allowed_for_training`, or `source_category` semantics.

## 8. Artifact Policy

Committed or committable small metadata:

- `manifest.json`
- `validation_summary.json`
- `intake_summary.json`
- `intake_validation_summary.json`
- `expansion_readiness_summary.json`
- docs and script fixes

Local-only ignored data artifacts:

- `raw.jsonl`
- `processed/`
- `splits/`

No checkpoint artifacts are created or committed in this step.

## 9. Gitignore Check

Command:

```text
git status --short -- data/public_corpus/fineweb_edu_sample10bt_500mb/
```

Observed status showed only small metadata files:

```text
 M data/public_corpus/fineweb_edu_sample10bt_500mb/expansion_readiness_summary.json
?? data/public_corpus/fineweb_edu_sample10bt_500mb/intake_summary.json
?? data/public_corpus/fineweb_edu_sample10bt_500mb/intake_validation_summary.json
?? data/public_corpus/fineweb_edu_sample10bt_500mb/manifest.json
?? data/public_corpus/fineweb_edu_sample10bt_500mb/validation_summary.json
```

`raw.jsonl`, `processed/`, and `splits/` did not appear in Git status.

## 10. What MVP-11.1 Does Not Do

MVP-11.1 does not:

- train a tokenizer;
- train a model;
- enter A100 or A800;
- modify model code;
- create checkpoints;
- submit raw corpus data;
- submit processed corpus data;
- submit train/validation split data.

## 11. Next Step

Next step: MVP-12 public 16k tokenizer training plan.
