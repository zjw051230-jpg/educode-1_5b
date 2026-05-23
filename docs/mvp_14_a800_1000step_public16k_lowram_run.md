# MVP-14 A800 1000-step Public16k Low-RAM Run

## Purpose

MVP-14 records the imported A800 `300M` public16k `1000-step` low-host-RAM fallback run.

This was a real remote A800 training-systems execution, but the imported local artifacts are review artifacts only. Checkpoints were not downloaded and must not be committed.

## Imported Artifacts

| field | value |
|---|---|
| import_dir | `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/results_imported_lowram` |
| result package | `mvp14_a800_1000step_public16k_lowram_results.tar.gz` |
| run_id | `20260524_050841_fineweb_edu_500mb_300m_1000step_public16k_execute` |
| run_name | `fineweb_edu_500mb_300m_1000step_public16k_execute` |
| validation status | `passed` |

Imported files:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`
- `import_validation_summary.json`

## Run Configuration Observed

| field | value |
|---|---:|
| runtime_device | `cuda` |
| runtime_dtype | `bf16` |
| exact_parameter_count | `336106496` |
| max_steps | `1000` |
| batch_size | `1` |
| gradient_accumulation_steps | `1` |
| sequence_length | `512` |
| tokens_seen | `512000` |
| tokenizer_vocab_size | `16384` |

This was a low-host-RAM fallback run. It was not the original planned `batch_size=8` / `gradient_accumulation_steps=4` execution.

## Result Summary

| metric | value |
|---|---:|
| first_train_loss | `9.873169` |
| final_train_loss | `0.213472` |
| final_val_loss | `11.513049` |
| metrics_rows | `1000` |
| validation_rows | `10` |
| loss_all_finite | `true` |
| val_loss_all_finite | `true` |
| grad_all_finite | `true` |
| checkpoint_reload_match | `true` |
| post_run_artifact_validation.passed | `true` |

`validation_metrics.jsonl` was written as a standalone artifact and imported locally.

## Import Validation

Command:

```text
.venv/Scripts/python.exe scripts/validate_a800_lowram_imported_results.py
```

Observed for MVP-14:

| field | value |
|---|---|
| validation_status | `passed` |
| blocker_count | `0` |
| metrics_rows_actual | `1000` |
| validation_rows_actual | `10` |

## Caveats

- The original `batch_size=8` / `gradient_accumulation_steps=4` plan and intermediate fallback attempts were killed by the current `16GiB` container RAM limit.
- GPU memory was not the bottleneck; the limiting resource was host/container RAM.
- The successful run used `batch_size=1` and `gradient_accumulation_steps=1`, so it is not throughput-equivalent to the planned configuration.
- Very low train loss with high validation loss indicates overfitting and bounded-prefix memorization risk.
- This result supports training-systems, logging, checkpoint, reload, and artifact-validation claims only.
- It does not support model-quality or generalization claims.

## Artifact Policy

Checkpoint path was recorded in the remote summary, but the checkpoint file was not downloaded or committed.

Do not commit:

- checkpoints;
- raw corpus files;
- processed corpus files;
- split corpus files;
- result tarballs.

## Next Step

Use this result as the primary gate evidence for MVP-14. The next GPU rental should use `32GB+` host/container RAM, preferably `48GB` or `64GB`, before retrying larger host-side batch preparation.
