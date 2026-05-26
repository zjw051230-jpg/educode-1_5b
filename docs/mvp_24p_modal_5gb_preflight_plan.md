# MVP-24.P Modal 5GB Preflight Plan

## Purpose

Prepare the next Modal 5GB preflight route without starting training by default.

This plan uses the prepared local 5GB FineWeb-Edu split package and Modal Volume. It keeps GPU workers from fetching Hugging Face data during paid execution.

## Prepared Package

Use this Modal Volume path:

```text
/prepared/fineweb_edu_5gb_prepared_splits.tar.gz
```

Local source package:

```text
C:\Users\01\fineweb_edu_5gb_prepared_splits.tar.gz
```

Known local package metadata from the prepared corpus stage:

| field | value |
|---|---|
| package size | about `2.1GB` |
| SHA-256 | `19a933ec5afc379d58751461ff56e8e89be4d3fbfc05e10df789c6541f8bcd5d` |
| excluded from Git | yes |

## Upload Command

Upload only when ready to run 5GB preflight:

```bash
modal volume put educode-data C:\Users\01\fineweb_edu_5gb_prepared_splits.tar.gz /prepared/fineweb_edu_5gb_prepared_splits.tar.gz
```

Do not paste Modal tokens into chat or repository files.

## Volume Cost Estimate

Uploading the 5GB prepared package adds about `2.1GB` to Modal Volume storage.

Estimated incremental storage cost:

```text
2.1 GiB × $0.09/GiB/month ≈ $0.19/month
```

This is in addition to the existing 2GB prepared package and small result packages.

## Preflight Mode

Use the existing Modal runner mode:

```bash
modal run scripts/modal_a100_streaming_runner.py --mode preflight_5gb_1000
```

This mode should:

- clone the repository;
- verify required commit history;
- extract `/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz`;
- verify the 5GB train/val split paths;
- run memory inspection;
- run dry-run;
- run readiness checks;
- copy small summaries to `/vol/results/modal_preflight_5gb_1000/`.

## Expected Outputs

Expected Modal Volume output directory:

```text
/results/modal_preflight_5gb_1000/
```

Expected files:

- `batch_memory_plan_summary.json`
- `dry_run_summary.json`
- `execution_readiness_summary.json`
- `modal_preflight_receipt.json`

## No Training By Default

`preflight_5gb_1000` must not run training and must not produce checkpoints. It is a readiness gate only.

Training should run only after:

1. the 5GB prepared package is uploaded;
2. preflight completes successfully;
3. readiness reports no blockers;
4. cost is explicitly approved;
5. the user explicitly approves a training mode.

## Stop Conditions

Stop before 5GB training if:

- the 5GB package is missing from Volume;
- extraction fails;
- train/val splits are missing;
- memory inspection fails;
- dry-run fails;
- readiness has blockers;
- the command would fetch Hugging Face data on the GPU worker;
- the user has not explicitly approved training.
