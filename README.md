# EduCode-1.5B

EduCode-1.5B is a CS336-inspired LLM training systems project built from scratch in PyTorch. The focus is reproducible training infrastructure: tokenizer/data loading, model code, validation guardrails, Modal A100 execution gates, artifact validation, and small systems profiling.

This is not a finished foundation model. The repository is evidence for building and validating the training pipeline, not a claim of production model quality.

## Key Evidence

- **Training trend:** the FineWeb-Edu 5GB 3000-step run improved over the 1000-step run.
- **Validation guardrail:** the 5GB 3000-step run used `validation_unique_doc_count = 15` with `validation_prefix_only_risk = false`.
- **A100 SDPA systems baseline:**
  - seq512, batch 8, 50-step profile: `44100.712407` summary tokens/sec, `0.371513s` average step time.
  - seq1024, batch 4, 50-step profile: no OOM, `41430.475003` summary tokens/sec, `0.395458s` average step time.
  - seq1024 peak memory: `2.649026 GiB` allocated, `8.412109 GiB` reserved.

## What To Know

- Short profiling runs are systems evidence, not model-quality evidence.
- MFU is currently unavailable/null; throughput, step time, and memory are the useful profiling metrics.
- Raw datasets, prepared data, result tarballs, and checkpoints are intentionally not committed.
- GPU/Modal runs require explicit mode-specific approval and cost awareness.

## Details

- Experiment index: `docs/experiment_index.md`
- Experimental branch inventory: `docs/branch_asset_inventory.md`
- 5GB training analysis: `docs/mvp_27_a_5gb_3000step_result_analysis.md`
- seq512 SDPA analysis: `docs/mvp_28_a_sdpa_profile_result_analysis.md`
- seq1024 memory preflight analysis: `docs/mvp_29_a_seq1024_memory_preflight_result_analysis.md`
- seq1024 SDPA profiling analysis: `docs/mvp_30_a_seq1024_sdpa_profile_result_analysis.md`

## Current Next Step

Recommended next planning item:

```text
MVP-31.P seq1024 batch_size=8 memory preflight plan
```

The goal is to decide whether seq1024 can safely use `batch_size=8` before attempting longer training or backend comparisons.
