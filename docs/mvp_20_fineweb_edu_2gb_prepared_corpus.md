# MVP-20 FineWeb-Edu 2GB Prepared Corpus

## Purpose

MVP-20 prepares a bounded `2GB` FineWeb-Edu `sample-10BT` public corpus slice locally/CPU-side for future A800/A100 streaming training experiments.

This step does not enter A100/A800, run model training, train a tokenizer, change model code, advance the D20/E corpus lines, or commit raw/processed/split corpus data.

## Inputs

| field | value |
|---|---|
| config | `configs/data/fineweb_edu_sample10bt_2gb.json` |
| dataset_id | `HuggingFaceFW/fineweb-edu` |
| dataset_config | `sample-10BT` |
| split | `train` |
| target_size_mb | `2048` |
| license | `odc-by` |
| local output dir | `data/public_corpus/fineweb_edu_sample10bt_2gb/` |

## Fetch Result

The bounded fetch completed locally with exit code `0`.

| metric | value |
|---|---:|
| raw record_count | `449802` |
| raw total_text_bytes | `2147485975` |
| raw total_file_bytes | `2164293095` |
| raw empty_text_count | `0` |
| raw duplicate_text_hash_count | `434` |
| min_text_chars | `208` |
| max_text_chars | `640136` |
| mean_text_chars | `4749.868162` |

The fetch emitted a Hugging Face unauthenticated-request warning and one remote-host disconnect retry message, but the command completed and raw validation passed.

## Intake Result

| metric | value |
|---|---:|
| processed_count | `449367` |
| train_count | `426857` |
| val_count | `22510` |
| dropped_empty_count | `0` |
| dropped_duplicate_count | `435` |
| total_text_bytes | `2145535856` |
| train_text_bytes | `2036973656` |
| val_text_bytes | `108562200` |

Generated output basenames are `fineweb_edu_2gb`:

- `data/public_corpus/fineweb_edu_sample10bt_2gb/processed/fineweb_edu_2gb.processed.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.val.jsonl`

## Validation Artifacts

Small committed metadata artifacts:

- `data/public_corpus/fineweb_edu_sample10bt_2gb/manifest.json`
- `data/public_corpus/fineweb_edu_sample10bt_2gb/validation_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_2gb/intake_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_2gb/intake_validation_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_2gb/prepared_package_manifest.json`

Ignored local-only corpus artifacts:

- `data/public_corpus/fineweb_edu_sample10bt_2gb/raw.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_2gb/processed/`
- `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/`

## Prepared Package

Local package path:

```text
C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz
```

Package metadata:

| field | value |
|---|---|
| package_size_bytes | `847344882` |
| package_sha256 | `1c02cdf74e5a883ac1fcbee2cb9ebcf5917b8de145aaf4bdc59b1da6c120d51a` |
| committed manifest | `data/public_corpus/fineweb_edu_sample10bt_2gb/prepared_package_manifest.json` |

Package members:

- `manifest.json`
- `validation_summary.json`
- `intake_summary.json`
- `intake_validation_summary.json`
- `splits/fineweb_edu_2gb.train.jsonl`
- `splits/fineweb_edu_2gb.val.jsonl`

The package excludes `raw.jsonl` and `processed/`.

## Git Boundary

The following ignore rules protect large artifacts:

- `data/public_corpus/*/raw.jsonl`
- `data/public_corpus/*/processed/`
- `data/public_corpus/*/splits/`
- `data/public_corpus/*/*.tar.gz`

`git check-ignore` confirmed the 2GB raw, processed, train split, and val split paths are ignored.

## Interpretation

This is a data-preparation milestone, not model-quality evidence. The next useful step is to create a 2GB-specific A800/A100 streaming training config and run a bounded 300M public16k experiment only after explicit GPU execution approval.
