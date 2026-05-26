# MVP-22.R Modal A100 2GB 3000-Step Streaming Run

## Purpose

Record and validate the imported result artifacts from the Modal `train_2gb_3000` execution path for the EduCode-1.5B public16k 300M-class streaming run.

This report is training-systems evidence for the Modal backend, prepared-data transfer path, streaming iterator, run logging, validation logging, checkpoint reload check, and post-run artifact validator over a bounded 3000-step run.

## Modal Backend

The run used Modal as an alternate remote execution backend with requested GPU `A100-40GB`. The imported run metadata reports:

| field | value |
|---|---|
| Modal mode | `train_2gb_3000` |
| GPU requested | `A100-40GB` |
| Runtime GPU | `NVIDIA A100-SXM4-40GB` |
| Runtime device | `cuda` |
| Runtime dtype | `bf16` |
| Modal volume | `educode-data` |
| Modal job status | completed |
| Training status | success |
| repo commit | `8e92c81` |

## Data Package

The run used the prepared 2GB FineWeb-Edu split package uploaded to Modal Volume:

```text
/vol/prepared/fineweb_edu_2gb_prepared_splits.tar.gz
```

The Modal/GPU worker did not fetch Hugging Face data. The training script consumed extracted prepared train/val splits from the Volume-backed package.

## Config

| field | value |
|---|---|
| config path | `configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json` |
| data_loading_mode | `streaming` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| sequence_length | `512` |
| max_steps | `3000` |
| eval_interval | `300` |
| tokenizer_vocab_size | `16384` |
| exact_parameter_count | `336106496` |

## Training Result

| metric | value |
|---|---|
| run_id | `20260526_165916_fineweb_edu_2gb_300m_3000step_public16k_execute` |
| success | `true` |
| first_train_loss | `9.864925` |
| final_train_loss | `3.156151` |
| final_val_loss | `9.043165` |
| loss_all_finite | `true` |
| val_loss_all_finite | `true` |
| grad_all_finite | `true` |
| metrics_rows | `3000` |
| validation_rows | `10` |
| tokens_seen | `49152000` |
| elapsed_seconds | `1043.828751` |
| approximate_tokens_per_sec | `47088.183726` |
| checkpoint_reload_match | `true` |

## Artifact Validation

Imported files are stored under:

```text
experiments/a100/fineweb_edu_2gb_300m_3000step_public16k_execute/results_imported_modal_streaming/
```

Imported files:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`
- `import_validation_summary.json`

Local import validation command:

```bash
.venv/Scripts/python.exe scripts/validate_mvp22_modal_a100_2gb_3000step_imported_results.py
```

Validation result:

| field | value |
|---|---|
| validation_status | `passed` |
| blocker_count | `0` |
| metrics_rows_actual | `3000` |
| validation_rows_actual | `10` |
| post_run_artifact_validation | `passed` |

## Checkpoint Policy

The remote training run produced a checkpoint and verified reload match remotely:

```text
experiments/a100/fineweb_edu_2gb_300m_3000step_public16k_execute/checkpoints/checkpoint_step_3000.pt
```

The checkpoint was not downloaded and is not committed. This repository import includes only small result artifacts and validation summaries.

## Cost/Runtime Note

The Modal GPU job completed and may have incurred A100-40GB runtime cost for the successful 3000-step training execution. The Modal Volume continues to consume storage until the uploaded prepared package or the Volume itself is deleted.

## What This Proves

- Modal A100-40GB can execute the prepared-data public16k streaming training path for a bounded 3000-step run.
- The Modal backend can consume the prepared 2GB package from Volume without Hugging Face fetch on the GPU worker.
- The 300M-class config runs for 3000 bounded steps with `batch_size=8` and `gradient_accumulation_steps=4` in streaming mode.
- Metrics logging, validation logging, summary generation, checkpoint reload validation, and post-run artifact validation completed successfully.
- The imported result package can be validated locally without rerunning training.

## What This Does Not Prove

- This is not a model-quality claim.
- This is not full pretraining.
- This does not validate 5000-step, 5GB, or larger-corpus Modal runs.
- This does not prove generalization or downstream task performance.
- This does not change the current caveat that scheduler fields are recorded but not applied in the current training script.

## Next Step

Use this successful 2GB 3000-step Modal result as the gate for the next explicit decision. The next reasonable execution path is either to stop and summarize the 1000/3000-step Modal evidence or consider a longer bounded follow-up only after confirming cost budget, Volume state, and explicit approval to run another remote training job.
