# MVP-11 FineWeb-Edu 500MB Public Corpus Expansion Plan

## 1. Purpose

Expand from the reviewed 50MB public corpus slice to a bounded 500MB FineWeb-Edu public slice so the project has a stronger data substrate for the public 16k tokenizer step and a later 300M 1000-step bounded run.

This MVP-11 step is planning and readiness only. It creates the 500MB config, directory skeleton, artifact policy, readiness check, and execution checklist.

## 2. Why 500MB Before More Training

The 50MB FineWeb-Edu slice has already proven the public-corpus training systems path: fetch, intake, batching, model materialization, loss, optimizer step, checkpoint save, and checkpoint reload all worked across the A800 10-step and 100-step runs.

Continuing directly to a 1000-step run on the same 50MB corpus would mostly stress a tiny dataset and could test overfitting more than a useful generalization path. A 500MB slice remains bounded and reviewable, but it is materially better suited for tokenizer training and longer public-corpus training than the current smoke-scale slice.

The recommended sequence is therefore:
1. expand the public corpus to 500MB;
2. train a public 16k tokenizer after the larger public slice is reviewed;
3. run the 300M 1000-step bounded training step on the larger public-corpus path.

## 3. Source

- dataset: `HuggingFaceFW/fineweb-edu`
- dataset config: `sample-10BT`
- split: `train`
- license: `odc-by`
- text field: `text`
- streaming: `true`
- target size: `500MB`
- config: `configs/data/fineweb_edu_sample10bt_500mb.json`
- planned output directory: `data/public_corpus/fineweb_edu_sample10bt_500mb/`

## 4. Artifact Policy

The 500MB corpus artifacts are local-only unless they are small metadata summaries:

- `raw.jsonl` is not committed.
- `processed/` is not committed.
- `splits/` is not committed.
- `manifest.json` may be committed after fetch.
- `validation_summary.json` may be committed after raw validation.
- `intake_summary.json` may be committed after intake.
- `intake_validation_summary.json` may be committed after intake validation.
- checkpoints are unrelated to MVP-11 and must not be created or committed here.
- local corpus artifacts are rebuildable from the config and scripts.

The `.gitignore` policy covers `raw.jsonl`, parquet files, cache directories, shard directories, `processed/`, and `splits/` under `data/public_corpus/*/`.

## 5. Execution Plan

The next execution step is MVP-11.1:

1. fetch the bounded 500MB FineWeb-Edu slice;
2. validate the raw JSONL slice;
3. run public-corpus intake;
4. validate the processed and split intake outputs;
5. record `manifest.json`, `validation_summary.json`, `intake_summary.json`, and `intake_validation_summary.json`;
6. keep tokenizer training out of MVP-11.1;
7. keep model training out of MVP-11.1.

MVP-11.1 should start by running `scripts/check_fineweb_edu_500mb_expansion_readiness.py` and confirming `ready_for_500mb_fetch=true` with `blockers=0`.

## 6. Expected Outputs

MVP-11.1 is expected to produce these local data artifacts and small summaries:

- `data/public_corpus/fineweb_edu_sample10bt_500mb/raw.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_500mb/manifest.json`
- `data/public_corpus/fineweb_edu_sample10bt_500mb/validation_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_500mb/processed/fineweb_edu_500mb.processed.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_500mb/intake_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_500mb/intake_validation_summary.json`

Only the small metadata and summary files should be committed. The raw, processed, and split corpus files remain local-only.

## 7. Risks

- Hugging Face network instability may interrupt or slow streaming fetches.
- Local disk usage is higher than the 50MB slice because raw plus processed plus split files coexist during review.
- `raw.jsonl`, `processed/`, or `splits/` could be accidentally committed if ignore rules are bypassed.
- Duplicate text or very long documents may affect the usefulness of the bounded slice.
- 500MB is still small relative to serious pretraining and should not be treated as a final corpus scale.

## 8. Stop Conditions

Stop MVP-11.1 if any of these occur:

- `raw.jsonl` appears in `git status` as a trackable file.
- Local disk space is insufficient.
- The fetch fails repeatedly after bounded retries.
- Raw JSONL validation fails.
- Empty text count is high.
- Duplicate rate is unexpectedly high.
- Any generated data file appears outside the planned `fineweb_edu_sample10bt_500mb/` directory.

## 9. What MVP-11 Does Not Do

MVP-11 does not:

- fetch data;
- download data;
- run intake;
- train a tokenizer;
- train a model;
- enter A100 or A800;
- modify model code;
- create checkpoints.

## 10. Next Step

Next step: MVP-11.1 FineWeb-Edu 500MB fetch and intake.
