# MVP-21.Q + MVP-22.P Local Multi-Prep Bundle

## Purpose

Prepare a larger local bundle for the next GPU session: extend the existing 2GB public16k queue through 5000 steps, prepare a 5GB FineWeb-Edu public corpus package, and create 5GB 1000/3000-step streaming configs with local dry-run/readiness evidence.

This step did not push Git, enter A800/A100, run model training, train a tokenizer/model, change model architecture, create checkpoints, or commit raw/processed/split corpus data.

## Result Summary

| area | status | evidence |
|---|---|---|
| 2GB 5000-step queue config | success | `configs/a100/fineweb_edu_2gb_300m_5000step_public16k_execute.json` |
| readiness gate update | success | 5GB path marker supported; validator bounded to `1000`, `3000`, `5000` |
| 5GB data config | success | `configs/data/fineweb_edu_sample10bt_5gb.json` |
| 5GB fetch/raw validation | success | `1127093` raw records; `5368710356` text bytes |
| 5GB intake/split validation | success | `1122642` processed; `1066882` train; `55760` val |
| 5GB prepared package | success | `C:/Users/01/fineweb_edu_5gb_prepared_splits.tar.gz` |
| 5GB 1000/3000-step configs | success | both dry-run/readiness passed with blockers `0` |

## 2GB Queue

| config | max_steps | eval_interval | readiness |
|---|---:|---:|---|
| `configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json` | `1000` | `100` | passed in MVP-21.P |
| `configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json` | `3000` | `300` | passed in MVP-21.P |
| `configs/a100/fineweb_edu_2gb_300m_5000step_public16k_execute.json` | `5000` | `500` | passed in this step |

The next GPU session should still run 2GB 1000-step first. Run 3000-step only after 1000-step passes, and run 5000-step only after 3000-step passes and rental time remains.

## 5GB Data Result

| metric | value |
|---|---:|
| target_size_mb | `5120` |
| raw record_count | `1127093` |
| raw total_text_bytes | `5368710356` |
| raw duplicate_text_hash_count | `4431` |
| processed_count | `1122642` |
| train_count | `1066882` |
| val_count | `55760` |
| dropped_duplicate_count | `4451` |
| train_text_bytes | `5080485686` |
| val_text_bytes | `268127033` |

Prepared package:

```text
C:/Users/01/fineweb_edu_5gb_prepared_splits.tar.gz
```

Package size is `2112167310` bytes, SHA-256 is `19a933ec5afc379d58751461ff56e8e89be4d3fbfc05e10df789c6541f8bcd5d`.

## 5GB Training Readiness

| config | max_steps | memory inspection | dry-run | readiness |
|---|---:|---|---|---|
| `configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json` | `1000` | streaming host-RAM safe; batch tensor `0.062` MiB | passed; parameter count `336106496` | blockers `0`, caveats `0` |
| `configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json` | `3000` | streaming host-RAM safe; batch tensor `0.062` MiB | passed; parameter count `336106496` | blockers `0`, caveats `0` |

Both configs keep `data_loading_mode=streaming`, `batch_size=8`, `gradient_accumulation_steps=4`, public16k vocab size `16384`, and checkpoint paths under their matching output dirs.

## Package Logistics

- 2GB package: `C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz`.
- 5GB package: `C:/Users/01/fineweb_edu_5gb_prepared_splits.tar.gz`.
- GPU hosts should receive prepared packages before training.
- GPU hosts should not fetch Hugging Face data for prepared slices.
- Copy back only small result artifacts and validation summaries unless a later step explicitly approves checkpoint transfer.

## Import Plan

Future result packages should include only:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`

Do not import checkpoints, raw corpus files, processed corpus files, split files, prepared data packages, or result tarballs into Git.

## Next GPU Route

1. Run/import 2GB 1000-step first.
2. If it passes, run/import 2GB 3000-step.
3. If it passes and time remains, run/import 2GB 5000-step.
4. Start 5GB 1000-step only after the 2GB queue result supports moving up in data scale.
5. Run 5GB 3000-step only after 5GB 1000-step passes.

## Claim Boundary

This bundle is engineering/scaling preparation. It validates local data preparation, package logistics, config consistency, dry-run materialization, and readiness gates. It is not full pretraining and not model-quality evidence.
