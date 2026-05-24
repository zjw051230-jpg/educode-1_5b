# MVP-19 A800 3000-Step Streaming Execution Receipt Template

Use this template after a future MVP-19 streaming 3000-step run. Fill it from the remote `summary.json`, post-run validation summary, and import validation output.

## Execution Receipt

| field | value |
|---|---|
| 是否完成 | `TBD` |
| machine/cloud provider | `TBD` |
| GPU name | `TBD` |
| container RAM | `TBD` |
| commit hash | `TBD` |
| config path | `configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json` |
| data package source | `fineweb_edu_500mb_prepared_splits.tar.gz` |
| data_loading_mode | `streaming` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| max_steps | `3000` |
| tokenizer_path | `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json` |
| tokenizer_vocab_size | `16384` |
| parameter_count | `336106496` |
| first_train_loss | `TBD` |
| final_train_loss | `TBD` |
| final_val_loss | `TBD` |
| loss_all_finite | `TBD` |
| grad_all_finite | `TBD` |
| metrics_rows | `3000 expected` |
| validation_rows | `10 expected` |
| tokens_seen | `TBD` |
| elapsed_seconds | `TBD` |
| approximate_tokens_per_sec | `TBD` |
| checkpoint_path | `TBD` |
| checkpoint_reload_match | `TBD` |
| post_run_artifact_validation | `TBD` |
| copied back files | `TBD` |
| 是否提交 checkpoint | `No expected` |
| 是否 OOM | `TBD` |
| 是否 non-finite loss | `TBD` |
| known caveats | `bounded systems validation only; 500MB corpus; no model-quality claim` |
| 下一步建议 | `TBD` |

## Copied Back Files Checklist

Only these files should be copied back:

- [ ] `summary.json`
- [ ] `summary.md`
- [ ] `metrics.jsonl`
- [ ] `validation_metrics.jsonl`
- [ ] `run_config.json`
- [ ] `run_metadata.json`
- [ ] `post_run_artifact_validation_summary.json`

Do not copy back by default:

- [ ] checkpoint files
- [ ] `raw.jsonl`
- [ ] processed corpus files
- [ ] train/validation split files
- [ ] prepared split packages
- [ ] result tarball into git

## Stop/Failure Notes

If the run stops early, record:

- step where it stopped;
- final visible log lines;
- whether the stop was OOM, non-finite loss, readiness blocker, checkpoint reload failure, or artifact validation failure;
- whether any checkpoint exists remotely;
- which small artifacts were still safe to copy back.
