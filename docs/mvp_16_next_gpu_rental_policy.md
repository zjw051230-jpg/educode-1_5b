# MVP-16 Next GPU Rental Policy

## Purpose

This note records the next rental policy after the A800 public16k low-RAM fallback runs.

The current bottleneck is host/container RAM and batch preparation, not GPU VRAM.

## GPU Requirement

A single `A800/A100 40GB` GPU remains sufficient for the next engineering validation step.

Do not rent H200/B200 to solve this bottleneck. A larger GPU does not address Python host-memory pressure from run-sized batch materialization.

## Host / Container RAM Requirement

Minimum:

- `32GB+` host/container RAM

Recommended:

- `16 CPU cores`
- `48GB` host/container RAM
- `1×A800/A100 40GB`

Ideal:

- `16 CPU cores`
- `64GB` host/container RAM
- `1×A800/A100 40GB`

Select `16核/48G` if available.

## Environment Guidance

Avoid unnecessary VNC/Jupyter overhead if possible. Prefer a lean shell execution environment that leaves more RAM available for Python and dataloader work.

Before launching a real run, execute the memory inspection script and check whether the active config is still using list-based batch materialization.

## If Only 16GB RAM Is Available

If the provider only exposes about `16GiB` container RAM:

- use `batch_size=1` fallback only;
- do not attempt the original `batch_size=8` / `gradient_accumulation_steps=4` path;
- do not treat low-batch results as model-quality training;
- use the run only for systems validation;
- prioritize streaming batch iterator work before spending more GPU rental time.

## Preferred Next Run Order

1. Implement or validate streaming batch preparation.
2. Run a local memory inspection.
3. Run a short A800/A100 smoke with streaming mode.
4. Only then retry larger effective batch settings.

Candidate fallback order after streaming exists:

1. `batch_size=8` / `gradient_accumulation_steps=4`;
2. `batch_size=4` / `gradient_accumulation_steps=4`;
3. `batch_size=4` / `gradient_accumulation_steps=2`;
4. `batch_size=2` / `gradient_accumulation_steps=4`.

## Interpretation Boundary

A successful low-RAM run validates the execution chain, not model quality. A future higher-RAM or streaming-mode run should still be reviewed as bounded training-systems evidence unless corpus scale, sampling, validation, and evaluation are also improved.
