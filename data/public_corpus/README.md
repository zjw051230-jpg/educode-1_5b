# Public Corpus Directory

## 1. Purpose
This directory is reserved for bounded public-corpus source planning and future controlled fetches for the EduCode-1.5B A100 MVP.

## 2. Current Status
- This directory currently contains structure only.
- No public corpus slice has been downloaded in MVP-2.
- No `raw.jsonl` has been created in MVP-2.
- No A100 execution has been run from this directory in MVP-2.

## 3. Directory Layout

Per-source subdirectories may contain:
- committed `.gitkeep` skeleton files
- small committed `manifest.json` files when later created intentionally
- ignored `raw.jsonl` files for bounded local fetches
- ignored cache/shard/parquet files when later fetch steps are approved

## 4. Git Policy
- large fetched files should not be committed by default
- `raw.jsonl`, parquet files, cache directories, and shard directories should stay ignored
- small manifests, docs, configs, and `.gitkeep` files may be committed
- before any public release, re-check this directory for unexpected large artifacts

## 5. Scope Guardrails
- public availability does not remove the need for provenance and scope tracking
- MVP-2 is planning and config only
- no tokenizer training or model training is run from this directory in MVP-2
