# MVP-22.R Modal A100 2GB 3000-Step Execution Receipt

| field | value |
|---|---|
| 是否完成 | yes |
| backend/GPU | Modal / requested `A100-40GB`, runtime `NVIDIA A100-SXM4-40GB` |
| Modal volume | `educode-data` |
| repo_commit | `8e92c81` |
| config path | `configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json` |
| prepared package | `/vol/prepared/fineweb_edu_2gb_prepared_splits.tar.gz` |
| data_loading_mode | `streaming` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| max_steps | `3000` |
| tokenizer_vocab_size | `16384` |
| parameter_count | `336106496` |
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
| checkpoint_path | `experiments/a100/fineweb_edu_2gb_300m_3000step_public16k_execute/checkpoints/checkpoint_step_3000.pt` |
| checkpoint_reload_match | `true` |
| post_run_artifact_validation | `passed`, blockers `0` |
| copied back files | `summary.json`, `summary.md`, `metrics.jsonl`, `validation_metrics.jsonl`, `run_config.json`, `run_metadata.json`, `post_run_artifact_validation_summary.json` |
| 是否提交 checkpoint | no |
| 是否提交 raw/processed/splits | no |
| known caveats | bounded 3000-step training-systems run only; no model-quality claim; scheduler config present but scheduler not applied |
| 下一步建议 | summarize 1000/3000-step Modal evidence or consider a longer bounded follow-up only after explicit approval and cost/Volume check |

## Import Validation

| field | value |
|---|---|
| validation script | `scripts/validate_mvp22_modal_a100_2gb_3000step_imported_results.py` |
| validation summary | `experiments/a100/fineweb_edu_2gb_300m_3000step_public16k_execute/results_imported_modal_streaming/import_validation_summary.json` |
| validation_status | `passed` |
| blocker_count | `0` |

## Imported Artifact Directory

```text
experiments/a100/fineweb_edu_2gb_300m_3000step_public16k_execute/results_imported_modal_streaming/
```

The result transfer tarball remains local and uncommitted:

```text
mvp22_a100_2gb_3000step_public16k_streaming_results.tar.gz
```
