# MVP-16 Host-RAM and Batching Fix Plan

## 1. Purpose

MVP-16 reviews the host-RAM and batch-preparation bottleneck discovered during the A800 public16k runs before attempting larger batches or longer training again.

MVP-14 and MVP-15 proved that the CUDA bf16 model path, tokenizer path, logging, validation metrics, checkpoint reload, and artifact validation can work. They also showed that the current host-side batch preparation is not safe for the intended larger batch settings under a `16GiB` container RAM limit. Fixing this comes before more step stacking.

## 2. Evidence from MVP-14 / MVP-15

Observed low-RAM fallback evidence:

- original `batch_size=8` / `gradient_accumulation_steps=4` failed under `16GiB` container RAM;
- `batch_size=8` / `gradient_accumulation_steps=1` also failed;
- `batch_size=4` / `gradient_accumulation_steps=1` also failed;
- `batch_size=1` / `gradient_accumulation_steps=1` succeeded;
- GPU memory reserved in the successful low-RAM runs was only a few GiB;
- checkpoint reload matched for both imported runs;
- standalone `validation_metrics.jsonl` was written for both runs;
- post-run artifact validation passed for both runs.

The successful runs were:

| field | MVP-14 1000-step | MVP-15 3000-step |
|---|---:|---:|
| batch_size | `1` | `1` |
| gradient_accumulation_steps | `1` | `1` |
| tokens_seen | `512000` | `1536000` |
| final_train_loss | `0.213472` | `0.114589` |
| final_val_loss | `11.513049` | `12.515621` |
| checkpoint_reload_match | `true` | `true` |
| post_run_artifact_validation.passed | `true` | `true` |

These are training-systems results, not model-quality results. The very low train losses and high validation losses indicate overfitting or bounded-prefix memorization risk.

## 3. Root Cause Hypothesis

The limiting resource was host/container RAM, not A800/A100 GPU memory.

The GPU compute path works. The tokenizer and model path works. The observed failure pattern points to host-side batch preparation retaining too many Python objects before training starts.

The current training script likely exhausts host RAM because it:

- collects a large token buffer for the whole requested bounded run;
- expands that buffer into every overlapping next-token sample;
- batches all available overlapping samples;
- then slices down to the required number of batches.

This creates a much larger Python object graph than the actual `input_ids` and `labels` tensors needed at any single training step.

## 4. Batching Risk Review

Reviewed script:

```text
scripts/run_a100_300m_fineweb_edu_10step_training.py
```

Risky path:

```text
run_training -> extract_bounded_batches -> make_next_token_samples -> batch_samples
```

Findings:

| risk | observed |
|---|---|
| precomputed train batches | yes, `train_batches` is built for `max_steps * gradient_accumulation_steps` |
| large token buffer | yes, `token_ids` is extended until `required_batches * batch_size * sequence_length + 1` |
| full prefix-batch caching | yes, the training loop indexes into a retained `train_batches` list |
| validation batch caching | yes, `val_batches` is also built before training |
| missing streaming iterator | yes, the current path is list-based |
| over-generation of sliding samples | yes, `make_next_token_samples` creates every offset sample before `batch_samples` slices batches |

MVP-16 memory inspection for the original `1000-step` config reported:

| field | value |
|---|---:|
| required_train_batches | `4000` |
| required_tokens | `16384001` |
| needed_non_overlapping_samples | `32000` |
| current_sliding_window_samples | `16383489` |
| current_available_batches_before_slice | `2047936` |
| current_unused_batches_before_slice | `2043936` |
| estimated input + label tensor memory | `250.0 MiB` |
| estimated token buffer Python memory | `562.5 MiB` |
| estimated sliding sample pointer memory | `124.996101 GiB` |
| estimated current Python precompute memory | `129.024313 GiB` |

The tensor memory for the actual retained numeric payload is modest. The Python list/slice representation is the major host-RAM risk.

## 5. Recommended Fix

Implement a streaming batch iterator before retrying the intended larger batch settings.

Recommended implementation properties:

- stream JSONL records instead of loading a full corpus or run-sized token buffer;
- tokenize records incrementally;
- keep only a small rolling token buffer;
- produce `x`/`y` blocks lazily;
- produce batches lazily;
- avoid preparing `max_steps * gradient_accumulation_steps` batches at once;
- avoid creating every overlapping sliding-window sample when only bounded sequential blocks are needed;
- rebuild or lazily evaluate validation batches with a small cache;
- log a memory plan before training starts;
- add a configurable `max_host_ram_mb` warning threshold.

A minimal safe direction is:

```text
iter_jsonl_texts -> iter_token_blocks -> iter_batches -> training loop
```

The training loop should request the next microbatch from an iterator instead of indexing into a precomputed list.

## 6. Next Config Recommendation

For the next `16-core / 48GB` A800/A100 run:

1. Do not return directly to a `3000-step` larger-batch run.
2. First validate the streaming iterator with a short bounded run or dry-run memory plan.
3. Try `batch_size=8` / `gradient_accumulation_steps=4` only after the streaming fix or an explicit memory check passes.
4. If needed, use fallbacks in this order:
   - `batch_size=4` / `gradient_accumulation_steps=4`;
   - `batch_size=4` / `gradient_accumulation_steps=2`;
   - `batch_size=2` / `gradient_accumulation_steps=4`.
5. Avoid treating `batch_size=1` fallback runs as quality training.

The A800/A100 `40GB` GPU class is still sufficient at this stage. The next rental should primarily improve host/container RAM.

## 7. What MVP-16 Does Not Do

MVP-16 does not:

- run training;
- enter A100/A800;
- train a tokenizer;
- train a model;
- modify the core model architecture;
- download new data;
- advance D20/E work;
- save checkpoints.

## 8. Next Step

Proceed to MVP-17 streaming batch iterator implementation, or MVP-17.P planning if the change should be reviewed as a larger refactor before editing the training path.
