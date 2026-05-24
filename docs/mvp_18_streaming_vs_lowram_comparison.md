# MVP-18 Streaming vs Low-RAM Fallback Comparison

## Purpose

This note compares the MVP-18 streaming 1000-step run against the earlier MVP-14/MVP-15 low-RAM fallback runs.

The comparison is about training-systems behavior and host-RAM batching, not model quality.

## Key Difference

MVP-14 and MVP-15 succeeded only after falling back to `batch_size=1` / `gradient_accumulation_steps=1` under about `16GiB` container RAM.

MVP-18 used `48GiB` container RAM plus the MVP-17 streaming batch iterator and completed the intended `batch_size=8` / `gradient_accumulation_steps=4` path.

## Run Comparison

| field | MVP-14 low-RAM 1000-step | MVP-15 low-RAM 3000-step | MVP-18 streaming 1000-step |
|---|---:|---:|---:|
| data_loading_mode | pre-streaming fallback | pre-streaming fallback | streaming |
| container RAM | about `16GiB` | about `16GiB` | `48GiB` |
| batch_size | `1` | `1` | `8` |
| gradient_accumulation_steps | `1` | `1` | `4` |
| sequence_length | `512` | `512` | `512` |
| tokens_seen | `512000` | `1536000` | `16384000` |
| final_train_loss | `0.213472` | `0.114589` | `2.877289` |
| final_val_loss | `11.513049` | `12.515621` | `8.752452` |
| checkpoint_reload_match | `true` | `true` | `true` |
| post_run_artifact_validation | `passed` | `passed` | `passed` |

## Interpretation

The earlier low-RAM fallback runs validated that the CUDA bf16 model path, logging, validation metrics, checkpoint save/reload, and artifact validation could work. They did not validate the intended larger-batch path because host-side batch preparation exhausted RAM before training.

MVP-18 validates that the streaming path restored the intended larger batch settings:

```text
batch_size=8
gradient_accumulation_steps=4
sequence_length=512
```

The run was not a `batch_size=1` fallback. It supports the conclusion that MVP-17 fixed the host-RAM precompute bottleneck by avoiding run-sized token, sliding-sample, and batch list materialization.

## Loss Pattern

MVP-18 shows a healthier train/validation pattern than the low-RAM fallback runs, with final train loss `2.877289` and final validation loss `8.752452` rather than near-zero train loss with very high validation loss.

This is still not a model-quality claim. The corpus is bounded, the run is short, the model remains a systems-validation artifact, and no downstream evaluation has been run.

## Operational Conclusion

For continued GPU work:

1. Use streaming mode, not the old precomputed batch path.
2. Prefer `32GB+` host/container RAM, with `48GiB` validated by MVP-18.
3. Keep checkpoint artifacts remote unless explicitly needed and approved.
4. Treat any future MVP-19 3000-step streaming run as bounded training-systems evidence unless evaluation scope changes.

## Next Step

If continuing GPU work, run MVP-19 streaming 3000-step only after reviewing MVP-18 artifacts. If pausing GPU work, do a local next-scale decision report before more rentals.
