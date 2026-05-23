# MVP-2 FineWeb-Edu Fetch Plan

## 1. Files Added
MVP-2 adds:
- `docs/mvp_2_fineweb_edu_source_decision.md`
- `docs/mvp_2_fineweb_edu_fetch_plan.md`
- `configs/data/fineweb_edu_sample10bt_50mb.json`
- `data/public_corpus/README.md`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/.gitkeep`
- `scripts/fetch_fineweb_edu_slice.py`
- `.gitignore` protection for large public-corpus fetch outputs

## 2. Config
The committed bounded fetch config targets:
- dataset: `HuggingFaceFW/fineweb-edu`
- config: `sample-10BT`
- split: `train`
- streaming: `true`
- target size: `50MB`
- text field: `text`

The config exists to define a controlled first smoke slice for later execution, not to trigger an actual download in MVP-2.

## 3. Fetch Script
The fetch script is a bounded utility that:
- reads the committed config JSON
- prepares a streaming dataset loader call
- supports `--dry-run`
- limits output by accumulated UTF-8 text bytes
- writes `manifest.json` only when a real bounded fetch is intentionally executed later
- prints a concise summary of records, bytes, and output targets

## 4. Dry-run Policy
Dry-run is the default-safe policy for early validation:
- do not write a large `raw.jsonl`
- do not create parquet cache payloads for repository storage
- do not perform a `50MB` fetch in MVP-2
- do not run anything on A100

## 5. Gitignore Policy
The public-corpus line now ignores:
- `raw.jsonl`
- parquet files
- local cache directories
- shard directories

This keeps large fetch artifacts out of Git while still allowing small manifests, docs, config files, and `.gitkeep` skeleton files to remain reviewable.

## 6. Expected Outputs
When a future bounded fetch step is intentionally run, expected outputs are:
- `data/public_corpus/fineweb_edu_sample10bt_50mb/raw.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/manifest.json`

MVP-2 itself does not create those large outputs.

## 7. What MVP-2 Does Not Do
MVP-2 does not:
- download FineWeb-Edu data beyond script syntax validation
- enter A100
- run training
- train a tokenizer
- train a model
- modify model code
- promote this public corpus into another corpus line automatically

## 8. Next Step
Recommended next step:
- run a bounded MVP-3 fetch for the `50MB` FineWeb-Edu slice, inspect the resulting manifest and sample output shape, and only then discuss intake or training-facing follow-up steps
