# MVP-22.P FineWeb-Edu 5GB Prepared Corpus Result

## Purpose

MVP-22.P expands the bounded FineWeb-Edu `sample-10BT` public-corpus preparation path from 2GB to 5GB, locally/CPU-side, for future A800/A100 public16k streaming runs.

This step did not enter A800/A100, run model training, train a tokenizer/model, change model architecture, create checkpoints, or commit raw/processed/split corpus data.

## Disk Gate

The local disk gate passed before fetch: D: had approximately `248.93 GiB` free, above the `80GB` threshold required for 5GB fetch/intake/package execution.

## Inputs

| field | value |
|---|---|
| config | `configs/data/fineweb_edu_sample10bt_5gb.json` |
| dataset_id | `HuggingFaceFW/fineweb-edu` |
| dataset_config | `sample-10BT` |
| split | `train` |
| target_size_mb | `5120` |
| license | `odc-by` |
| local output dir | `data/public_corpus/fineweb_edu_sample10bt_5gb/` |

## Fetch Result

The bounded fetch completed locally with exit code `0`.

| metric | value |
|---|---:|
| raw record_count | `1127093` |
| raw total_text_bytes | `5368710356` |
| raw total_file_bytes | `5410614440` |
| raw empty_text_count | `0` |
| raw duplicate_text_hash_count | `4431` |
| min_text_chars | `174` |
| max_text_chars | `640136` |
| mean_text_chars | `4738.822347` |

The fetch emitted a Hugging Face unauthenticated-request warning and one remote-host disconnect retry message, but the command completed and raw validation passed.

## Intake Result

| metric | value |
|---|---:|
| processed_count | `1122642` |
| train_count | `1066882` |
| val_count | `55760` |
| dropped_empty_count | `0` |
| dropped_duplicate_count | `4451` |
| total_text_bytes | `5348612719` |
| train_text_bytes | `5080485686` |
| val_text_bytes | `268127033` |

Generated output basenames are `fineweb_edu_5gb`:

- `data/public_corpus/fineweb_edu_sample10bt_5gb/processed/fineweb_edu_5gb.processed.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl`

## Validation Artifacts

Small committed metadata artifacts:

- `data/public_corpus/fineweb_edu_sample10bt_5gb/manifest.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/validation_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/intake_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/intake_validation_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/prepared_package_manifest.json`

Ignored local-only corpus artifacts:

- `data/public_corpus/fineweb_edu_sample10bt_5gb/raw.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/processed/`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/`

## Prepared Package

Local package path:

```text
C:/Users/01/fineweb_edu_5gb_prepared_splits.tar.gz
```

Package metadata:

| field | value |
|---|---|
| package_size_bytes | `2112167310` |
| package_sha256 | `19a933ec5afc379d58751461ff56e8e89be4d3fbfc05e10df789c6541f8bcd5d` |
| committed manifest | `data/public_corpus/fineweb_edu_sample10bt_5gb/prepared_package_manifest.json` |

Package members:

- `manifest.json`
- `validation_summary.json`
- `intake_summary.json`
- `intake_validation_summary.json`
- `splits/fineweb_edu_5gb.train.jsonl`
- `splits/fineweb_edu_5gb.val.jsonl`

The package excludes `raw.jsonl` and `processed/`.

## Git Boundary

`git check-ignore` confirmed these 5GB local artifact paths are ignored:

- `data/public_corpus/fineweb_edu_sample10bt_5gb/raw.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/processed/fineweb_edu_5gb.processed.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/fineweb_edu_5gb_prepared_splits.tar.gz`

## Interpretation

This is a data-preparation and GPU-logistics milestone. It supports future 5GB public16k streaming execution, but it is not model-quality evidence and does not imply full pretraining.
