# MVP-24 Modal A100 5GB 1000-step Streaming Run

## Scope

This document records the imported Modal A100 result for `train_5gb_1000` using the 5GB FineWeb-Edu prepared-data package, the public 16k tokenizer, the 300M-class EduCode model configuration, streaming data loading, shuffle-buffer train sampling, and constant scheduler metadata.

This local import step did not run Modal, did not enter A100/A800, did not run training, did not train tokenizer/model, did not download data, and did not import or stage checkpoints, raw corpus files, processed files, splits, prepared tarballs, or result tarballs.

## Source result package

| Field | Value |
| --- | --- |
| Local package | `mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz` |
| Modal result package | `/vol/results/mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz` |
| Modal mode | `train_5gb_1000` |
| GPU requested | `A100-40GB` |
| Volume | `educode-data` |
| Required runner commit | `16f4cd6` |
| Reported repo commit | `5c7c1b5` |

Only the approved small result artifacts were extracted into:

```text
experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_streaming/
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

## Run metadata

| Field | Value |
| --- | --- |
| Run ID | `20260526_192023_fineweb_edu_5gb_300m_1000step_public16k_execute` |
| Hostname | `modal` |
| Runtime device | `cuda` |
| Runtime dtype | `bf16` |
| GPU | `NVIDIA A100-SXM4-40GB` |
| GPU memory | `39.494 GiB` |
| Python | `3.11.12` |
| Torch | `2.12.0+cu130` |
| CUDA | `13.0` |
| Git commit | `5c7c1b594d1191e198eb5609a0b74024c8c4130a` |
| Git branch | `main` |
| Start time | `2026-05-26T19:20:23` |
| End time | `2026-05-26T19:26:16` |
| Status | `success` |

## Configuration and data path

| Field | Value |
| --- | --- |
| Config | `configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json` |
| Output dir | `experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute` |
| Data loading mode | `streaming` |
| Host RAM efficient batching | `true` |
| Batch precompute disabled | `true` |
| Batch size | `8` |
| Sequence length | `512` |
| Gradient accumulation steps | `4` |
| Max steps | `1000` |
| Eval interval | `100` |
| Tokenizer vocab size | `16384` |
| Exact parameter count | `336106496` |

The Modal worker confirmed that the prepared package was available at:

```text
/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz
```

The reported train and validation paths existed on the Modal worker, and the run used streaming batches rather than local full-corpus materialization.

## Sampling and scheduler metadata

| Field | Value |
| --- | --- |
| Train sampling policy | `shuffle_buffer` |
| Validation sampling policy | `sequential_prefix` |
| Summary sampling policy | `shuffle_buffer` |
| Shuffle seed | `1337` |
| Shuffle buffer size | `1024` |
| Bounded prefix batches only | `false` |
| Scheduler policy | `constant` |
| Scheduler applied | `false` |
| Learning-rate mode | `constant` |
| Base learning rate | `0.0003` |
| Final learning rate | `0.0003` |

The train probe saw `1054` records, used `1054` documents, reached shuffle buffer occupancy `1024`, and used `4000` train batches. The validation probe used the sequential prefix policy for `10` validation batches.

## Metrics summary

| Metric | Value |
| --- | --- |
| First train loss | `9.869211` |
| Final train loss | `3.160682` |
| Final validation loss | `9.214416` |
| Final gradient norm | `1.001534` |
| Metrics rows | `1000` |
| Validation rows | `10` |
| Tokens seen | `16384000` |
| Elapsed seconds | `341.633667` |
| Approximate tokens/sec | `47957.802693` |
| Last GPU memory allocated | `2.64512 GiB` |
| Last GPU memory reserved | `8.416016 GiB` |

All reported train loss, validation loss, and gradient finite checks passed.

## Checkpoint and artifact boundary

The Modal training run reported a checkpoint path and confirmed reload validation:

```text
experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/checkpoints/checkpoint_step_1000.pt
```

The checkpoint was produced on the Modal side but was not included in the result package import and must not be committed. The imported result directory contains only small result and validation artifacts.

## Local validation evidence

Validator:

```text
scripts/validate_mvp24_modal_a100_5gb_1000step_imported_results.py
```

Commands run locally:

```bash
./.venv/Scripts/python.exe -m py_compile scripts/validate_mvp24_modal_a100_5gb_1000step_imported_results.py
./.venv/Scripts/python.exe scripts/validate_mvp24_modal_a100_5gb_1000step_imported_results.py
```

Validation result:

| Field | Value |
| --- | --- |
| Validation status | `passed` |
| Blocker count | `0` |
| Metrics rows actual | `1000` |
| Validation rows actual | `10` |
| Checkpoint reload match | `true` |
| Post-run artifact validation passed | `true` |

The local validator also scans the import directory for forbidden artifact names, including checkpoint, raw JSONL, processed data, splits, and nested tarballs.

## Interpretation

MVP-24 establishes that the 5GB prepared-data streaming path can complete a bounded 1000-step Modal A100 run with shuffle-buffer train sampling, sequential-prefix validation sampling, constant learning-rate scheduler metadata, finite train/validation/gradient metrics, matching imported line counts, and post-run artifact validation passing.

Longer 5GB runs remain separate cost-bearing work and require explicit approval before execution.
