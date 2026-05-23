# MVP-14 + MVP-15 Low-RAM Training Summary

## Summary

MVP-14 and MVP-15 both completed on remote A800 using a low-host-RAM fallback configuration.

Both runs succeeded as training-systems validations:

- CUDA bf16 execution worked;
- public16k tokenizer path worked;
- metrics were written for every step;
- standalone `validation_metrics.jsonl` was written;
- checkpoint reload verification matched;
- post-run artifact validation passed;
- imported local result validation passed.

Neither run proves model quality.

## Results Compared

| field | MVP-14 1000-step | MVP-15 3000-step |
|---|---:|---:|
| max_steps | `1000` | `3000` |
| batch_size | `1` | `1` |
| gradient_accumulation_steps | `1` | `1` |
| tokens_seen | `512000` | `1536000` |
| exact_parameter_count | `336106496` | `336106496` |
| metrics_rows | `1000` | `3000` |
| validation_rows | `10` | `10` |
| first_train_loss | `9.873169` | `9.873169` |
| final_train_loss | `0.213472` | `0.114589` |
| final_val_loss | `11.513049` | `12.515621` |
| checkpoint_reload_match | `true` | `true` |
| post_run_artifact_validation.passed | `true` | `true` |
| import validation | `passed` | `passed` |

## Low-RAM Fallback Context

The planned public16k configurations used larger effective host-side batch preparation. On the remote machine, the original config and `batch_size=8` / `gradient_accumulation_steps=4` fallback attempts were killed by the current `16GiB` container RAM limit.

The successful fallback changed both runs to:

- `batch_size = 1`
- `gradient_accumulation_steps = 1`

GPU memory was not the bottleneck. The recorded GPU memory values were low relative to A800/A100 capacity; the problem was host/container RAM.

## Interpretation

The low train losses and high validation losses show a strong overfitting or bounded-prefix memorization signal:

- MVP-14: final train loss `0.213472`, final validation loss `11.513049`;
- MVP-15: final train loss `0.114589`, final validation loss `12.515621`.

This means the runs should be described as training-systems evidence only. They validate the execution harness, logging, validation metrics, checkpoint reload path, and artifact review path. They do not validate model quality, generalization, tokenizer quality, or final architecture quality.

## Artifact Policy

The imported local result directories contain only small review artifacts:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`
- `import_validation_summary.json`

Checkpoints were not downloaded and were not committed. Result tarballs remain local-only and should not be committed.

## Next Direction

The next A800/A100 experiments should use `32GB+` host/container RAM, preferably `48GB` or `64GB`, before retrying larger batch settings. If high-RAM rental is not available, improve streaming batch preparation before longer or larger-batch runs.
