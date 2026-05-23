# MVP-14 + MVP-15 Next GPU Resource Requirements

## Purpose

This note records the resource lesson from the A800 public16k low-RAM fallback runs.

The next rental should avoid repeating the `16GiB` host/container RAM bottleneck that killed the original larger-batch attempts.

## Observed Bottleneck

The original public16k execution plan and `batch_size=8` / `gradient_accumulation_steps=4` fallback attempts were killed by the current `16GiB` container RAM limit.

The successful fallback used:

| field | value |
|---|---:|
| batch_size | `1` |
| gradient_accumulation_steps | `1` |
| sequence_length | `512` |
| model parameters | `336106496` |
| runtime dtype | `bf16` |

GPU memory was not the limiting resource. The host/container RAM limit was the issue.

## Recommended Next Rental

Minimum recommended instance:

- `1×A800/A100 40GB GPU`
- `16 CPU cores`
- `32GB+ host/container RAM`

Preferred instance:

- `1×A800/A100 40GB GPU`
- `16 CPU cores`
- `48GB` or `64GB` host/container RAM

The A800/A100 40GB GPU class remains sufficient for this stage. The requirement change is primarily host/container RAM.

## Alternative Engineering Route

If a higher-RAM instance is unavailable, improve the input pipeline before larger-batch execution:

- reduce host-side token accumulation;
- stream batches instead of building large token buffers;
- validate memory use before launching long runs;
- preserve standalone `validation_metrics.jsonl` and post-run artifact validation.

## Experiment Interpretation Boundary

The low-RAM fallback runs completed successfully, but they are not equivalent to the original larger effective batch plan. They should be used as evidence for:

- execution harness viability;
- logging and validation artifact correctness;
- checkpoint save/reload path correctness;
- low-batch bounded-run stability.

They should not be used as evidence for:

- model quality;
- final generalization;
- final training recipe;
- larger-batch throughput;
- production-grade data sampling.

## Next Decision

Before the next rental, decide between:

1. renting an A800/A100 instance with `32GB+` host/container RAM, preferably `48GB` or `64GB`;
2. improving streaming batch preparation locally before another GPU run;
3. keeping low-batch runs only for systems validation and moving model-quality work behind corpus/sampling improvements.
