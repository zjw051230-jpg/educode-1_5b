# Public Corpus Directory

## 1. Purpose

This directory stores bounded public-corpus source skeletons, manifests, summaries, and local-only fetched artifacts for the EduCode-1.5B public-corpus MVP path.

## 2. Current Status

| slice | config | target_size_mb | status | artifact policy |
|---|---|---:|---|---|
| FineWeb-Edu `sample-10BT` 50MB | `configs/data/fineweb_edu_sample10bt_50mb.json` | 50 | fetched and intaked in prior MVP steps | raw, processed, and splits are local-only |
| FineWeb-Edu `sample-10BT` 500MB | `configs/data/fineweb_edu_sample10bt_500mb.json` | 500 | planned, not fetched | raw, processed, and splits are local-only |

The 500MB planned slice exists only as a config, directory skeleton, and readiness summary in MVP-11. No 500MB `raw.jsonl`, `processed/`, or `splits/` artifacts are created in this step.

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

## 5. FineWeb-Edu 500MB Planned Slice

The planned 500MB slice uses:

- dataset: `HuggingFaceFW/fineweb-edu`
- dataset config: `sample-10BT`
- split: `train`
- streaming: `true`
- text field: `text`
- license: `odc-by`
- config path: `configs/data/fineweb_edu_sample10bt_500mb.json`
- output directory: `data/public_corpus/fineweb_edu_sample10bt_500mb/`
- status: planned, not fetched

MVP-11 only prepares this slice. A later MVP-11.1 step may fetch, validate, intake, and review it.

## 6. Scope Guardrails

- public availability does not remove the need for provenance and scope tracking.
- raw corpus data remains local-only by default.
- tokenizer training and model training require separate approved MVP steps.
- no A100 or A800 execution is triggered from this directory by MVP-11.
