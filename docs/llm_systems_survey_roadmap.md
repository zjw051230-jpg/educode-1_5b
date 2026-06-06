# LLM Systems Survey Roadmap

This roadmap maps modern LLM training-system directions onto the current EduCode-1.5B project state. It is a planning and claims-boundary document only; no Modal, GPU, training, profiling, or feature-branch merge was performed for this branch.

## Current Project Position

EduCode-1.5B is strongest today as a reproducible training-systems portfolio project. The evidence base includes local code, Modal A100 execution gates, imported small artifacts, artifact hygiene, validation coverage notes, and bounded SDPA profiling runs.

## Systems Areas

| Area | Current Status | Evidence Level | Next Useful Step |
| --- | --- | --- | --- |
| Data loading and artifact hygiene | Implemented in `main` | Committed code/docs and run artifacts | Keep guardrails before every result import |
| A100 SDPA profiling | Implemented in `main` | seq512 and seq1024 bounded profiling | Compare against carefully reviewed backend alternatives |
| Inference / KV cache | Branch-only | `feature/inference-kv-cache-harness-v2` | Review before real checkpoint inference |
| Attention backend abstraction | Branch-only | attention abstraction branches | Deep review before merge; GPU profiling gate |
| RoPE / long context | Branch-only | RoPE branches | Deep review; long-context memory/profile gate |
| Muon optimizer | Branch-only | Muon optimizer branches | Experimental only until AdamW comparison is designed |
| MoE routing | Branch-only | MoE skeleton branches | Experimental only until routing/load-balance risks are reviewed |
| LoRA / PEFT | Branch-only | LoRA skeleton branch | Review adapter state/checkpoint policy before training |
| Quantization / QLoRA | Branch-only | quantization feasibility branch | GPU/Modal feasibility gate before real 4-bit load |
| Distributed training | Planned | This second-batch branch family | Keep as local schema/planning until multi-GPU gate |
| Preference / reward tuning | Branch-only | preference/reward skeleton branches | Data policy and cost gate before tuning |

## Seven-Day Roadmap

1. Review low-risk documentation and reporting branches.
2. Review data utilization and data quality utilities.
3. Review inference/KV cache API without loading a real checkpoint.
4. Review LoRA and quantization feasibility branches for claims and artifact boundaries.
5. Keep attention, RoPE, Muon, MoE, and activation checkpointing branches experimental until deeper review.

## Thirty-Day Roadmap

1. Merge low-risk reporting and reproducibility assets after review.
2. Build a single consolidated data-quality and packing utility branch from the best parts of v1/v2 branches.
3. Decide one backend comparison path: SDPA vs naive/manual attention or FlashAttention feasibility.
4. Decide one memory path: seq1024 batch-size gate or activation checkpointing review.
5. Design a multi-GPU/distributed training plan without executing it until explicit cost approval.

## GPU-Gated Work

- Backend profiling beyond current SDPA baselines.
- FlashAttention install/profile.
- RoPE long-context profiling.
- Muon vs AdamW training comparison.
- MoE training/profiling.
- LoRA/QLoRA training.
- Preference/reward tuning.
- Real checkpoint inference and generation evaluation.
- Multi-GPU or B200 experiments.

## Practical Review Priority

Start with docs/reporting/data utilities because they are low-risk and improve project readability. Then review inference and PEFT/quantization. Treat model-internal changes as deeper review items.
