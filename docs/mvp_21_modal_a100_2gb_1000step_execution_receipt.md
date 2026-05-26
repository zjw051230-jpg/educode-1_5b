# MVP-21.R Modal A100 2GB 1000-Step Execution Receipt

| field | value |
|---|---|
| 是否完成 | yes |
| backend/GPU | Modal / requested `A100-40GB`, runtime `NVIDIA A100-SXM4-40GB` |
| Modal volume | `educode-data` |
| repo_commit | `0b0332a` |
| config path | `configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json` |
| prepared package | `/vol/prepared/fineweb_edu_2gb_prepared_splits.tar.gz` |
| data_loading_mode | `streaming` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| max_steps | `1000` |
| tokenizer_vocab_size | `16384` |
| parameter_count | `336106496` |
| first_train_loss | `9.864925` |
| final_train_loss | `3.008913` |
| final_val_loss | `9.012106` |
| loss_all_finite | `true` |
| val_loss_all_finite | `true` |
| grad_all_finite | `true` |
| metrics_rows | `1000` |
| validation_rows | `10` |
| tokens_seen | `16384000` |
| elapsed_seconds | `346.31222` |
| approximate_tokens_per_sec | `47309.910177` |
| checkpoint_path | `experiments/a100/fineweb_edu_2gb_300m_1000step_public16k_execute/checkpoints/checkpoint_step_1000.pt` |
| checkpoint_reload_match | `true` |
| post_run_artifact_validation | `passed`, blockers `0` |
| copied back files | `summary.json`, `summary.md`, `metrics.jsonl`, `validation_metrics.jsonl`, `run_config.json`, `run_metadata.json`, `post_run_artifact_validation_summary.json` |
| 是否提交 checkpoint | no |
| 是否提交 raw/processed/splits | no |
| known caveats | bounded 1000-step training-systems run only; no model-quality claim; scheduler config present but scheduler not applied |
| 下一步建议 | consider Modal `train_2gb_3000` only after explicit approval and cost/Volume check |

## Import Validation

| field | value |
|---|---|
| validation script | `scripts/validate_mvp21_modal_a100_2gb_1000step_imported_results.py` |
| validation summary | `experiments/a100/fineweb_edu_2gb_300m_1000step_public16k_execute/results_imported_modal_streaming/import_validation_summary.json` |
| validation_status | `passed` |
| blocker_count | `0` |

## Imported Artifact Directory

```text
experiments/a100/fineweb_edu_2gb_300m_1000step_public16k_execute/results_imported_modal_streaming/
```

The result transfer tarball remains local and uncommitted:

```text
mvp21_a100_2gb_1000step_public16k_streaming_results.tar.gz
```
