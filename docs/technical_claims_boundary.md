# Technical Claims Boundary

This document lists claims that are supported, branch-only, planned, or explicitly not yet supported.

## Supported By Main

- FineWeb-Edu 5GB 3000-step training evidence exists as imported small artifacts.
- seq512 and seq1024 A100 SDPA profiling evidence exists as imported small artifacts.
- Artifact hygiene guardrails exist in `main`.
- Short profiling losses are sanity signals, not model-quality evidence.

## Branch-Only Claims

These may be described only as branch-local prototypes until reviewed and merged:

- KV cache and inference harness.
- Attention backend abstraction.
- RoPE/long-context helpers.
- Muon optimizer guardrails.
- MoE routing skeleton.
- LoRA/PEFT utilities.
- Quantization/QLoRA feasibility.
- Dataset quality, packing, diagnostics, preference, and reward skeletons.

## Planned Claims

These should be described as plans, not implemented capabilities:

- FSDP, ZeRO, tensor parallel, sequence parallel, or Megatron-style execution.
- Multi-GPU training.
- B200 training.
- FlashAttention performance comparison.
- Real QLoRA/LoRA training.
- Preference or reward tuning.

## Do Not Claim Yet

- Do not claim production model quality.
- Do not claim SDPA is faster than naive attention or FlashAttention without matched baselines.
- Do not claim seq1024 long training is safe based only on bounded profiling.
- Do not claim distributed training support until a reviewed implementation and a gated run exist.
- Do not claim real checkpoint inference until the inference branch is reviewed and run under an explicit gate.
