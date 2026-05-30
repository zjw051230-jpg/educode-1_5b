# EduCode-1.5B

A CS336-inspired LLM training systems project built from scratch in PyTorch, with a focus on reproducible training infrastructure, data/validation guardrails, and small-scale A100 systems profiling.

This repository is not a finished foundation model. It is an engineering project that demonstrates the pipeline needed to move from local smoke tests to bounded GPU experiments: config validation, tokenization, streaming data, model execution, training/eval loops, artifact validation, and Modal A100 run import.

## Current Evidence

| Area | Key Result |
| --- | --- |
| Training trend | FineWeb-Edu 5GB 3000-step improved over the 1000-step run |
| Validation credibility | `validation_unique_doc_count = 15`, `validation_prefix_only_risk = false` for the 5GB 3000-step run |
| A100 SDPA baseline | seq512 50-step SDPA profile: `44100.712407` summary tokens/sec, `0.371513s` average step time |
| Seq1024 memory preflight | seq1024 10-step SDPA preflight completed with no OOM at `batch_size=4` |
| Seq1024 SDPA profile | seq1024 50-step SDPA profile completed with no OOM: `41430.475003` summary tokens/sec, `0.395458s` average step time |
| GPU memory | seq1024 50-step profile peak allocated `2.649026 GiB`, peak reserved `8.412109 GiB` |
| Current caveat | MFU is recorded as `null`; throughput, step time, and memory are the usable systems metrics |

## What Is Implemented

- Decoder-only Transformer training path with RMSNorm, SwiGLU, learned position embeddings, and PyTorch SDPA.
- Public 16k BPE tokenizer path for FineWeb-Edu public-corpus experiments.
- Host-RAM-efficient streaming batch iterator with deterministic shuffle-buffer sampling.
- Modal A100 runner modes for bounded prepared-data streaming runs.
- Readiness gates that separate long training execution from bounded profiling/preflight runs.
- Post-run artifact validation for training, SDPA profiling, and seq1024 memory/preflight artifacts.
- Import scripts and analysis docs for small JSON/JSONL/Markdown result artifacts.

## Important Reports

| Topic | Report |
| --- | --- |
| 5GB 3000-step result analysis | `docs/mvp_27_a_5gb_3000step_result_analysis.md` |
| Route selection after 3000-step | `docs/mvp_27_b_next_stage_route_selection.md` |
| Seq512 SDPA profile analysis | `docs/mvp_28_a_sdpa_profile_result_analysis.md` |
| Seq1024 memory preflight analysis | `docs/mvp_29_a_seq1024_memory_preflight_result_analysis.md` |
| Seq1024 SDPA profile analysis | `docs/mvp_30_a_seq1024_sdpa_profile_result_analysis.md` |
| Full experiment index | `docs/experiment_index.md` |

## Quick Local Checks

These commands do not run Modal, do not use GPU, and do not start training:

```powershell
.\.venv\Scripts\python.exe scripts\analyze_mvp30_a_seq1024_sdpa_profile_results.py
.\.venv\Scripts\python.exe scripts\validate_mvp30_modal_a100_seq1024_sdpa_profile_results.py
```

Toy/local demo commands are still available:

```powershell
python scripts/run_resume_demo.py
python scripts/run_50_step_toy_training.py
```

## Guardrails

- Raw datasets, prepared data packages, checkpoints, and result tarballs are not committed.
- Long GPU runs require explicit mode-specific approval and cost awareness.
- Bounded profiling results are systems evidence, not model-quality evidence.
- Do not compare SDPA against naive attention or FlashAttention until those backends exist and are measured.

## Current Recommendation

Next planned step:

```text
MVP-31.P seq1024 batch_size=8 memory preflight plan
```

Rationale: seq1024 at `batch_size=4` is now stable for a 50-step SDPA profile. The next unanswered systems question is whether seq1024 can safely use `batch_size=8` before considering longer training or backend comparisons.
