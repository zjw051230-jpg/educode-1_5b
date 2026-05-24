# MVP-18 A800 1000-Step Public16k Streaming Run

## Summary

MVP-18 completed the A800 300M public16k 1000-step streaming run and imported the small result artifacts for local review.

This was the first post-MVP-17 GPU execution using the streaming batch iterator with the intended larger batch settings restored.

## Imported Artifacts

Imported directory:

```text
experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/results_imported_streaming/
```

Imported files:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`
- `import_validation_summary.json`

The result tarball, checkpoint, raw corpus, processed corpus, and split files were not committed.

## Run Configuration

| field | value |
|---|---:|
| run_id | `20260524_211036_fineweb_edu_500mb_300m_1000step_public16k_execute` |
| run_name | `fineweb_edu_500mb_300m_1000step_public16k_execute` |
| GPU | `A800-SXM4-40GB` |
| container RAM | `48GiB` |
| runtime_device | `cuda` |
| runtime_dtype | `bf16` |
| exact_parameter_count | `336106496` |
| tokenizer_vocab_size | `16384` |
| max_steps | `1000` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| sequence_length | `512` |
| data_loading_mode | `streaming` |
| host_ram_efficient_batching | `true` |
| batch_precompute_disabled | `true` |
| train_batches_used | `4000` |
| val_batches_used | `10` |

The 500MB train/val splits were uploaded from the prepared local split package. The remote run did not depend on a live Hugging Face download.

## Results

| metric | value |
|---|---:|
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
| last_gpu_memory_reserved_gib | `8.416016` |
| checkpoint_reload_match | `true` |
| checkpoint_path_starts_with_output_dir | `true` |
| post_run_artifact_validation | `passed` |
| import_validation_status | `passed` |
| import_validation_blockers | `0` |

`validation_metrics.jsonl` was written as a standalone validation metrics stream and contains `10` rows.

## Meaning

MVP-18 restored the target `batch_size=8` / `gradient_accumulation_steps=4` path that previously failed under low host RAM. This was not a `batch_size=1` low-RAM fallback run.

The successful run supports the MVP-17 conclusion that streaming batch preparation fixed the host-side run-sized precompute bottleneck. The checkpoint reload, validation metrics, structured logs, and post-run artifact validation also confirm the bounded training-systems chain.

## Boundaries

This is not a model-quality claim. The result is bounded systems evidence for:

- streaming batch preparation;
- larger effective batch execution;
- logging and validation metrics;
- checkpoint save/reload behavior;
- artifact validation and import review.

The remote checkpoint was about `1.9G`; it was not downloaded and was not committed.

## Next Step

If GPU time continues, the next candidate is MVP-19: a streaming 3000-step public16k run. If not continuing with GPU time, the next step should be local summary and next-scale decision work before further rentals.
