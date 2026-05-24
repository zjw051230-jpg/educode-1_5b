# MVP-18 A800 1000-Step Streaming Execution Receipt

## Execution Identity

| field | value |
|---|---|
| milestone | MVP-18 |
| run_id | `20260524_211036_fineweb_edu_500mb_300m_1000step_public16k_execute` |
| run_name | `fineweb_edu_500mb_300m_1000step_public16k_execute` |
| output_dir | `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute` |
| imported_result_dir | `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/results_imported_streaming` |
| config | `configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json` |

## Hardware / Runtime

| field | value |
|---|---:|
| GPU | `A800-SXM4-40GB` |
| container RAM | `48GiB` |
| runtime_device | `cuda` |
| runtime_dtype | `bf16` |
| GPU memory reserved | about `8.416 GiB` |
| exact_parameter_count | `336106496` |

## Data and Tokenizer

| field | value |
|---|---|
| corpus | FineWeb-Edu `sample-10BT` 500MB prepared local split |
| train/val source | uploaded from local prepared splits package |
| live Hugging Face download during run | no |
| tokenizer | `fineweb_edu_public_bpe_16k` |
| tokenizer_vocab_size | `16384` |

## Streaming Batch Settings

| field | value |
|---|---:|
| data_loading_mode | `streaming` |
| host_ram_efficient_batching | `true` |
| batch_precompute_disabled | `true` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| sequence_length | `512` |
| train_batches_used | `4000` |
| val_batches_used | `10` |

This run used the MVP-17 streaming batch iterator and was not a `batch_size=1` low-RAM fallback.

## Metrics Receipt

| field | value |
|---|---:|
| max_steps | `1000` |
| first_train_loss | `9.864946` |
| final_train_loss | `2.877289` |
| final_val_loss | `8.752452` |
| loss_all_finite | `true` |
| val_loss_all_finite | `true` |
| grad_all_finite | `true` |
| metrics_rows | `1000` |
| validation_rows | `10` |
| tokens_seen | `16384000` |
| elapsed_seconds | `343.899789` |
| approximate_tokens_per_sec | `47641.785517` |

`validation_metrics.jsonl` was independently written and imported with `10` validation rows.

## Checkpoint / Artifact Validation

| field | value |
|---|---|
| checkpoint_reload_match | `true` |
| checkpoint_path_starts_with_output_dir | `true` |
| post_run_artifact_validation | `passed` |
| import_validation_status | `passed` |
| import_validation_blockers | `0` |
| checkpoint downloaded locally | no |
| checkpoint committed | no |

The remote checkpoint was about `1.9G`. It was intentionally not downloaded and not committed.

## Receipt Conclusion

MVP-18 proves the 300M public16k A800 training-systems chain can run with restored `batch_size=8` / `gradient_accumulation_steps=4` after the MVP-17 streaming batch iterator change. It validates streaming batching, logging, standalone validation metrics, checkpoint save/reload, and artifact validation.

It does not claim model quality.
