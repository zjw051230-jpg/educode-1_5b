# MVP-27.B Next Stage Route Selection

## Scope

This document selects the next stage after the successful Modal A100 5GB 3000-step run and MVP-27.A analysis. It does not run Modal, does not request GPU, does not start training, and does not implement Muon, FlashAttention, or any new training mode.

## Current Stage

EduCode-1.5B has moved beyond smoke tests into cost-gated A100 training-system evidence:

- 5GB prepared FineWeb-Edu public corpus path exists.
- Modal A100 prepared-data streaming runs are validated.
- 5GB 3000-step completed on A100-40GB.
- Final train loss improved from `3.160682` to `3.029707` versus 5GB 1000-step.
- Final validation loss improved from `9.214416` to `8.341638`.
- Validation coverage is now credible for a bounded run: `validation_unique_doc_count=15`, `validation_prefix_only_risk=false`.

This is a good point to broaden the project from "longer run" evidence into systems and modeling experiments.

## Why Not Direct 10000-step

Do not jump directly to 10000-step.

Reasons:

- 3000-step is one successful bounded run, not a full scaling law.
- More steps would mainly spend GPU time without adding a new technical dimension.
- Validation uses only `10` validation batches and `40,960` tokens, even though coverage is now much better.
- Current baseline still uses context length `512`, learned position embeddings, and SDPA only.
- Resume value improves more from systems/profiling/context/optimizer evidence than from immediately stacking steps.
- A 10000-step run should come after route selection, profiling, and a separate cost gate.

## Candidate Comparison

| Route | Technical value | Resume value | Risk | Estimated cost | Modal/GPU needed | New code needed | Depends on 5GB 3000-step | Assessment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. 5GB 5000-step continuation | Medium: checks longer horizon stability | Medium: direct training progress | Low-medium | Medium; likely around another bounded A100 run | Yes | Runner/config may be needed | Yes | Good later continuity step, but less new technical substance. |
| B. AdamW vs Muon optimizer experiment | High: optimizer comparison and implementation | High: strong technical talking point | Medium-high | Low before training; later GPU cost if scaled | Not for local implementation, yes for real comparison run | Yes | Not strictly | Valuable, but should start with implementation and tiny/local validation, not a large run. |
| C. context length `512 -> 1024` | High: memory, throughput, and data path stress | High: realistic LLM training constraint | Medium | Medium; preflight first, GPU later | Eventually yes | Mostly config/preflight, maybe memory tooling | Yes | Strong MVP-29 after attention profiling establishes baseline. |
| D. SDPA / FlashAttention profiling | Very high: attention backend, speed, memory, tokens/sec | Very high: CS336/systems-friendly evidence | Medium | Low-to-medium if bounded to profiling/preflight | Likely yes for meaningful GPU profiling | Yes, but bounded | Yes | Best next step: adds systems depth without committing to long training. |
| E. B200 300M/1B scale plan | High for final roadmap | Medium-high | High if executed too soon | Planning low, execution high | Not for planning; yes for execution | Not initially | Yes | Useful later, but premature before A100 profiling and context baselines. |

## Static Decision Script

Decision helper:

```text
scripts/analyze_mvp27_b_next_stage_options.py
```

Key output:

```json
{
  "analysis_status": "passed",
  "recommended_next_mvp": "MVP-28: SDPA / FlashAttention profiling plan + preflight",
  "recommended_mvp_29": "MVP-29: context length 512 -> 1024 memory/preflight",
  "recommended_mvp_30": "MVP-30: choose between 5GB 5000-step continuation and AdamW vs Muon",
  "direct_10000step_recommended": false,
  "next_step_requires_gpu": true,
  "next_step_estimated_cost_category": "low-to-medium; profiling/preflight should be bounded and cheaper than long training"
}
```

Ranked options:

| Rank | Route | Reason |
| --- | --- | --- |
| 1 | D. SDPA / FlashAttention profiling | Highest systems/resume value and can be bounded before long training. |
| 2 | C. context length `512 -> 1024` | Natural follow-up once baseline attention profiling exists. |
| 3 | B. AdamW vs Muon | Strong technical point, but needs careful implementation and local validation. |
| 4 | A. 5GB 5000-step continuation | Useful training continuity, but lower novelty. |
| 5 | E. B200 scale plan | Important roadmap item, but premature to execute. |

## Recommended Route

### MVP-28

Recommended: SDPA / FlashAttention profiling plan + preflight.

Goal:

- inspect current PyTorch/CUDA attention backend support
- define profiling metrics: tokens/sec, memory allocated/reserved, elapsed step time
- create a bounded profiling plan before any long training
- keep the first implementation/run small and explicitly cost-gated

Why this first:

- It adds a CS336-style systems layer.
- It helps explain why future context-length or B200 work is safe.
- It can be done with much less cost than another long training run.
- It improves the project story beyond "we ran more steps."

### MVP-29

Recommended: context length `512 -> 1024` memory/preflight.

Goal:

- estimate memory and throughput change from doubling context length
- run local/static memory inspection first
- prepare a small GPU preflight only after MVP-28 profiling tells us what backend to use

Why second:

- Context length is a visible LLM training constraint.
- It directly supports CS/ML/code learning use cases.
- It should be informed by attention backend profiling.

### MVP-30

Recommended: choose between 5GB 5000-step continuation and AdamW vs Muon.

Decision rule:

- If MVP-28/29 show systems headroom and the project needs more training continuity, plan 5GB 5000-step.
- If the project needs stronger technical breadth, start AdamW vs Muon with implementation, unit tests, tiny/local validation, and only then a small GPU comparison.

Do not default to 10000-step at MVP-30 without another explicit analysis and cost gate.

## Resume Value

The selected path improves the story:

- MVP-26/MVP-27.A show real A100 training and measured improvement.
- MVP-28 adds performance engineering and attention backend profiling.
- MVP-29 adds memory/context-length scaling evidence.
- MVP-30 can then add either bounded training continuity or optimizer research depth.

This is stronger than a linear "more steps" narrative because it shows debugging, measurement, cost control, systems thinking, and experiment design.
