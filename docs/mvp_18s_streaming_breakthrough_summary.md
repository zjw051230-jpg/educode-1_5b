# MVP-18.S Streaming Breakthrough Summary

## Purpose

MVP-18.S summarizes the training-systems breakthrough from the public16k A800 streaming run and records the decision boundary for the next scale step.

This is a documentation and decision milestone only. It does not run training, enter A100/A800, train a tokenizer or model, download data, change the training loop, or commit checkpoints, raw corpus files, processed data, split files, or result tarballs.

## Timeline

| milestone | role | outcome |
|---|---|---|
| MVP-14 | A800 1000-step public16k low-RAM fallback | Completed with CUDA bf16 execution, metrics, validation metrics, checkpoint reload, and artifact validation, but only after falling back to `batch_size=1` / `gradient_accumulation_steps=1`. |
| MVP-15 | A800 3000-step public16k low-RAM fallback | Completed the same low-RAM fallback path, again as systems evidence only. |
| MVP-16 | Host-RAM batching diagnosis | Identified host/container RAM as the blocker, not GPU memory. The old 1000-step path was estimated at `129.024313 GiB` of Python precompute memory; the 3000-step path at `387.080954 GiB`. |
| MVP-17 | Streaming batch iterator implementation | Added lazy JSONL text, token block, and batch iteration; updated public16k 1000/3000-step configs to `data_loading_mode=streaming`; validated locally with unit tests, memory inspection, data/model/loss smoke, and dry-runs. |
| MVP-18 | A800 1000-step public16k streaming run | Completed the target `batch_size=8` / `gradient_accumulation_steps=4` streaming path under `48GiB` container RAM. |

## Key Technical Breakthrough

The previous bottleneck was host-side Python object materialization. The old path built a large token buffer, expanded it into a full overlapping sliding-window sample list, built all batches, and then sliced the bounded run requirement.

MVP-17 replaced that with a streaming path:

```text
iter_jsonl_texts -> iter_token_blocks -> iter_batches -> cycle_batches
```

The streaming path validates corpus metadata at the JSONL boundary, tokenizes one document at a time, keeps only a rolling token buffer, yields next-token blocks lazily, and provides one microbatch at a time to the training loop. This keeps the model-facing batch shape unchanged while avoiding full-run `train_batches` and `val_batches` retention.

## MVP-18 Result

MVP-18 completed the A800 300M public16k 1000-step streaming run with the intended larger batch settings restored.

| field | value |
|---|---:|
| GPU | `A800-SXM4-40GB` |
| container RAM | `48GiB` |
| runtime_dtype | `bf16` |
| exact_parameter_count | `336106496` |
| tokenizer_vocab_size | `16384` |
| max_steps | `1000` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| sequence_length | `512` |
| data_loading_mode | `streaming` |
| train_batches_used | `4000` |
| val_batches_used | `10` |
| tokens_seen | `16384000` |
| first_train_loss | `9.864946` |
| final_train_loss | `2.877289` |
| final_val_loss | `8.752452` |
| metrics_rows | `1000` |
| validation_rows | `10` |
| approximate_tokens_per_sec | `47641.785517` |
| checkpoint_reload_match | `true` |
| post_run_artifact_validation | `passed` |
| import_validation_status | `passed` |

The remote checkpoint was about `1.9G`. It was not downloaded and was not committed.

## Comparison to Low-RAM Runs

| field | MVP-14 low-RAM 1000-step | MVP-15 low-RAM 3000-step | MVP-18 streaming 1000-step |
|---|---:|---:|---:|
| container RAM | about `16GiB` | about `16GiB` | `48GiB` |
| data_loading_mode | pre-streaming fallback | pre-streaming fallback | streaming |
| batch_size | `1` | `1` | `8` |
| gradient_accumulation_steps | `1` | `1` | `4` |
| tokens_seen | `512000` | `1536000` | `16384000` |
| final_train_loss | `0.213472` | `0.114589` | `2.877289` |
| final_val_loss | `11.513049` | `12.515621` | `8.752452` |
| checkpoint_reload_match | `true` | `true` | `true` |

The low-RAM runs validated the execution harness but did not validate the intended larger-batch path. MVP-18 validates that the streaming iterator restored that path under higher host/container RAM.

## Caveats

- MVP-18 is training-systems evidence, not a model-quality claim.
- The run is bounded to a 500MB prepared FineWeb-Edu public split and 1000 optimizer steps.
- No downstream evaluation has been run.
- The model still uses the current 300M public16k architecture and learned positional embeddings.
- Scheduler configuration was present but not applied in the current training script, so scheduler cleanup remains a later engineering task.
- The result does not justify committing checkpoints, raw corpus files, processed data, split files, or result tarballs.

## Conclusion

MVP-18 confirms that the MVP-17 streaming batch iterator removed the host-RAM precompute blocker for the current public16k A800 path. Future public16k A800/A100 work should treat streaming mode as the baseline and should use prepared data packages transferred to GPU hosts rather than live large-corpus fetching inside the GPU container.

The recommended next GPU-facing step is MVP-19: a bounded streaming 3000-step public16k run on the existing 500MB prepared corpus, only after a short execution/import plan gate and only if GPU time is available.
