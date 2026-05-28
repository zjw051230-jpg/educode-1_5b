# MVP-28.P Attention Backend Profiling Plan

## Scope

This step plans SDPA / FlashAttention profiling. It does not run Modal, does not request GPU, does not start training, does not install FlashAttention, and does not implement a new attention backend.

## Why MVP-28 Does Attention Profiling

MVP-26 and MVP-27 established a real A100 training baseline:

- Modal A100 5GB 3000-step completed.
- Final train loss improved from `3.160682` to `3.029707` versus 5GB 1000-step.
- Final validation loss improved from `9.214416` to `8.341638`.
- Validation coverage is now credible for a bounded run: `validation_unique_doc_count=15`, `validation_prefix_only_risk=false`.

That means the next most valuable work is not simply spending on more steps. Attention backend profiling adds systems depth and prepares the project for context-length, throughput, and B200 scale decisions.

## Why Not Direct 10000-step

Do not jump directly to 10000-step:

- The 3000-step run is one successful bounded run, not a full scaling law.
- More steps would add cost without explaining whether the current attention path is efficient.
- Current configs still use context length `512`; MVP-29 needs context-length planning.
- FlashAttention support is not implemented yet.
- A shorter profiling/preflight path can produce more useful engineering evidence at much lower cost.

## Current Attention Backend Status

Static readiness script:

```text
scripts/analyze_mvp28_p_attention_backend_readiness.py
```

Current findings:

| Field | Status |
| --- | --- |
| Attention implementation file | `src/educode/tiny_model.py` |
| Runtime attention implementation | `torch.nn.functional.scaled_dot_product_attention` |
| Causal masking | uses `is_causal=True` |
| Current backend | `sdpa` |
| SDPA ready | yes |
| Naive backend | config validator allows `naive`, but core model has no naive branch |
| FlashAttention backend | config validator allows `flash_attention_2`, but core model has no implementation/import |
| bf16/fp16 | training script uses CUDA autocast for bf16/fp16 |
| CUDA path | non-dry-run training requires CUDA |
| MPS path | config validator knows `mac_mps`, but current non-dry-run training path is CUDA-only |

Important nuance: config validation is ahead of runtime implementation. The validator allows `naive`, `sdpa`, and `flash_attention_2`, but `TinyModelConfig` and `CausalSelfAttention` currently reject non-`sdpa` runtime backends.

## Candidate Backends

| Backend | Current status | Profiling role |
| --- | --- | --- |
| naive/manual attention | Not implemented in core runtime | Useful as an explicit baseline only after a small implementation and correctness test |
| PyTorch SDPA | Implemented and currently used | Baseline for all profiling |
| FlashAttention / FlashAttention-2 | Not implemented; dependency not installed by this step | Optional candidate after environment support is confirmed |

## Mac MPS vs CUDA/A100

Mac MPS is useful for local development and shape/debug checks, but it is not equivalent to CUDA/A100 for backend profiling:

- PyTorch SDPA kernel selection differs by device, dtype, shape, and PyTorch version.
- FlashAttention is a CUDA-oriented path and should not be assumed available on MPS.
- The training script currently requires CUDA for non-dry-run training.
- A100 profiling should be the source of truth for tokens/sec, memory, and backend comparison.

## Existing Profiling Metadata

The training loop already records:

- per-step `tokens_per_sec`
- per-step `elapsed_seconds`
- per-step `gpu_memory_allocated_gib`
- per-step `gpu_memory_reserved_gib`
- summary `approximate_tokens_per_sec`
- summary `last_gpu_memory_allocated_gib`
- summary `last_gpu_memory_reserved_gib`
- `mfu`, currently emitted as `null`

A100 configs already contain:

- `profiling.enabled=true`
- `profiling.record_memory=true`
- `profiling.record_tokens_per_sec=true`
- `profiling.record_mfu=true`
- `profiling.attention_backend=sdpa`

## Profiling Metrics

MVP-28 profiling should compare:

- tokens/sec
- step time
- peak or last GPU memory allocated/reserved
- train loss sanity over a short run
- validation sanity if evaluation is enabled
- reproducibility of result rows and metadata
- backend label recorded in config, summary, and artifact names

The goal is system comparison, not model quality.

## Suggested Experiment Matrix

Initial bounded matrix:

| Dimension | Value |
| --- | --- |
| context length | `512` |
| batch size | `8` |
| gradient accumulation | `4` |
| model | current 300M-class config |
| data mode | streaming prepared data |
| steps | `20-50` profiling steps |
| baseline backend | `sdpa` |
| comparison backend | `naive` only after implementation; FlashAttention only if environment supports it |
| validation | optional sanity check, not quality claim |
| checkpoint | disabled or not imported; no large checkpoint committed |

Recommended first implementation:

1. Add a bounded profiling config/mode for SDPA only.
2. Add explicit backend labels to output paths and summaries.
3. Confirm profiling artifact rows and memory/tokens/sec fields.
4. Only then consider implementing naive or FlashAttention branches.

## Cost Boundary

This planning step costs `0` in Modal/GPU.

The next A100 profiling step should be much cheaper than the 5GB 3000-step training run because it should use only `20-50` steps. It still requires explicit cost approval before any Modal/GPU command.

## Success Criteria

MVP-28 implementation/profiling should be considered successful only if:

- it produces comparable profiling artifacts
- backend labels are unambiguous
- tokens/sec and step time are recorded
- GPU memory fields are recorded
- train loss sanity is finite
- validation sanity is finite if enabled
- no large checkpoint is committed
- no raw/prepared data or result tarball is committed

## Risks

- FlashAttention depends on package availability, CUDA/PyTorch compatibility, and GPU support.
- PyTorch SDPA kernel behavior can vary by version, dtype, shape, and environment.
- MPS behavior does not predict CUDA/A100 behavior.
- A naive backend may be slower and memory-heavier, so it should be bounded and tested locally first.
- Comparing backends requires careful control of config, data, seeds, and output naming.

## Next Step

Recommended next MVP:

```text
MVP-28.I: implement bounded attention profiling harness/configs before any profiling run
```

That step should still avoid long training. Any actual Modal/A100 profiling run requires a fresh cost gate.
