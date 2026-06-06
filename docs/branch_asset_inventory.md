# Branch Asset Inventory

This inventory records remote branch assets as of `main` commit `565fc42` (`docs: update branch asset inventory`). It is a planning document only: no feature branch is merged, reviewed in detail, or executed here.

## Overview

- Current main commit at V2 refresh start: `565fc42`
- Current remote non-main branches total: `44`
- Detailed branch assets covered: `36`
- Remote non-main branches not yet detailed: `8`
- Main status at inventory time: `main...origin/main`
- Scope: branch-level assets, likely review order, risk notes, and GPU/Modal gates.
- V2 update: second-batch data-driven branches are included in a dedicated section below.

## Remote Coverage Snapshot

- Covered in detailed inventory: `36` branches.
- Second-batch data-driven branches covered in this update: `9` branches.
- Remote branches still listed for later inventory expansion: `feature/auto-report-packager`, `feature/cli-experiment-manager`, `feature/eval-benchmark-harness`, `feature/instruction-tuning-data-skeleton`, `feature/model-compression-distillation`, `feature/rag-retrieval-skeleton`, `feature/run-registry-database`, `feature/serving-api-skeleton`.

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

## Completed Technical Branch Classification

| Category | Branches |
| --- | --- |
| docs/roadmap | `docs/notebooklm-tech-synthesis`, `docs/llm-systems-survey-roadmap`, `feature/experiment-planner` |
| inference/eval | `feature/inference-kv-cache-harness-v2`, `feature/inference-eval-harness` |
| attention/backend | `feature/attention-backend-abstraction-v2`, `feature/attention-backend-abstraction`, `feature/attention-backend-prep`, `feature/flashattention-feasibility` |
| optimizer | `feature/muon-experimental-optimizer`, `feature/optimizer-registry-muon` |
| MoE | `feature/moe-routing-skeleton-v2`, `feature/moe-routing-prep` |
| RoPE/long context | `feature/rope-position-encoding-v2`, `feature/rope-position-prep` |
| PEFT/LoRA | `feature/lora-peft-skeleton`, `feature/lora-peft-v2` |
| quantization | `feature/quantization-qlora-feasibility`, `feature/qlora-quantization-v2` |
| data/packing/quality | `feature/sequence-packing-data-utilization`, `feature/dataset-quality-dedup`, `feature/sequence-packing-v2`, `feature/dataset-quality-dedup-v2`, `feature/tokenizer-stats-analyzer` |
| diagnostics/reporting | `feature/training-report-generator`, `feature/loss-metric-diagnostics`, `feature/profiling-matrix-planner` |
| memory/training systems | `feature/checkpoint-artifact-hygiene`, `feature/config-schema-hardening`, `feature/memory-knobs-activation-checkpointing`, `feature/distributed-config-memory-estimator`, `feature/distributed-launch-feasibility`, `feature/activation-checkpointing-v2` |
| preference/reward | `feature/preference-optimization-skeleton`, `feature/reward-model-skeleton` |

## Second-Batch Data-Driven Branches

| Branch | Commit | Category | Main Content | Main Files | Local Validation Result | GPU/Modal Gate | Risk | Suggested Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `docs/llm-systems-survey-roadmap` | `ed45fde` | docs/roadmap | LLM systems roadmap, claims boundary, and resume narrative. | `docs/llm_systems_survey_roadmap.md`, `docs/technical_claims_boundary.md`, `docs/resume_project_narrative.md` | `git diff --check` passed. | No | Low | review soon |
| `feature/distributed-config-memory-estimator` | `e3ad6cc` | memory/training systems | Distributed config, gradient accumulation accounting, and rough memory estimator. | `docs/distributed_config_memory_estimator.md`, `src/educode/distributed_config.py`, `src/educode/grad_accum.py`, `src/educode/memory_estimator.py`, `scripts/validate_distributed_config.py`, `scripts/estimate_training_memory.py`, `tests/test_distributed_config.py`, `tests/test_grad_accum_accounting.py`, `tests/test_memory_estimator.py` | py_compile, validator script, estimator script, 7 tests, diff check passed. | Yes for multi-GPU validation. | High | experimental only |
| `feature/distributed-launch-feasibility` | `e2f0ebf` | memory/training systems | FSDP / ZeRO / Megatron launch planner; generates command strings only. | `scripts/plan_distributed_launch.py`, `scripts/check_fsdp_zero_feasibility.py`, `tests/test_distributed_launch_planner.py`, `docs/fsdp_zero_megatron_feasibility.md`, `docs/distributed_launch_planner.md` | py_compile, planner script, feasibility script, 4 tests, diff check passed. | Yes for any real launch. | High | experimental only |
| `feature/activation-checkpointing-v2` | `f6808fc` | memory/training systems | Activation checkpointing config/wrapper with CPU synthetic backward. | `src/educode/activation_checkpointing.py`, `src/educode/memory_knobs.py`, `scripts/validate_activation_checkpointing.py`, `tests/test_activation_checkpointing.py`, `docs/activation_checkpointing_v2.md` | py_compile, validator, 4 tests, diff check passed. | Yes for profiling/training integration. | High | needs deeper review |
| `feature/lora-peft-v2` | `377756a` | PEFT/LoRA | LoRA wrapper, adapter state dict, merge/unmerge guard, trainable parameter report. | `src/educode/lora.py`, `src/educode/peft.py`, `scripts/validate_lora_peft_v2.py`, `tests/test_lora_peft_v2.py`, `docs/lora_peft_v2.md` | py_compile, validator, 5 tests, diff check passed. | Yes for LoRA training. | Medium | needs deeper review |
| `feature/qlora-quantization-v2` | `9b1ddfb` | quantization | QLoRA config, bitsandbytes/CUDA guard, fake quant/dequant helpers. | `src/educode/quantization.py`, `scripts/check_quantization_feasibility_v2.py`, `scripts/validate_qlora_config.py`, `tests/test_quantization_v2.py`, `docs/qlora_quantization_v2.md`, `docs/dora_loftq_feasibility.md` | py_compile, 2 scripts, 4 tests, diff check passed. | Yes for 4-bit load/training. | Medium | needs deeper review |
| `feature/sequence-packing-v2` | `7ffbc0f` | data/packing/quality | Packing, document boundaries, loss mask skeleton, report scripts. | `src/educode/packing.py`, `src/educode/document_boundaries.py`, `scripts/build_packing_report.py`, `scripts/analyze_token_utilization_v2.py`, `tests/test_sequence_packing_v2.py`, `docs/sequence_packing_v2.md` | py_compile, 2 report scripts, 3 tests, diff check passed. | No for synthetic utility; yes before training integration. | Low | review soon |
| `feature/dataset-quality-dedup-v2` | `81a641f` | data/packing/quality | Exact/near duplicate detection, quality stats, MinHash placeholder. | `src/educode/data_quality.py`, `src/educode/dedup.py`, `scripts/analyze_dataset_quality_v2.py`, `tests/test_data_quality_v2.py`, `tests/test_dedup_v2.py`, `docs/dataset_quality_dedup_v2.md` | py_compile, quality script, 4 tests, diff check passed. | No for tiny fixtures; yes before large corpus scan. | Low | review soon |
| `feature/tokenizer-stats-analyzer` | `1a638a9` | data/packing/quality | Tokenizer stats, frequency, special/unknown token rate, bytes-per-token proxy. | `src/educode/tokenizer_stats.py`, `scripts/analyze_tokenizer_stats.py`, `tests/test_tokenizer_stats.py`, `docs/tokenizer_stats_analyzer.md` | py_compile, analyzer script, 2 tests, diff check passed. | No | Low | review soon |

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

Low-risk branches should be reviewed before branches that alter model internals, optimizer behavior, attention execution, distributed execution, or training memory semantics.

### Low Risk First

1. `docs/llm-systems-survey-roadmap`
2. `feature/tokenizer-stats-analyzer`
3. `feature/training-report-generator`
4. `feature/loss-metric-diagnostics`
5. `feature/model-card-reproducibility`
6. `feature/sequence-packing-v2`
7. `feature/dataset-quality-dedup-v2`
8. `feature/sequence-packing-data-utilization`
9. `feature/dataset-quality-dedup`
10. `feature/inference-kv-cache-harness-v2`

### Medium Risk

- `feature/lora-peft-v2`
- `feature/qlora-quantization-v2`
- `feature/lora-peft-skeleton`
- `feature/quantization-qlora-feasibility`
- `feature/rope-position-encoding-v2`
- `feature/attention-backend-abstraction-v2`

### High Risk / Experimental Only

- `feature/distributed-config-memory-estimator`
- `feature/distributed-launch-feasibility`
- `feature/activation-checkpointing-v2`
- `feature/memory-knobs-activation-checkpointing`
- `feature/muon-experimental-optimizer`
- `feature/moe-routing-skeleton-v2`
- Attention backend branches that modify `src/educode/tiny_model.py`

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

- Multi-GPU distributed run.
- FSDP / ZeRO / TP / SP validation.
- Activation checkpointing profiling.
- LoRA training.
- QLoRA 4-bit load/training.
- Backend profiling.
- FlashAttention install/profile.
- Muon vs AdamW training.
- MoE training/profiling.
- RoPE long-context profiling.
- Real checkpoint inference.
- Reward/preference tuning.

## Do Not Claim Yet

These claims require real review, gated execution, and measured evidence before they can be used:

- Do not claim Muon is better than AdamW.
- Do not claim MoE improves model quality.
- Do not claim QLoRA saves memory.
- Do not claim LoRA effectiveness.
- Do not claim distributed scaling succeeded.
- Do not claim activation checkpointing improves throughput.
- Do not claim FlashAttention accelerates this project.
- Do not claim tokenizer, packing, or dedup utilities improve loss.
- Do not claim seq1024 long training is safe; current evidence supports only short profiling/preflight no-OOM for bounded runs.

## Current Prohibitions

- No Modal.
- No GPU.
- No training.
- No tarball/checkpoint/raw data commit.
- No batch merge.
- No PR without review.
