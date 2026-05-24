# MVP-18 A800 Streaming 1000-Step Execution Plan

## Purpose

MVP-18 is the next approved-candidate GPU execution step after MVP-17 streaming batch preparation.

The goal is to run the 300M public16k 1000-step config with streaming batch preparation on a host/container with enough RAM, then decide whether a 3000-step follow-up is still useful.

## Preconditions

Before any GPU rental or remote execution:

1. Keep `data.data_loading_mode = "streaming"` in the 1000-step config.
2. Confirm local dry-run still reports `data_loading_mode=streaming` and `batch_precompute_disabled=True`.
3. Confirm memory inspection still reports `streaming_expected_host_ram_safe=True`.
4. Confirm no checkpoints, `raw.jsonl`, `processed/`, `splits/`, or result tarballs are staged for commit.
5. Get explicit approval for real GPU execution.

## Recommended Hardware

Use the MVP-16 rental policy:

- minimum: `32GB+` host/container RAM;
- recommended: `16 CPU cores`, `48GB` host/container RAM, `1×A800/A100 40GB`;
- ideal: `16 CPU cores`, `64GB` host/container RAM, `1×A800/A100 40GB`.

Do not rent H200/B200 to solve this bottleneck. The previous issue was Python host-memory pressure, not GPU VRAM.

## Local Preflight Commands

Run these before copying the command set to a remote A800/A100 environment:

```text
.venv/Scripts/python.exe scripts/inspect_training_batch_memory_plan.py --config configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json
```

```text
.venv/Scripts/python.exe scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json --dry-run
```

```text
.venv/Scripts/python.exe scripts/inspect_streaming_public16k_data_model_loss_smoke.py --config configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json
```

These commands are bounded local validation only. They do not perform real training.

## First Remote Run

After explicit approval, run the 1000-step streaming config first:

```text
.venv/Scripts/python.exe scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json
```

Expected active settings:

```text
data_loading_mode=streaming
batch_size=8
gradient_accumulation_steps=4
sequence_length=512
max_steps=1000
eval_interval=100
checkpoint_interval=1000
tokenizer_vocab_size=16384
exact_parameter_count=336106496
```

## Success Criteria

The run is usable as bounded systems evidence only if:

- `metrics.jsonl` has `1000` rows;
- `validation_metrics.jsonl` has `10` rows;
- all train and validation losses are finite;
- checkpoint reload matches;
- `summary.json` records `data_loading_mode=streaming`;
- `summary.json` records `batch_precompute_disabled=True`;
- `post_run_artifact_validation_summary.json` passes;
- no artifact path escapes the configured output directory.

## Follow-Up Decision

Only consider the 3000-step config if the 1000-step streaming run succeeds and rental time remains.

If the 1000-step run fails due to host RAM, stop and inspect the active container memory and streaming summary fields before trying smaller batch fallbacks.

Fallback order if streaming is active but host RAM still fails:

1. `batch_size=4` / `gradient_accumulation_steps=4`;
2. `batch_size=4` / `gradient_accumulation_steps=2`;
3. `batch_size=2` / `gradient_accumulation_steps=4`.

Do not return to `batch_size=1` as a model-quality run. That fallback remains systems-only evidence.

## Interpretation Boundary

MVP-18 should still be reported as bounded training-systems validation. It does not establish model quality, corpus sufficiency, tokenizer quality, or generalization.
