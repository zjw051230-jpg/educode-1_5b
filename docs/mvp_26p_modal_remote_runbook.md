# MVP-26.P Modal Remote Runbook

## Purpose

Run EduCode-1.5B public16k streaming preflight on Modal A100/A100-40GB using prepared data packages in Modal Volume. Training commands are documented for later explicit approval only.

## Local Setup

From the project root:

```bash
python -m pip install -U modal
modal setup
```

Do not paste Modal tokens into chat or commit credentials to Git.

## Modal Auth

Check the active Modal profile locally:

```bash
modal profile current
```

If this fails, run `modal setup` locally. Do not write tokens into repository files.

## Create Volume

```bash
modal volume create educode-data
```

## Upload 2GB Package

Upload the first package for preflight/training:

```bash
modal volume put educode-data C:\Users\01\fineweb_edu_2gb_prepared_splits.tar.gz /prepared/fineweb_edu_2gb_prepared_splits.tar.gz
```

## Optional Upload 5GB Package

Upload only as standby. Do not start with 5GB execution:

```bash
modal volume put educode-data C:\Users\01\fineweb_edu_5gb_prepared_splits.tar.gz /prepared/fineweb_edu_5gb_prepared_splits.tar.gz
```

## Run Preflight

Default safe command:

```bash
modal run scripts/modal_a100_streaming_runner.py --mode preflight_2gb_1000
```

Expected preflight behavior:

- clone the GitHub repo into `/workspace/educode-1_5b`;
- checkout/pull `main`;
- verify history includes `66b00b9`;
- extract `/vol/prepared/fineweb_edu_2gb_prepared_splits.tar.gz`;
- verify 2GB train/val splits;
- run memory inspection;
- run dry-run;
- run readiness;
- copy small summaries to `/vol/results/modal_preflight_2gb_1000/`.

Expected preflight outputs:

- `batch_memory_plan_summary.json`
- `dry_run_summary.json`
- `execution_readiness_summary.json`
- `modal_preflight_receipt.json`

## Training Command To Run Later

Run only after explicit approval and successful preflight:

```bash
modal run scripts/modal_a100_streaming_runner.py --mode train_2gb_1000
```

Follow-up training command only after 1000-step success:

```bash
modal run scripts/modal_a100_streaming_runner.py --mode train_2gb_3000
```

5GB preflight command only after the 2GB route supports moving up in data scale:

```bash
modal run scripts/modal_a100_streaming_runner.py --mode preflight_5gb_1000
```

## Result Download Policy

Download only small result artifacts from `/results/`.

Template:

```bash
modal volume get educode-data /results/mvp21_a100_2gb_1000step_public16k_streaming_results.tar.gz C:\Users\01\mvp21_a100_2gb_1000step_public16k_streaming_results.tar.gz
```

Do not download checkpoints by default. Do not import prepared packages, raw corpus files, processed files, or split files into Git.

## Cost Safety

- Do not deploy a persistent app for MVP-26.P.
- Do not configure warm containers.
- Do not set minimum containers.
- Run one explicit Modal job at a time.
- Run preflight before training.
- Stop on readiness blockers.

## Stop Conditions

Stop before remote execution if Modal CLI/auth is unavailable, the prepared package is not uploaded, Git history does not include `66b00b9`, or the command would fetch Hugging Face data on the GPU function.

Stop before training if preflight fails, readiness has blockers, train/val splits are missing, or the user has not explicitly approved the training mode.
