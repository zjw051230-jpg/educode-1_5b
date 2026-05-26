# MVP-24 Modal 5GB 1000-Step Training Runbook

## Purpose

Prepare the exact command and artifact boundary for a future Modal A100 5GB 1000-step streaming training run.

This document is a runbook only. It does not approve cost, run Modal, enter A100/A800, or start training.

## Current Gate Status

The `preflight_5gb_1000` mode has already passed on Modal with:

| field | value |
|---|---|
| repo commit | `16f4cd6` |
| GPU requested | `A100-40GB` |
| config | `configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json` |
| prepared package | `/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz` |
| memory plan | success |
| dry-run | success |
| readiness | success |
| blockers | `[]` |
| ran training | false |
| produced checkpoint | false |

The next executable mode is `train_5gb_1000`, but it must run only after explicit cost approval.

## Required Repo Commit

Use repo commit `16f4cd6` or later. The Modal runner verifies that required history contains `16f4cd6`.

## Required Modal Volume Package

The training mode requires this package to already exist in Modal Volume `educode-data`:

```text
/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz
```

The package should extract to:

```text
data/public_corpus/fineweb_edu_sample10bt_5gb/
```

The runner verifies these extracted files before training:

- `data/public_corpus/fineweb_edu_sample10bt_5gb/manifest.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/validation_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/intake_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/intake_validation_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl`

## Cost Gate

Do not run the training command until the user explicitly approves the Modal runtime cost for this run.

Expected planning cost remains bounded, but actual cost depends on Modal runtime, queue behavior, and current pricing.

## Training Command To Run Later

Run only after explicit cost approval:

```bash
modal run scripts/modal_a100_streaming_runner.py --mode train_5gb_1000
```

The mode uses:

- config: `configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json`
- prepared package: `/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz`
- result dir: `/vol/results/modal_train_5gb_1000`
- result package: `/vol/results/mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz`

## Result Package Policy

The training mode packages only small result files:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`

The package must not include:

- checkpoints
- `raw.jsonl`
- `processed/`
- `splits/`
- prepared package tarballs
- model weights
- Modal tokens or credentials

## Download Command After Training

After the future training job completes, download only the small result package:

```powershell
modal volume get educode-data /results/mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz C:\Users\01\mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz
```

## Copy To Project Root

Copy the downloaded result package into the project root for the later import step:

```powershell
copy C:\Users\01\mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz D:\模型\educode-1_5b\mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz
```

Do not download checkpoints by default. Do not commit the result package.

## Expected Receipt Semantics

A successful future `train_5gb_1000` receipt should include:

- `mode=train_5gb_1000`
- `ran_training=true`
- `produced_checkpoint=true`
- `config_path=configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json`
- `prepared_package=/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz`
- `result_package=/vol/results/mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz`

## Stop Conditions

Stop before training if:

- cost is not explicitly approved;
- the Volume package is missing;
- any required package member is missing after extraction;
- memory inspection fails;
- dry-run fails;
- readiness reports blockers;
- the command would fetch Hugging Face data on the GPU worker.
