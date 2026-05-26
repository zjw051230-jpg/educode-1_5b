# MVP-21 A800 2GB 1000-step Streaming Execution Receipt Template

## Execution Receipt

| field | value |
|---|---|
| 是否完成 |  |
| GPU |  |
| container RAM |  |
| commit hash |  |
| data package source | `C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz` |
| config path | `configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json` |
| data_loading_mode | `streaming` |
| batch_size | `8` |
| grad_accum | `4` |
| max_steps | `1000` |
| parameter_count | `336106496` |
| first_train_loss |  |
| final_train_loss |  |
| final_val_loss |  |
| loss_all_finite |  |
| val_loss_all_finite |  |
| grad_all_finite |  |
| metrics_rows |  |
| validation_rows |  |
| tokens_seen |  |
| elapsed_seconds |  |
| tokens_per_sec |  |
| checkpoint_reload_match |  |
| post_run_artifact_validation |  |
| copied back files |  |
| checkpoint policy | checkpoints remain remote/local-only and must not be committed |
| known caveats | bounded 1000-step systems run, not model-quality evidence |
| next step | run/import 2GB 3000-step only after this 1000-step result passes validation |

## Required Attachments

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`

Do not attach checkpoints, raw corpus files, processed corpus files, split files, or prepared data packages.
