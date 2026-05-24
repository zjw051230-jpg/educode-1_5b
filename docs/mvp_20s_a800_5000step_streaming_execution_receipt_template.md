# MVP-20.S A800 5000-Step Streaming Execution Receipt Template

Use this template only if the optional MVP-20.S 5000-step follow-up runs after a successful MVP-19 3000-step primary run.

## Execution Receipt

| field | value |
|---|---|
| 是否完成 | `TBD` |
| GPU | `TBD` |
| container RAM | `TBD` |
| commit hash | `TBD` |
| config path | `configs/a100/fineweb_edu_500mb_300m_5000step_public16k_execute.json` |
| data package source | `fineweb_edu_500mb_prepared_splits.tar.gz` |
| data_loading_mode | `streaming` |
| batch_size | `8` |
| grad_accum | `4` |
| max_steps | `5000` |
| parameter_count | `336106496 expected` |
| first_train_loss | `TBD` |
| final_train_loss | `TBD` |
| final_val_loss | `TBD` |
| loss_all_finite | `TBD` |
| val_loss_all_finite | `TBD` |
| grad_all_finite | `TBD` |
| metrics_rows | `5000 expected` |
| validation_rows | `10 expected` |
| tokens_seen | `TBD` |
| elapsed_seconds | `TBD` |
| tokens_per_sec | `TBD` |
| checkpoint_reload_match | `TBD` |
| post_run_artifact_validation | `TBD` |
| copied back files | `TBD` |
| known caveats | `500MB corpus; bounded_prefix_batches_only=true; systems validation only; not model quality` |
| 下一步建议 | `TBD` |

## Copied Back Files Checklist

- [ ] `summary.json`
- [ ] `summary.md`
- [ ] `metrics.jsonl`
- [ ] `validation_metrics.jsonl`
- [ ] `run_config.json`
- [ ] `run_metadata.json`
- [ ] `post_run_artifact_validation_summary.json`

Do not copy back by default:

- [ ] checkpoint files
- [ ] raw corpus files
- [ ] processed corpus files
- [ ] train/validation split files
- [ ] prepared split packages
- [ ] result tarball into git

## Known Caveats

Record whether these remain true:

- `bounded_prefix_batches_only=true`;
- 500MB corpus only;
- scheduler disabled or not applied;
- no downstream evaluation;
- no model-quality claim.
