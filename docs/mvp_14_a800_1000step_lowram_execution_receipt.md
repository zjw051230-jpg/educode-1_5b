# MVP-14 A800 1000-step Low-RAM Execution Receipt

## Execution Status

| field | value |
|---|---|
| 是否完成 | yes |
| machine/cloud provider | remote A800 provider |
| GPU name | A800 class |
| CUDA available | true |
| config path | `configs/a100/fineweb_edu_500mb_300m_1000step_public16k_lowram_execute.json` |
| command | low-RAM fallback execution of public16k 1000-step run |
| output_dir | `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute` |
| imported_dir | `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/results_imported_lowram` |

## Run Configuration

| field | value |
|---|---:|
| max_steps | `1000` |
| batch_size | `1` |
| gradient_accumulation_steps | `1` |
| tokenizer_vocab_size | `16384` |
| parameter_count | `336106496` |
| tokens_seen | `512000` |

## Loss and Stability

| field | value |
|---|---:|
| first_train_loss | `9.873169` |
| final_train_loss | `0.213472` |
| final_val_loss | `11.513049` |
| loss_all_finite | `true` |
| val_loss_all_finite | `true` |
| grad_all_finite | `true` |
| 是否 OOM | no for low-RAM fallback; yes for earlier larger-batch attempts under 16GiB host/container RAM |
| 是否 non-finite loss | no |
| 是否超过 1000 steps | no |

## Artifact Counts

| field | value |
|---|---:|
| metrics_rows | `1000` |
| validation_rows | `10` |
| validation_metrics.jsonl standalone | `true` |
| checkpoint_path | `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/checkpoints/checkpoint_step_1000.pt` |
| checkpoint_reload_match | `true` |
| post_run_artifact_validation.passed | `true` |
| import_validation_status | `passed` |
| copied back files | `summary.json`, `summary.md`, `metrics.jsonl`, `validation_metrics.jsonl`, `run_config.json`, `run_metadata.json`, `post_run_artifact_validation_summary.json` |
| 是否提交 checkpoint | no |

## Known Caveats

- This was a low-host-RAM fallback run, not the original `batch_size=8` / `gradient_accumulation_steps=4` plan.
- Earlier larger-batch attempts were killed by `16GiB` host/container RAM, not GPU VRAM.
- Final train loss is very low while validation loss is high, indicating overfitting or bounded-prefix memorization risk.
- The run validates training systems, logging, checkpoint reload, and artifact validation, not model quality.

## 下一步建议

- Use this as MVP-14 systems evidence.
- For future larger-batch runs, rent `32GB+` host/container RAM, preferably `48GB` or `64GB`.
- Do not make model-quality claims from this run.
