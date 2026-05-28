# MVP-28.A A100 SDPA Profile Result Analysis

## Scope

This analysis reads the imported Modal A100 50-step SDPA profiling artifact. It does not run Modal, does not request GPU, does not start training, and does not implement any new attention backend.

## Inputs

Imported artifact directory:

```text
experiments/a100/fineweb_edu_5gb_300m_50step_public16k_sdpa_profile/results_imported_modal_streaming/
```

Key files:

- `summary.json`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`

## Result

SDPA profiling succeeded. Modal app completed in MVP-28.R, the run used A100-40GB, the post-run artifact validator reported blocker count `0`, and the imported result validator passed.

This was not quality training. It was a bounded systems profiling run: `50` steps, context length `512`, batch size `8`, gradient accumulation `4`, and attention backend `sdpa`. Loss values are only sanity signals that the short run executed with finite loss.

| Metric | Value |
| --- | --- |
| attention backend | `sdpa` |
| max steps | `50` |
| metrics rows | `50` |
| validation rows | `1` |
| final train loss | `4.328258` |
| final validation loss | `8.897261` |
| summary tokens/sec | `44100.712407` |
| mean per-step tokens/sec | `46732.188322` |
| average step time | `0.371513s` |
| peak allocated memory | `2.645120 GiB` |
| peak reserved memory | `8.416016 GiB` |
| MFU | unavailable / `null` |

## Throughput

The summary-level throughput was `44100.712407` tokens/sec. The mean per-step throughput across all 50 metric rows was `46732.188322` tokens/sec.

The first step was slower because it included startup/warmup effects, while later steps settled around the high-47k tokens/sec range. This is enough to serve as an initial SDPA baseline for the current 300M-class, public16k, sequence-length-512 training path.

It is not a comparative result. Without a naive/manual attention run, this does not prove SDPA is faster than naive attention. Without a FlashAttention implementation and run, this does not compare against FlashAttention.

## Step Time

Average per-step time was `0.371513s`. The late-run rows were closer to roughly `0.345s`, while the first row was slower due to warmup. For future backend comparisons, reports should separate all-step average from warmup-excluded average if the goal is precise throughput comparison.

## Memory

Peak allocated memory was `2.645120 GiB`; peak reserved memory was `8.416016 GiB`. This indicates the current 300M-class SDPA seq512 profile is comfortably within A100-40GB memory for this batch/accumulation shape.

The memory result is useful as a baseline for MVP-29 context-length work. It does not by itself prove seq1024 is safe, because attention memory and activation behavior change with sequence length.

## MFU Caveat

MFU was requested in the config, but imported metric rows emit `mfu=null`. That means MFU is unavailable for this run. The likely reason is that the current training loop records the field but does not compute a hardware-specific FLOP utilization estimate.

This is a caveat, not a blocker. Tokens/sec, step time, and GPU memory were recorded and are enough for a first SDPA systems baseline.

## Loss Caveat

The final train loss was `4.328258` and final validation loss was `8.897261`. These are finite sanity signals only. A 50-step profiling run is too short to support model-quality claims, validation-quality conclusions, or scaling-law decisions.

## Resume Value

The result is valuable for systems-oriented project narrative:

- implemented a bounded A100 profiling harness instead of using long training as a proxy for performance
- recorded SDPA throughput, step time, and GPU memory on real A100-40GB
- separated readiness validation, post-run artifact validation, and imported-result analysis
- documented that profiling evidence is not model-quality evidence

This is a stronger engineering story than simply adding more training steps.

## Is This Enough As The SDPA Baseline?

Yes, it is enough as an initial SDPA baseline for the current shape:

- 300M-class model
- context length `512`
- batch size `8`
- gradient accumulation `4`
- 5GB prepared FineWeb-Edu streaming data
- A100-40GB

It is not enough as a backend comparison. A comparison needs either a naive/manual attention baseline or a FlashAttention implementation/audit path.

## Next Route Decision

Naive/manual attention baseline is useful, but it requires implementation and correctness checks before profiling. FlashAttention should not be run directly yet because the dependency and runtime path are not implemented.

The recommended MVP-29 is:

```text
MVP-29.P context length 512 -> 1024 memory/preflight plan
```

Reasoning:

- SDPA seq512 baseline now exists.
- Peak reserved memory at seq512 leaves room for a bounded seq1024 preflight design.
- Context-length scaling is directly relevant to LLM training systems.
- It should remain a preflight/plan first, not an immediate long training run.

Secondary follow-ups:

- MVP-29.N naive/manual attention baseline for profiling comparison
- MVP-29.F FlashAttention feasibility audit

Do not jump directly to another long training run or claim FlashAttention comparison until the runtime path exists.
