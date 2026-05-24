# MVP-17 Streaming Batch Iterator Implementation

## Purpose

MVP-17 replaces run-sized host-side batch materialization with a streaming batch path for the A100/A800 public16k training script.

The goal is to keep the 300M public16k 1000/3000-step configs eligible for larger-batch GPU validation without retaining the full token buffer, full sliding-window sample list, or full run batch list in Python host RAM.

## Implemented Changes

- Added `scripts/streaming_lm_batch_iterator.py`.
- Added `tests/test_streaming_lm_batch_iterator.py` using standard-library `unittest`.
- Added `data.data_loading_mode = "streaming"` to both public16k execution configs.
- Updated `scripts/run_a100_300m_fineweb_edu_10step_training.py` to preserve the existing precomputed path and use streaming only when configured.
- Updated `scripts/inspect_training_batch_memory_plan.py` to report both the old precompute estimate and the active streaming steady-state estimate.
- Added `scripts/inspect_streaming_public16k_data_model_loss_smoke.py` for local streaming data/model/loss validation.

## Streaming Iterator Behavior

The streaming path uses:

```text
iter_jsonl_texts -> iter_token_blocks -> iter_batches -> cycle_batches
```

It validates `source_category`, `license`, and `allowed_for_training` at the JSONL boundary, tokenizes one document at a time, appends EOS when configured, keeps only a rolling token buffer, yields overlapping next-token blocks lazily, and yields one microbatch at a time.

The first streaming batches match the existing `make_next_token_samples` + `batch_samples` ordering on a tiny fixture, but the implementation no longer exposes or retains a full list of samples or batches.

## Training Script Integration

The A100/A800 training script now reads `data.data_loading_mode`:

- `precomputed`: old behavior, retained for backward compatibility;
- `streaming`: lazy microbatch retrieval with no full-run `train_batches` / `val_batches` list.

Dry-run and training summaries now record:

- `data_loading_mode`;
- `streaming_batches_used`;
- `host_ram_efficient_batching`;
- `batch_precompute_disabled`;
- streaming-aware `train_data_probe` and `val_data_probe` fields.

## Configs Updated

Updated configs:

- `configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json`
- `configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json`

Both keep the intended larger-batch settings:

```text
batch_size=8
gradient_accumulation_steps=4
sequence_length=512
```

Both now set:

```text
data_loading_mode=streaming
host_ram_efficient_batching=true
streaming_train_probe_records=64
streaming_val_probe_records=32
```

## Verification Evidence

Local bounded checks completed without running real training, backward, optimizer steps, or checkpoint saves.

| check | result |
|---|---|
| `py_compile` changed scripts | passed |
| `unittest tests/test_streaming_lm_batch_iterator.py` | `Ran 6 tests ... OK` |
| 1000-step memory inspection | `data_loading_mode=streaming`, old precompute estimate `129.024313 GiB`, streaming batch tensor estimate `0.062 MiB`, host-RAM safe `True` |
| 3000-step memory inspection | `data_loading_mode=streaming`, old precompute estimate `387.080954 GiB`, streaming batch tensor estimate `0.062 MiB`, host-RAM safe `True` |
| streaming public16k data/model/loss smoke | finite train loss `9.875000`, finite val loss `9.937500`, parameter count `336106496` |
| 1000-step dry-run | streaming mode active, tokenizer vocab `16384`, parameter count `336106496`, core feature parity `True` |
| 3000-step dry-run | streaming mode active, tokenizer vocab `16384`, parameter count `336106496`, core feature parity `True` |

Generated local summary artifacts:

- `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/batch_memory_plan_summary.json`
- `experiments/a100/fineweb_edu_500mb_300m_3000step_public16k_execute/batch_memory_plan_summary.json`
- `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/streaming_public16k_data_model_loss_smoke_summary.json`
- `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/dry_run_summary.json`
- `experiments/a100/fineweb_edu_500mb_300m_3000step_public16k_execute/dry_run_summary.json`

## Interpretation Boundary

MVP-17 is a host-RAM and training-systems improvement. It does not train a model, train a tokenizer, download data, change the core model architecture, enter A100/A800, or make model-quality claims.

The next GPU step should still be treated as bounded systems validation.
