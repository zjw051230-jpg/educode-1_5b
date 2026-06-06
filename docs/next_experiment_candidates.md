# Next Experiment Candidates

These are planning candidates only. Any GPU or Modal run requires a separate cost gate and explicit user confirmation.

## 1. mvp31_seq1024_bs8_memory_preflight

- Status: `planned_requires_gpu`
- Category: `memory_preflight`
- Requires GPU: `True`
- Requires Modal: `True`
- Cost gate: required before A100 run
- Rationale: Tests whether seq1024 can safely return to batch_size=8 after bs4 no-OOM evidence.

## 2. naive_attention_baseline

- Status: `planned_local_then_gpu`
- Category: `attention_backend`
- Requires GPU: `False`
- Requires Modal: `False`
- Cost gate: GPU confirmation needed only for measured profiling
- Rationale: Creates a correctness and profiling comparison point for SDPA without claiming speedup yet.

## 3. flashattention_feasibility

- Status: `planned_local_feasibility`
- Category: `attention_backend`
- Requires GPU: `False`
- Requires Modal: `False`
- Cost gate: GPU confirmation needed only after dependency feasibility passes
- Rationale: Checks optional FlashAttention2 path and install/runtime risks before any A100 comparison.

## 4. adamw_vs_muon_optimizer_prep

- Status: `planned_local_prep`
- Category: `optimizer`
- Requires GPU: `False`
- Requires Modal: `False`
- Cost gate: GPU confirmation needed for future training comparison
- Rationale: Adds optimizer registry and guarded Muon experiment path while keeping AdamW default.

## 5. moe_routing_prep

- Status: `planned_local_prep`
- Category: `moe`
- Requires GPU: `False`
- Requires Modal: `False`
- Cost gate: GPU confirmation needed only after MoE config is explicitly enabled
- Rationale: Prepares routing and expert skeleton without changing dense baseline behavior.

## 6. rope_long_context_prep

- Status: `planned_local_prep`
- Category: `position_encoding`
- Requires GPU: `False`
- Requires Modal: `False`
- Cost gate: GPU confirmation needed for future long-context profiling
- Rationale: Prepares RoPE/position encoding switch for later long-context experiments.

## 7. mvp_future_5gb_5000step_continuation

- Status: `planned_requires_gpu`
- Category: `training`
- Requires GPU: `True`
- Requires Modal: `True`
- Cost gate: required before any longer A100 training
- Rationale: Possible quality-trend continuation after systems guardrails mature.
