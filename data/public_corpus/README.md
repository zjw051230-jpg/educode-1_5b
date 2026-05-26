# Public Corpus Directory

## 1. Purpose

This directory stores bounded public-corpus source skeletons, manifests, summaries, and local-only fetched artifacts for the EduCode-1.5B public-corpus MVP path.

## 2. Current Status

| slice | config | target_size_mb | status | artifact policy |
|---|---|---:|---|---|
| FineWeb-Edu `sample-10BT` 50MB | `configs/data/fineweb_edu_sample10bt_50mb.json` | 50 | fetched and intaked in prior MVP steps | raw, processed, and splits are local-only |
| FineWeb-Edu `sample-10BT` 500MB | `configs/data/fineweb_edu_sample10bt_500mb.json` | 500 | fetched and intaked in MVP-11.1 | raw, processed, and splits are local-only |
| FineWeb-Edu `sample-10BT` 2GB | `configs/data/fineweb_edu_sample10bt_2gb.json` | 2048 | fetched, validated, intaked, and packaged locally in MVP-20 | raw, processed, splits, and prepared tarball are local-only |
| FineWeb-Edu `sample-10BT` 5GB | `configs/data/fineweb_edu_sample10bt_5gb.json` | 5120 | fetched, validated, intaked, and packaged locally in MVP-22.P | raw, processed, splits, and prepared tarball are local-only |

The 500MB slice has been fetched, raw-validated, intaked, and intake-validated. Its raw, processed, and split corpus files remain local-only and ignored by Git.

The 2GB slice has been fetched, raw-validated, intaked, intake-validated, and packaged as local prepared splits for future GPU transfer. Its raw, processed, split, and prepared package artifacts remain local-only and ignored or outside the repository.

The 5GB slice has been fetched, raw-validated, intaked, intake-validated, and packaged as local prepared splits for future GPU transfer. Its raw, processed, split, and prepared package artifacts remain local-only and ignored or outside the repository.

## 3. Directory Layout

Per-source subdirectories may contain:

- committed `.gitkeep` skeleton files;
- small committed `manifest.json` files when later created intentionally;
- small committed validation and intake summary JSON files;
- ignored `raw.jsonl` files for bounded local fetches;
- ignored `processed/` and `splits/` directories for local intake outputs;
- ignored cache, shard, or parquet files when later fetch steps are approved.

## 4. Git Policy

- `raw.jsonl` files must not be committed.
- `processed/` directories must not be committed.
- `splits/` directories must not be committed.
- parquet files, cache directories, and shard directories must stay ignored.
- small manifests, summaries, docs, configs, and `.gitkeep` files may be committed.
- before any public release, re-check this directory for unexpected large artifacts.

## 5. FineWeb-Edu 500MB Slice

The 500MB slice uses:

- dataset: `HuggingFaceFW/fineweb-edu`
- dataset config: `sample-10BT`
- split: `train`
- streaming: `true`
- text field: `text`
- license: `odc-by`
- config path: `configs/data/fineweb_edu_sample10bt_500mb.json`
- output directory: `data/public_corpus/fineweb_edu_sample10bt_500mb/`
- status: fetched and intaked
- manifest path: `data/public_corpus/fineweb_edu_sample10bt_500mb/manifest.json`
- validation summary path: `data/public_corpus/fineweb_edu_sample10bt_500mb/validation_summary.json`
- intake summary path: `data/public_corpus/fineweb_edu_sample10bt_500mb/intake_summary.json`
- intake validation summary path: `data/public_corpus/fineweb_edu_sample10bt_500mb/intake_validation_summary.json`

Local-only ignored artifacts:

- `data/public_corpus/fineweb_edu_sample10bt_500mb/raw.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_500mb/processed/`
- `data/public_corpus/fineweb_edu_sample10bt_500mb/splits/`

## 6. FineWeb-Edu 2GB Slice

The 2GB slice uses:

- dataset: `HuggingFaceFW/fineweb-edu`
- dataset config: `sample-10BT`
- split: `train`
- streaming: `true`
- text field: `text`
- license: `odc-by`
- config path: `configs/data/fineweb_edu_sample10bt_2gb.json`
- output directory: `data/public_corpus/fineweb_edu_sample10bt_2gb/`
- status: fetched, validated, intaked, intake-validated, and packaged locally
- manifest path: `data/public_corpus/fineweb_edu_sample10bt_2gb/manifest.json`
- validation summary path: `data/public_corpus/fineweb_edu_sample10bt_2gb/validation_summary.json`
- intake summary path: `data/public_corpus/fineweb_edu_sample10bt_2gb/intake_summary.json`
- intake validation summary path: `data/public_corpus/fineweb_edu_sample10bt_2gb/intake_validation_summary.json`
- prepared package manifest path: `data/public_corpus/fineweb_edu_sample10bt_2gb/prepared_package_manifest.json`

Local-only ignored artifacts:

- `data/public_corpus/fineweb_edu_sample10bt_2gb/raw.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_2gb/processed/`
- `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/`
- `C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz`

## 7. FineWeb-Edu 5GB Slice

The 5GB slice uses:

- dataset: `HuggingFaceFW/fineweb-edu`
- dataset config: `sample-10BT`
- split: `train`
- streaming: `true`
- text field: `text`
- license: `odc-by`
- config path: `configs/data/fineweb_edu_sample10bt_5gb.json`
- output directory: `data/public_corpus/fineweb_edu_sample10bt_5gb/`
- status: fetched, validated, intaked, intake-validated, and packaged locally
- manifest path: `data/public_corpus/fineweb_edu_sample10bt_5gb/manifest.json`
- validation summary path: `data/public_corpus/fineweb_edu_sample10bt_5gb/validation_summary.json`
- intake summary path: `data/public_corpus/fineweb_edu_sample10bt_5gb/intake_summary.json`
- intake validation summary path: `data/public_corpus/fineweb_edu_sample10bt_5gb/intake_validation_summary.json`
- prepared package manifest path: `data/public_corpus/fineweb_edu_sample10bt_5gb/prepared_package_manifest.json`

Local-only ignored artifacts:

- `data/public_corpus/fineweb_edu_sample10bt_5gb/raw.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/processed/`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/`
- `C:/Users/01/fineweb_edu_5gb_prepared_splits.tar.gz`

## 8. Scope Guardrails

- public availability does not remove the need for provenance and scope tracking.
- raw corpus data remains local-only by default.
- tokenizer training and model training require separate approved MVP steps.
- no A100 or A800 execution is triggered from this directory by MVP-11.1.
