# MVP-24 Modal A100 5GB 1000-Step Execution Receipt Template

Use this template after the future `train_5gb_1000` Modal run completes.

## Execution Receipt

| Field | Value |
|---|---|
| 是否完成 |  |
| backend/GPU | Modal / A100-40GB |
| Modal volume | `educode-data` |
| repo_commit |  |
| config path | `configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json` |
| prepared package | `/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz` |
| data_loading_mode | `streaming` |
| sampling_policy | `shuffle_buffer` |
| shuffle_seed | `1337` |
| shuffle_buffer_size | `1024` |
| bounded_prefix_batches_only | `false` |
| scheduler_policy | `constant` |
| learning_rate_mode | `constant` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| max_steps | `1000` |
| tokenizer_vocab_size | `16384` |
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
| approximate_tokens_per_sec |  |
| checkpoint_path |  |
| checkpoint_reload_match |  |
| post_run_artifact_validation |  |
| copied back files |  |
| 是否提交 checkpoint | no |
| 是否提交 raw/processed/splits | no |
| known caveats | bounded training-systems evidence only; no model-quality claim |
| 下一步建议 | import the small result package and validate with the MVP-24.R validator |

## Copied Back Files Checklist

The result package should contain only:

- [ ] `summary.json`
- [ ] `summary.md`
- [ ] `metrics.jsonl`
- [ ] `validation_metrics.jsonl`
- [ ] `run_config.json`
- [ ] `run_metadata.json`
- [ ] `post_run_artifact_validation_summary.json`

Confirm not copied back:

- [ ] checkpoint files
- [ ] `raw.jsonl`
- [ ] `processed/`
- [ ] `splits/`
- [ ] prepared package tarballs
- [ ] result tarballs nested inside the result package

## Notes

This run should be reported as bounded training-systems evidence for Modal prepared-data streaming, shuffle-buffer sampling, checkpoint reload validation, and artifact packaging. It should not be described as full pretraining or model-quality evidence.
