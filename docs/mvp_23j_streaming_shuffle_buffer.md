# MVP-23.J Streaming Shuffle Buffer Implementation

## Scope

MVP-23.J adds seed-controlled shuffle-buffer sampling to the streaming JSONL data path so future 2GB/5GB prepared-corpus training runs do not consume only the sequential prefix of the train split.

This step stays local-only:

- no Modal run
- no A100/A800 session
- no real training
- no tokenizer/model training
- no checkpoint generation
- no data download
- no raw, processed, split, prepared tarball, result tarball, or checkpoint artifact promotion

## Sampling Config Schema

The 2GB/5GB A100/A800 execution configs now declare:

```json
"sampling": {
  "policy": "shuffle_buffer",
  "shuffle_seed": 1337,
  "shuffle_buffer_size": 1024
}
```

The legacy/default behavior remains `sequential_prefix` when no sampling config is present. For `shuffle_buffer`, the config parser requires `shuffle_buffer_size > 1` and uses `sampling.shuffle_seed` when present, falling back to `run.seed` only if an explicit shuffle seed is absent.

## Iterator Behavior

`scripts/streaming_lm_batch_iterator.py` now supports two sampling policies before tokenization:

| Policy | Behavior | Prefix-only metadata |
|---|---|---|
| `sequential_prefix` | preserves the old JSONL document order | `bounded_prefix_batches_only=true` |
| `shuffle_buffer` | keeps at most `shuffle_buffer_size` documents in memory and emits seeded pseudo-random documents from that buffer | `bounded_prefix_batches_only=false` |

The implementation uses `random.Random(seed)` rather than global randomness. It does not load the full corpus; only the bounded shuffle buffer and the existing rolling token/batch buffers are held in memory.

Probe metadata now includes:

- `sampling_policy`
- `shuffle_seed`
- `shuffle_buffer_size`
- `documents_buffered_total`
- `max_shuffle_buffer_occupancy`
- `shuffle_buffer_underfilled`
- `bounded_prefix_batches_only`
- `last_shuffle_seed_used`

## Training Script Metadata

`scripts/run_a100_300m_fineweb_edu_10step_training.py` now reads the sampling config and passes it to the streaming iterator for the `train` split.

Validation remains `sequential_prefix` to keep validation-loss sampling comparable across bounded runs. The dry-run and real-run summaries record:

- top-level sampling metadata from the train policy
- `train_sampling_policy`
- `val_sampling_policy`
- train/val probe-level sampling metadata

Fixed-LR scheduler metadata remains unchanged from MVP-23.I: `scheduler_policy=constant`, `scheduler_applied=false`, and `learning_rate_mode=constant`.

## Readiness and Memory Inspection

`scripts/check_a100_execution_readiness.py` now checks sampling policy for 2GB/5GB execution configs. These configs must declare `shuffle_buffer`, integer `shuffle_seed`, `shuffle_buffer_size > 1`, and `bounded_prefix_batches_only=false`.

`scripts/inspect_training_batch_memory_plan.py` now reports sampling metadata plus a bounded shuffle-buffer memory estimate based on at most `MAX_SAMPLE_RECORDS` local records. It still does not scan the full corpus.

## Updated Execution Configs

The following configs now use `shuffle_buffer` with seed `1337` and buffer size `1024`:

- `configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json`
- `configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json`
- `configs/a100/fineweb_edu_2gb_300m_5000step_public16k_execute.json`
- `configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json`
- `configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json`

Their `data.bounded_prefix_batches_only` metadata is now `false`.

## Local Validation Evidence

Commands run locally:

```text
./.venv/Scripts/python.exe -m py_compile scripts/streaming_lm_batch_iterator.py scripts/run_a100_300m_fineweb_edu_10step_training.py scripts/check_a100_execution_readiness.py scripts/inspect_training_batch_memory_plan.py
./.venv/Scripts/python.exe tests/test_streaming_lm_batch_iterator.py && ./.venv/Scripts/python.exe tests/test_sampling_policy_config.py
./.venv/Scripts/python.exe scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json --dry-run
./.venv/Scripts/python.exe scripts/check_a100_execution_readiness.py --config configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json
./.venv/Scripts/python.exe scripts/check_a100_execution_readiness.py --config configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json
./.venv/Scripts/python.exe scripts/check_a100_execution_readiness.py --config configs/a100/fineweb_edu_2gb_300m_5000step_public16k_execute.json
./.venv/Scripts/python.exe scripts/check_a100_execution_readiness.py --config configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json
./.venv/Scripts/python.exe scripts/check_a100_execution_readiness.py --config configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json
./.venv/Scripts/python.exe scripts/inspect_training_batch_memory_plan.py --config configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json
```

Observed local results:

- py_compile: pass
- streaming iterator tests: `Ran 11 tests ... OK`
- sampling config tests: `Ran 7 tests ... OK`
- 2GB 1000-step dry-run: `sampling_policy=shuffle_buffer`, `shuffle_seed=1337`, `shuffle_buffer_size=1024`, `bounded_prefix_batches_only=False`, `no_training=True`
- five readiness checks: `status=success`, `ready_for_a100_execution=True`, `ready_for_a800_execution=True`, `caveats=0`, `blockers=0`
- 2GB 1000-step memory inspection: `streaming_expected_host_ram_safe=True`, `sampling_policy=shuffle_buffer`, `shuffle_seed=1337`, `shuffle_buffer_size=1024`, `no_training=True`

## Interpretation

This resolves the previous `bounded_prefix_batches_only` interpretability caveat for the prepared 2GB/5GB execution configs. It does not make a model-quality claim and does not change tokenizer, model architecture, batch size, gradient accumulation, max steps, or fixed-LR behavior.

## Recommended Next Step

Run a local/Modal preflight for the 5GB 1000-step config or schedule an explicitly approved GPU run only after cost approval. Do not treat this cleanup as evidence that longer 2GB step counts will improve validation quality.
