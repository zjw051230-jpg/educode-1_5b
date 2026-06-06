# Branch Asset Inventory

This inventory records remote branch assets as of `main` commit `5931aa4` (`merge: add artifact hygiene guardrail`). It is a planning document only: no feature branch is merged, reviewed in detail, or executed here.

## Overview

- Current main commit: `5931aa4`
- Remote non-main branches covered: `27`
- Main status at inventory time: `main...origin/main`
- Scope: branch-level assets, likely review order, risk notes, and GPU/Modal gates.

## Categories

- docs/roadmap
- inference/eval
- attention/backend
- optimizer
- MoE
- RoPE/long context
- PEFT/LoRA
- quantization
- data/packing/quality
- diagnostics/reporting
- memory/training systems
- preference/reward

## Branch Table

| Branch | Commit | Category | Main Content | Main Files | Local Validation Result | GPU/Modal Gate | Risk | Suggested Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `docs/notebooklm-tech-synthesis` | `c1d9df9` | docs/roadmap | NotebookLM technical roadmap synthesis and branch roadmap. | `docs/notebooklm_tech_synthesis.md`, `docs/codex_branch_roadmap.md`, `docs/change_log.md` | Docs-only branch; pushed. | No | Low | review soon |
| `feature/training-report-generator` | `4fa21d5` | diagnostics/reporting | Markdown report generator from imported artifact summaries. | `scripts/build_training_report.py`, `tests/test_training_report_generator.py`, `docs/training_report_generator.md`, `docs/generated_reports/*` | py_compile, script run, 2 tests, diff check passed. | No | Low | review soon |
| `feature/loss-metric-diagnostics` | `941b942` | diagnostics/reporting | Metrics reader, finite loss checks, spike detection, divergence caveat. | `src/educode/diagnostics.py`, `scripts/analyze_loss_diagnostics.py`, `tests/test_loss_diagnostics.py`, `docs/loss_metric_diagnostics.md` | py_compile, script run, 3 tests, diff check passed. | No | Low | review soon |
| `feature/model-card-reproducibility` | `6847938` | docs/roadmap | Model card template, reproducibility checklist, local environment capture. | `docs/model_card_template.md`, `docs/reproducibility_checklist.md`, `scripts/capture_environment_summary.py`, `tests/test_reproducibility_docs.py` | py_compile, script run, 2 tests, diff check passed. | No | Low | review soon |
| `feature/sequence-packing-data-utilization` | `2f8a413` | data/packing/quality | Synthetic sequence packing and token utilization estimators. | `src/educode/packing.py`, `scripts/analyze_token_utilization.py`, `tests/test_sequence_packing.py`, `docs/sequence_packing_data_utilization.md` | py_compile, script run, 3 tests, diff check passed. | No for estimator; yes before training impact measurement. | Low | review soon |
| `feature/dataset-quality-dedup` | `bcd1359` | data/packing/quality | Tiny text quality metrics and shingle near-duplicate detection. | `src/educode/data_quality.py`, `scripts/analyze_dataset_quality.py`, `tests/test_data_quality.py`, `docs/dataset_quality_dedup.md` | py_compile, script run, 3 tests, diff check passed. | No for tiny fixtures; yes before large corpus scan. | Low | review soon |
| `feature/inference-kv-cache-harness-v2` | `53c7cdc` | inference/eval | Inference, sampling, KV cache, paged cache, and eval harness. | `src/educode/inference.py`, `src/educode/kv_cache.py`, `src/educode/paged_cache.py`, `src/educode/sampling.py`, `tests/test_inference_harness.py`, related docs/scripts | Local validation recorded on branch; pushed. | Yes for real checkpoint inference. | Medium | needs deeper review |
| `feature/inference-eval-harness` | `4fbdf0b` | inference/eval | Earlier inference/eval harness path. | `src/educode/eval.py`, `src/educode/generation.py`, `scripts/run_generation_smoke.py`, `tests/test_generation_eval_harness.py` | Local validation recorded on branch; pushed. | Yes for real checkpoint inference. | Medium | experimental only |
| `feature/quantization-qlora-feasibility` | `778cae2` | quantization | Quantization config, bitsandbytes availability check, fake quant helper. | `src/educode/quantization.py`, `scripts/check_quantization_feasibility.py`, `tests/test_quantization_feasibility.py`, `docs/quantization_qlora_feasibility.md` | py_compile, validator, 4 tests, diff check passed. | Yes for QLoRA training or CUDA compatibility. | Medium | needs deeper review |
| `feature/lora-peft-skeleton` | `61dae9b` | PEFT/LoRA | LoRA linear wrapper, PEFT target helper, adapter state filtering. | `src/educode/lora.py`, `src/educode/peft.py`, `scripts/validate_lora_peft.py`, `tests/test_lora_peft.py`, `docs/lora_peft_skeleton.md` | py_compile, validator, 4 tests, diff check passed. | Yes for adapter training. | Medium | needs deeper review |
| `feature/flashattention-feasibility` | `0f41445` | attention/backend | FlashAttention feasibility checker and docs. | `scripts/check_flashattention_feasibility.py`, `tests/test_flashattention_feasibility.py`, `docs/flashattention_feasibility.md` | Local validation recorded on branch; pushed. | Yes for install/profile. | Medium-High | needs deeper review |
| `feature/attention-backend-abstraction-v2` | `07516c3` | attention/backend | Extended attention backend abstraction and GQA utilities. | `src/educode/attention_backends.py`, `src/educode/attention_utils.py`, `src/educode/tiny_model.py`, `tests/test_attention_backends.py`, `tests/test_attention_gqa.py` | Local validation recorded on branch; pushed. | Yes for backend profiling. | High | needs deeper review |
| `feature/attention-backend-abstraction` | `98bd62c` | attention/backend | Earlier attention backend abstraction branch. | `src/educode/attention_backends.py`, `src/educode/tiny_model.py`, `tests/test_attention_backends.py`, `docs/attention_backend_abstraction.md` | Local validation recorded on branch; pushed. | Yes for backend profiling. | High | experimental only |
| `feature/attention-backend-prep` | `c96ed24` | attention/backend | Early attention backend prep path. | `src/educode/attention_backends.py`, `src/educode/tiny_model.py`, `scripts/check_attention_backend_availability.py`, `docs/attention_backend_prep.md` | Local validation recorded on branch; pushed. | Yes for backend profiling. | High | experimental only |
| `feature/rope-position-encoding-v2` | `8885cc4` | RoPE/long context | RoPE helpers, position encoding path, passkey fixture script. | `src/educode/rope.py`, `src/educode/position_encoding.py`, `scripts/validate_position_encoding.py`, `tests/test_rope_cache.py` | Local validation recorded on branch; pushed. | Yes for long-context profiling. | High | needs deeper review |
| `feature/rope-position-prep` | `2eecc04` | RoPE/long context | Earlier RoPE position encoding prep path. | `src/educode/position_encoding.py`, `scripts/validate_rope_position_encoding.py`, `tests/test_position_encoding.py`, `docs/rope_position_encoding_prep.md` | Local validation recorded on branch; pushed. | Yes for long-context profiling. | High | experimental only |
| `feature/muon-experimental-optimizer` | `e5555ef` | optimizer | Guarded Muon optimizer experiment and optimizer registry tests. | `src/educode/muon.py`, `src/educode/optimizers.py`, `scripts/validate_optimizer_registry.py`, `tests/test_muon_experimental.py` | Local validation recorded on branch; pushed. | Yes for Muon vs AdamW training. | High | needs deeper review |
| `feature/optimizer-registry-muon` | `9657fda` | optimizer | Earlier optimizer registry and Muon guard path. | `src/educode/optimizers.py`, `scripts/validate_optimizer_registry.py`, `tests/test_optimizer_registry.py`, `docs/optimizer_registry_and_muon_prep.md` | Local validation recorded on branch; pushed. | Yes for Muon vs AdamW training. | High | experimental only |
| `feature/moe-routing-skeleton-v2` | `5d09791` | MoE | MoE routing, sparse layer skeleton, auxiliary losses. | `src/educode/moe_routing.py`, `src/educode/moe_layers.py`, `scripts/validate_moe_routing.py`, `tests/test_moe_routing.py`, `tests/test_moe_losses.py` | Local validation recorded on branch; pushed. | Yes for MoE training/profiling. | High | needs deeper review |
| `feature/moe-routing-prep` | `bb0bc7c` | MoE | Earlier MoE routing prep branch. | `src/educode/moe_layers.py`, `scripts/validate_moe_routing.py`, `tests/test_moe_routing.py`, `docs/moe_routing_prep.md` | Local validation recorded on branch; pushed. | Yes for MoE training/profiling. | High | experimental only |
| `feature/memory-knobs-activation-checkpointing` | `3ece41b` | memory/training systems | Activation checkpointing config and wrapper. | `src/educode/memory.py`, `scripts/validate_memory_knobs.py`, `tests/test_memory_knobs.py`, `docs/memory_knobs_activation_checkpointing.md` | py_compile, validator, 3 tests, diff check passed. | Yes for memory profiling/training integration. | High | needs deeper review |
| `feature/preference-optimization-skeleton` | `7f0f5c5` | preference/reward | Preference pair schema and DPO loss helper. | `src/educode/preference.py`, `src/educode/dpo.py`, `scripts/validate_preference_dataset.py`, `tests/test_dpo_loss.py` | py_compile, validator, 3 tests, diff check passed. | Yes for preference tuning. | Medium | keep as-is |
| `feature/reward-model-skeleton` | `45b9cdc` | preference/reward | Reward head, reward pair schema, pairwise ranking loss. | `src/educode/reward_model.py`, `scripts/validate_reward_dataset.py`, `tests/test_reward_model.py`, `docs/reward_model_skeleton.md` | py_compile, validator, 3 tests, diff check passed. | Yes for reward model training. | Medium | keep as-is |
| `feature/profiling-matrix-planner` | `8cd26e4` | diagnostics/reporting | Profiling matrix and next experiment candidate planner. | `scripts/build_profiling_matrix.py`, `docs/profiling_matrix.md`, `docs/profiling_matrix.json`, `docs/next_experiment_candidates.md` | Local validation recorded on branch; pushed. | No for planner; yes for generated profiling runs. | Low-Medium | likely merge later |
| `feature/experiment-planner` | `34cb2ec` | docs/roadmap | Experiment matrix planner and candidate docs. | `scripts/build_experiment_matrix.py`, `docs/experiment_matrix.md`, `docs/experiment_matrix.json`, `docs/next_experiment_candidates.md` | Local validation recorded on branch; pushed. | No for planner; yes for scheduled runs. | Low-Medium | likely merge later |
| `feature/config-schema-hardening` | `aa7fc8b` | memory/training systems | Training config schema hardening. | `src/educode/config_schema.py`, `scripts/validate_config_schema_hardening.py`, `tests/test_config_schema_hardening.py` | Local validation recorded on branch; pushed. | No direct GPU gate; impacts future run gates. | Medium | needs deeper review |
| `feature/checkpoint-artifact-hygiene` | `e622451` | memory/training systems | Artifact hygiene checker, already merged into main. | Already in main; no remaining diff versus `main`. | Merged and validated in `main`. | No | Low | keep as-is |

## Recommended Review / Merge Order

Low-risk branches should be reviewed before branches that alter model internals, optimizer behavior, attention execution, or training memory semantics.

1. `docs/notebooklm-tech-synthesis`
2. `feature/training-report-generator`
3. `feature/loss-metric-diagnostics`
4. `feature/model-card-reproducibility`
5. `feature/sequence-packing-data-utilization`
6. `feature/dataset-quality-dedup`
7. `feature/inference-kv-cache-harness-v2`
8. `feature/quantization-qlora-feasibility`
9. `feature/lora-peft-skeleton`
10. `feature/flashattention-feasibility`
11. `feature/attention-backend-abstraction-v2`
12. `feature/rope-position-encoding-v2`
13. `feature/muon-experimental-optimizer`
14. `feature/optimizer-registry-muon`
15. `feature/moe-routing-skeleton-v2`
16. `feature/memory-knobs-activation-checkpointing`

Older prep branches should generally stay experimental unless they contain a file or idea missing from the newer v2 branch.

## Branches Not To Merge Directly

These branches should not be batch-merged or merged without deeper review:

- Attention backend abstraction branches:
  - `feature/attention-backend-abstraction-v2`
  - `feature/attention-backend-abstraction`
  - `feature/attention-backend-prep`
- Muon optimizer branches:
  - `feature/muon-experimental-optimizer`
  - `feature/optimizer-registry-muon`
- MoE branches:
  - `feature/moe-routing-skeleton-v2`
  - `feature/moe-routing-prep`
- Memory checkpointing branch:
  - `feature/memory-knobs-activation-checkpointing`
- RoPE branches:
  - `feature/rope-position-encoding-v2`
  - `feature/rope-position-prep`

## GPU / Modal Gate Checklist

The following follow-up work requires explicit paid GPU/Modal confirmation before execution:

- Attention backend profiling.
- FlashAttention install/profile.
- Muon vs AdamW training.
- MoE training.
- RoPE long-context profiling.
- Real checkpoint inference.
- LoRA/QLoRA training.
- Reward/preference tuning.

## Current Prohibitions

- No Modal.
- No GPU.
- No training.
- No tarball/checkpoint/raw data commit.
- No batch merge.
- No PR without review.
