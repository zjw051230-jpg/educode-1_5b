# Project Asset Summary

EduCode-1.5B is a from-scratch small LLM training-systems project. It has completed A100 300M-class training evidence, a streaming data pipeline, validation coverage fixes, SDPA profiling, seq1024 memory/profiling checks, and a broad set of modern LLM engineering branch assets for later review.

This document summarizes what is real evidence today, what branch assets exist, which branches overlap, and how to review the existing technical inventory without adding more broad directions.

## Real Evidence

The strongest evidence is from executed and imported runs, not from experimental feature branches.

| Evidence | Current Result | Boundary |
| --- | --- | --- |
| FineWeb-Edu 5GB 3000-step A100 training | `final_train_loss=3.029707`, `final_validation_loss=8.341638` | Training-systems and trend evidence, not a finished model-quality claim. |
| Validation guardrail | `validation_unique_doc_count=15`, `validation_prefix_only_risk=false` | Stronger validation representativeness than earlier prefix-only stages. |
| Artifact validation | post-run `blocker_count=0` on the key imported A100 stages | Means imported small artifacts are structurally usable; it does not validate checkpoints for release. |
| seq512 SDPA 50-step profile | `44100.712407` summary tokens/sec, `46732.188322` mean step tokens/sec, `0.371513s` average step time | Systems baseline only. |
| seq512 SDPA memory | `2.645120 GiB` allocated, `8.416016 GiB` reserved | Baseline for bounded A100-40GB memory planning. |
| seq1024 10-step SDPA memory preflight | no OOM, `27151.115060` summary tokens/sec, `0.603437s` average step time | Short preflight only, not long-training safety. |
| seq1024 50-step SDPA profile | no OOM, `41430.475003` summary tokens/sec, `44774.595547` mean step tokens/sec, `0.395458s` average step time | Best current seq1024 SDPA systems profile. |
| seq1024 SDPA memory | `2.649026 GiB` allocated, `8.412109 GiB` reserved | Comparable to seq512 because batch size was reduced from `8` to `4`. |

## Asset Categories

| Category | Main Assets |
| --- | --- |
| docs / roadmap | `docs/notebooklm-tech-synthesis`, `docs/llm-systems-survey-roadmap`, `feature/experiment-planner` |
| safety / artifact hygiene | `feature/checkpoint-artifact-hygiene` already merged into main; `feature/safety-filter-skeleton` remains separate |
| reporting / diagnostics | `feature/cli-experiment-manager`, `feature/run-registry-database`, `feature/auto-report-packager`, `feature/training-report-generator`, `feature/loss-metric-diagnostics`, `feature/model-card-reproducibility`, `feature/profiling-matrix-planner` |
| eval / inference | `feature/eval-benchmark-harness`, `feature/inference-kv-cache-harness-v2`, `feature/inference-eval-harness` |
| attention | `feature/attention-backend-abstraction-v2`, `feature/flashattention-feasibility`, older attention prep branches |
| optimizer | `feature/muon-experimental-optimizer`, `feature/optimizer-registry-muon` |
| MoE | `feature/moe-routing-skeleton-v2`, `feature/moe-routing-prep` |
| RoPE / long context | `feature/rope-position-encoding-v2`, `feature/rope-position-prep` |
| LoRA / QLoRA | `feature/lora-peft-v2`, `feature/lora-peft-skeleton`, `feature/qlora-quantization-v2`, `feature/quantization-qlora-feasibility` |
| distributed / memory | `feature/distributed-config-memory-estimator`, `feature/distributed-launch-feasibility`, `feature/activation-checkpointing-v2`, `feature/memory-knobs-activation-checkpointing` |
| data / tokenizer / packing | `feature/sequence-packing-v2`, `feature/dataset-quality-dedup-v2`, `feature/tokenizer-stats-analyzer`, `feature/tokenizer-training-feasibility`, older v1 utility branches |
| serving / RAG / safety / distillation | `feature/serving-api-skeleton`, `feature/rag-retrieval-skeleton`, `feature/safety-filter-skeleton`, `feature/model-compression-distillation` |

## Overlap And Deduplication

| Topic | Older Branch | Newer Branch | Recommended Canonical Branch | Reason | Action |
| --- | --- | --- | --- | --- | --- |
| LoRA / PEFT | `feature/lora-peft-skeleton` | `feature/lora-peft-v2` | `feature/lora-peft-v2` | v2 adds adapter state, merge/unmerge guard, and trainable report. | Supersede v1 after review. |
| Quantization / QLoRA | `feature/quantization-qlora-feasibility` | `feature/qlora-quantization-v2` | `feature/qlora-quantization-v2` | v2 adds CUDA/bitsandbytes guard plus QLoRA config path. | Supersede v1 after review. |
| Sequence packing | `feature/sequence-packing-data-utilization` | `feature/sequence-packing-v2` | `feature/sequence-packing-v2` | v2 adds document boundaries, loss mask, and report scripts. | Keep v1 as reference until v2 review completes. |
| Dataset quality / dedup | `feature/dataset-quality-dedup` | `feature/dataset-quality-dedup-v2` | `feature/dataset-quality-dedup-v2` | v2 separates exact/near dedup and quality stats. | Supersede v1 after review. |
| Activation checkpointing | `feature/memory-knobs-activation-checkpointing` | `feature/activation-checkpointing-v2` | `feature/activation-checkpointing-v2` | v2 has narrower activation-checkpointing config/wrapper and CPU synthetic backward. | Keep older branch experimental. |
| Distributed planning | `feature/distributed-config-memory-estimator` | `feature/distributed-launch-feasibility` | Both, but separate purposes | One estimates config/memory; the other builds launch strings. | Keep separate, do not merge together blindly. |
| Muon optimizer | `feature/optimizer-registry-muon` | `feature/muon-experimental-optimizer` | `feature/muon-experimental-optimizer` | Newer branch has a guarded Muon module and experimental framing. | Supersede registry-only branch after review. |
| Attention backend | `feature/attention-backend-abstraction`, `feature/attention-backend-prep` | `feature/attention-backend-abstraction-v2` | `feature/attention-backend-abstraction-v2` plus `feature/flashattention-feasibility` | v2 adds GQA utilities and clearer backend abstraction; FlashAttention remains feasibility-only. | Keep older branches experimental. |
| Inference / eval | `feature/inference-eval-harness` | `feature/inference-kv-cache-harness-v2` | `feature/inference-kv-cache-harness-v2` plus `feature/eval-benchmark-harness` | KV-cache v2 is broader for inference; eval benchmark is a separate local benchmark harness. | Supersede earlier inference-eval branch after review. |
| MoE | `feature/moe-routing-prep` | `feature/moe-routing-skeleton-v2` | `feature/moe-routing-skeleton-v2` | v2 adds routing module, MoE layer skeleton, and auxiliary losses. | Keep prep branch experimental. |
| RoPE | `feature/rope-position-prep` | `feature/rope-position-encoding-v2` | `feature/rope-position-encoding-v2` | v2 adds RoPE helpers, cache tests, and passkey fixture. | Keep prep branch experimental. |

Do not delete branches now. Deletion should wait until the canonical branch has been reviewed, any missing file or idea has been copied forward deliberately, and the user approves branch cleanup.

## Canonical Branch Recommendations

| Direction | Recommended Branches |
| --- | --- |
| Roadmap / narrative | `docs/llm-systems-survey-roadmap`, `docs/notebooklm-tech-synthesis` |
| Local reporting / inventory | `feature/cli-experiment-manager`, `feature/run-registry-database`, `feature/auto-report-packager`, `feature/training-report-generator` |
| Diagnostics / reproducibility | `feature/loss-metric-diagnostics`, `feature/model-card-reproducibility`, `feature/tokenizer-stats-analyzer` |
| Eval / inference | `feature/eval-benchmark-harness`, `feature/inference-kv-cache-harness-v2` |
| Data / packing / quality | `feature/sequence-packing-v2`, `feature/dataset-quality-dedup-v2`, `feature/tokenizer-training-feasibility` |
| PEFT / quantization | `feature/lora-peft-v2`, `feature/qlora-quantization-v2` |
| Memory / distributed | `feature/activation-checkpointing-v2`, `feature/distributed-config-memory-estimator`, `feature/distributed-launch-feasibility` |
| Attention / long context | `feature/attention-backend-abstraction-v2`, `feature/flashattention-feasibility`, `feature/rope-position-encoding-v2` |
| Optimizer / MoE | `feature/muon-experimental-optimizer`, `feature/moe-routing-skeleton-v2` |
| RAG / serving / safety / distillation | `feature/rag-retrieval-skeleton`, `feature/serving-api-skeleton`, `feature/safety-filter-skeleton`, `feature/model-compression-distillation` |

## Do Not Merge Soon

These branches should remain unmerged until they get focused review, regression coverage, and where needed explicit GPU/Modal confirmation:

- `feature/attention-backend-abstraction-v2`: modifies model attention path and `tiny_model.py`.
- `feature/attention-backend-abstraction` and `feature/attention-backend-prep`: older overlapping attention branches with stale inventory/history noise.
- `feature/muon-experimental-optimizer`: changes optimizer dynamics and needs real AdamW comparison before claims.
- `feature/moe-routing-skeleton-v2`: changes model architecture and needs deeper correctness, loss, and routing review.
- `feature/rope-position-encoding-v2`: affects long-context position semantics and needs profiling/inference gates.
- `feature/activation-checkpointing-v2`: touches training memory semantics and needs profiling evidence before use.
- `feature/distributed-config-memory-estimator` and `feature/distributed-launch-feasibility`: require multi-GPU validation before practical claims.
- `feature/model-compression-distillation`: requires teacher/student checkpoint policy and real run gates.

## Low-Risk Review First

Review and polish these before medium/high-risk model-internal branches:

1. `docs/llm-systems-survey-roadmap`
2. `feature/cli-experiment-manager`
3. `feature/run-registry-database`
4. `feature/auto-report-packager`
5. `feature/safety-filter-skeleton`
6. `feature/tokenizer-stats-analyzer`
7. `feature/training-report-generator`
8. `feature/loss-metric-diagnostics`
9. `feature/model-card-reproducibility`

## Three-Phase Plan

### Phase 1: Low-Risk Tooling Polish

Review docs/reporting/diagnostics/safety-filter branches. Merge sparingly, one at a time, only after confirming they do not alter training, model internals, raw data, checkpoints, or Modal execution.

### Phase 2: Medium-Risk Data And Inference Review

Review SFT data schema, RAG retrieval, tokenizer feasibility, serving API, LoRA/QLoRA, and inference harnesses. These should remain local/synthetic until a real checkpoint, corpus, or GPU gate is explicitly approved.

### Phase 3: High-Risk Systems Branch Audits

Review attention backend, FlashAttention feasibility, RoPE, Muon, MoE, distributed launch, and activation checkpointing separately. Each needs targeted regression tests and, where applicable, a paid GPU/Modal gate before claims.

## Claims Boundary

Do not claim:

- Muon is better than AdamW.
- MoE improves quality.
- QLoRA saves memory.
- Distributed scaling succeeded.
- FlashAttention accelerates this project.
- seq1024 long training is safe.
- RAG improves answer quality.
- The safety filter is sufficient for safety.
- Distillation is effective.
- The serving API is production-ready or fast.
- Synthetic eval benchmark results represent real checkpoint capability.

The current defensible story is narrower and stronger: the project has built and validated a reproducible training pipeline, run bounded A100 training/profiling, imported validated artifacts, and prepared a large branch inventory for future focused review.
