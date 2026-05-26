# MVP-26.P Modal Backend Adapter Plan

## Purpose

Prepare Modal as an alternate A100/A100-40GB execution backend for EduCode-1.5B public16k streaming runs, without running training in this step.

MVP-26.P creates local Modal adapter scaffolding, data-volume policy, a remote runbook, and a preflight receipt template. It does not train a model/tokenizer, create checkpoints, push Git, or commit raw/processed/split corpus artifacts.

## Why Modal

Current direct GPU provider capacity is not available, so Modal gives a separate on-demand GPU execution path. The goal is to reuse the already validated local data/config/training pipeline while moving only the execution environment to Modal.

Modal is useful here because:

- A100/A100-40GB jobs can be launched as explicit one-off commands;
- Modal Volume can hold prepared data packages and small result packages;
- GPU functions can run bounded preflight commands before any training command;
- no persistent app, warm pool, or always-on service is required.

## What Modal Will Run

Modal will first run preflight for the 2GB public16k 1000-step config:

```text
configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json
```

The preflight job will:

1. clone `https://github.com/zjw051230-jpg/educode-1_5b.git` into `/workspace/educode-1_5b`;
2. checkout/pull `main`;
3. verify history includes `66b00b9` or a later main commit containing it;
4. extract the prepared data package from Modal Volume;
5. verify train/val split paths exist;
6. run memory inspection;
7. run dry-run config/model/tokenizer validation;
8. run execution readiness;
9. copy only small summary JSON files to Modal Volume results.

Training modes are present only for explicit later invocation. They must not be run by default.

## What Remains Local

Local remains responsible for:

- preparing bounded public-corpus packages;
- validating raw/intake summaries;
- keeping prepared tarballs outside Git;
- reviewing and importing small result packages after execution;
- deciding whether to advance from 2GB to 5GB.

Local prepared package paths:

```text
C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz
C:/Users/01/fineweb_edu_5gb_prepared_splits.tar.gz
```

## Data Package Strategy

Modal GPU functions must not fetch FineWeb-Edu from Hugging Face. Prepared packages are uploaded from local Windows storage to Modal Volume before any remote GPU job.

Recommended first package:

```text
C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz
```

5GB standby package:

```text
C:/Users/01/fineweb_edu_5gb_prepared_splits.tar.gz
```

Execution order stays conservative: run 2GB 1000-step preflight first, then later 2GB 1000-step training only after explicit approval. Do not jump directly to 5GB.

## Modal Volume Strategy

Use one Modal Volume:

```text
educode-data
```

Volume layout:

```text
/prepared/   prepared split packages uploaded from local machine
/results/    small preflight/training result packages for download
/checkpoints/ temporary checkpoint area if a later explicit training run needs it
```

Checkpoints should remain in Modal or be discarded by default. They should not be downloaded unless a later step explicitly approves checkpoint transfer.

## GPU Choice

Default Modal GPU target is A100-40GB, with A100 as the intended family. The runner should use one explicit Modal job at a time and should not configure persistent deployment, warm containers, or minimum containers.

## Preflight First, Training Later

MVP-26.P prepares these modes:

- `preflight_2gb_1000` as the default and primary mode;
- `train_2gb_1000` for later explicit training;
- `train_2gb_3000` for later explicit follow-up only after 1000-step success;
- `preflight_5gb_1000` for later data-scale preflight after the 2GB route is validated.

This step should not run a remote Modal job by default and should not run training.

## Credential Policy

- Do not write Modal tokens into code, docs, configs, shell history snippets, or Git.
- Do not ask the user to paste a Modal token into chat.
- Use `modal setup` locally for authentication.
- Keep Modal auth state in the user's local Modal configuration, not in this repository.

Local setup commands:

```bash
python -m pip install -U modal
modal setup
```

If Modal CLI is missing or not authenticated, record it as pending setup and stop before remote execution.

## Stop Conditions

Stop before running a Modal job if any of these occur:

- Git `main` is ahead/behind remote;
- latest pushed commit `66b00b9` is missing from history;
- Modal CLI is unavailable;
- Modal auth is unavailable;
- prepared package is missing locally or in Modal Volume;
- command would fetch Hugging Face data from the GPU function;
- command would write credentials to the repo;
- command would download checkpoints by default;
- user has not explicitly approved a training mode.

Stop during preflight if any of these occur:

- repo clone or checkout fails;
- commit history does not include `66b00b9`;
- prepared package extraction fails;
- train/val splits are missing;
- memory inspection fails;
- dry-run fails;
- readiness reports blockers.
