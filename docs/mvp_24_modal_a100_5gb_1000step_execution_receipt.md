# MVP-24 Modal A100 5GB 1000-step Execution Receipt

## Execution summary

| Field | Value |
| --- | --- |
| Status | `success` |
| Mode | `train_5gb_1000` |
| GPU requested | `A100-40GB` |
| Volume name | `educode-data` |
| Repo commit reported by request | `5c7c1b5` |
| Run metadata git commit | `5c7c1b594d1191e198eb5609a0b74024c8c4130a` |
| Required runner commit | `16f4cd6` |
| Config path | `configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json` |
| Prepared package | `/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz` |
| Result package | `/vol/results/mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz` |
| Ran training | `true` |
| Produced checkpoint on Modal worker | `true` |
| Training status | `success` |

## Data availability checks

| Field | Value |
| --- | --- |
| Train path exists | `true` |
| Validation path exists | `true` |
| Train sampling policy | `shuffle_buffer` |
| Validation sampling policy | `sequential_prefix` |
| Shuffle seed | `1337` |
| Shuffle buffer size | `1024` |
| Data loading mode | `streaming` |

Expected prepared package members:

- `data/public_corpus/fineweb_edu_sample10bt_5gb/manifest.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/validation_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/intake_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/intake_validation_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl`

## Imported result artifacts

Imported directory:

```text
experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_streaming/
```

Approved imported files:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`
- `import_validation_summary.json`

The original local result tarball was not staged for commit.

## Run result

| Field | Value |
| --- | --- |
| Run ID | `20260526_192023_fineweb_edu_5gb_300m_1000step_public16k_execute` |
| Runtime device | `cuda` |
| Runtime dtype | `bf16` |
| GPU | `NVIDIA A100-SXM4-40GB` |
| Max steps | `1000` |
| Batch size | `8` |
| Gradient accumulation steps | `4` |
| Tokenizer vocab size | `16384` |
| Exact parameter count | `336106496` |
| Final train loss | `3.160682` |
| Final validation loss | `9.214416` |
| Metrics rows | `1000` |
| Validation rows | `10` |
| Tokens seen | `16384000` |
| Approximate tokens/sec | `47957.802693` |

## Validation result

| Field | Value |
| --- | --- |
| Local import validation | `passed` |
| Import validation blockers | `0` |
| Post-run artifact validation | `passed` |
| Loss all finite | `true` |
| Validation loss all finite | `true` |
| Gradient all finite | `true` |
| Checkpoint reload match | `true` |
| Checkpoint path starts with output dir | `true` |

## Artifact boundary

The Modal worker produced a checkpoint and verified checkpoint reload. That checkpoint was not imported, staged, or committed. The import step excluded checkpoints, raw JSONL, processed data, splits, prepared tarballs, result tarballs, and credentials.
