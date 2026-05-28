# MVP-27.A 5GB 3000-step Result Analysis

## Scope

This analysis reviews the already-imported Modal A100 5GB 3000-step streaming results from MVP-26. It does not run Modal, does not request GPU, does not start training, and does not modify training code.

Analyzed artifacts:

- `experiments/a100/fineweb_edu_5gb_300m_3000step_public16k_execute/results_imported_modal_streaming/summary.json`
- `experiments/a100/fineweb_edu_5gb_300m_3000step_public16k_execute/results_imported_modal_streaming/metrics.jsonl`
- `experiments/a100/fineweb_edu_5gb_300m_3000step_public16k_execute/results_imported_modal_streaming/validation_metrics.jsonl`
- `experiments/a100/fineweb_edu_5gb_300m_3000step_public16k_execute/results_imported_modal_streaming/import_validation_summary.json`
- `experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_streaming/summary.json`
- `docs/mvp_25_a_5gb_1000step_result_analysis.md`
- `docs/mvp_26_modal_a100_5gb_3000step_streaming_run.md`
- `docs/mvp_26_modal_a100_5gb_3000step_execution_receipt.md`

Local analysis script:

```text
scripts/analyze_mvp27_a_5gb_3000step_results.py
```

## Direct Answers

| Question | Answer |
| --- | --- |
| 5GB 3000-step final train loss | `3.029707` |
| 5GB 3000-step final validation loss | `8.341638` |
| Did train loss overall decline? | Yes. It moved from `9.869211` to `3.029707`; first-to-last direction is `down`. |
| Did validation loss improve versus 5GB 1000-step? | Yes. Final validation loss improved from `9.214416` to `8.341638`, a delta of `-0.872778`. |
| Is validation coverage credible enough for this comparison? | Yes for this bounded run. It uses validation-side `shuffle_buffer`, covers `15` unique validation documents, and reports no prefix-only risk. |
| Is `validation_unique_doc_count > 1`? | Yes: `15`. |
| Is `validation_prefix_only_risk=false`? | Yes. |
| Should we directly run 10000-step next? | No. The 3000-step run improves the evidence base, but it is still one bounded run. |

## Script Output Summary

```json
{
  "analysis_status": "passed",
  "blocker_count": 0,
  "metrics_rows": 3000,
  "validation_rows": 10,
  "first_train_loss": 9.869211,
  "last_train_loss": 3.029707,
  "min_train_loss": 1.705493,
  "max_train_loss": 9.869211,
  "first_validation_loss": 9.028253,
  "last_validation_loss": 8.341638,
  "min_validation_loss": 8.230417,
  "max_validation_loss": 9.028253,
  "validation_loss_range": 0.797835,
  "validation_loss_population_stddev": 0.228388,
  "comparison_vs_5gb_1000_final_train_loss_delta": -0.130975,
  "comparison_vs_5gb_1000_final_validation_loss_delta": -0.872778
}
```

## Loss Behavior

### Train Loss

The train loss gives a clear optimization signal:

| Metric | Value |
| --- | --- |
| First train loss | `9.869211` |
| Last train loss | `3.029707` |
| Minimum train loss | `1.705493` |
| Maximum train loss | `9.869211` |
| Direction first-to-last | `down` |

The curve is noisy and the final value is not the minimum, so it should not be described as monotonic. Still, the first-to-last direction is healthy.

### Validation Loss

Validation loss also improves first-to-last:

| Metric | Value |
| --- | --- |
| First validation loss | `9.028253` |
| Last validation loss | `8.341638` |
| Minimum validation loss | `8.230417` |
| Maximum validation loss | `9.028253` |
| Range | `0.797835` |
| Population stddev | `0.228388` |
| Direction first-to-last | `down` |

The final validation loss is not the minimum, but it remains bounded and ends better than it starts.

## Comparison With 5GB 1000-step

| Metric | 5GB 1000-step | 5GB 3000-step | Delta |
| --- | ---: | ---: | ---: |
| Final train loss | `3.160682` | `3.029707` | `-0.130975` |
| Final validation loss | `9.214416` | `8.341638` | `-0.872778` |
| Metrics rows | `1000` | `3000` | `+2000` |
| Tokens seen | `16,384,000` | `49,152,000` | `+32,768,000` |
| Validation sampling | `sequential_prefix` | `shuffle_buffer` | improved |
| Validation unique doc count | `1`-document prefix behavior | `15` | improved |
| Validation prefix-only risk | present by policy | `false` | improved |

The 3000-step run improves in two different ways:

1. Measurement quality is materially better because validation is no longer a single-document sequential prefix.
2. The final train and validation losses are both lower than the 1000-step baseline.

This is stronger evidence than MVP-25.A, where validation representativeness was the main blocker.

## Caveats

- This is still one run on one dataset slice, not proof of general model quality.
- The model is a 300M-class systems run, not the final 1B-3B / 1.5B target.
- Validation uses only `10` validation batches and `40,960` validation tokens.
- The validation document count is now healthy for a bounded run, but still small compared with a full evaluation suite.
- The train loss remains noisy, with local troughs below the final loss.
- No downstream CS/ML/code task evaluation is included.
- Learned positional embeddings and SDPA remain the current baseline; RoPE/FlashAttention/B200 scale work is still future work.

## Recommendation

Do not jump directly to 10000-step.

The best next step is MVP-27.B: choose the next experiment route. The choice should compare a bounded step extension against technical experiments that make the project more complete:

| Candidate | Why it helps |
| --- | --- |
| 5GB 5000-step | Tests whether the corrected validation signal remains stable at a modest longer horizon. |
| 5GB 10000-step | Higher cost and less informative until 5000-step or route selection justifies it. Not the immediate default. |
| AdamW baseline vs Muon | Adds optimizer comparison value beyond simply stacking more steps. |
| Context length `512 -> 1024` | Tests a visible modeling/data-path capability important for code and ML learning tasks. |
| SDPA / FlashAttention profiling | Adds systems depth and throughput evidence before larger scale. |
| B200 300M / 1B scale plan | Prepares the later scale route without prematurely spending on a larger run. |

Recommended near-term decision: enter MVP-27.B for route selection. If the priority is pure training continuity, use a 5GB 5000-step gate before any 10000-step run. If the priority is portfolio depth, pick a technical experiment such as optimizer comparison, context length 1024, or attention profiling.

## Resume Value

This result is valuable for resume storytelling because it shows:

- a real Modal A100-40GB training run, not only local smoke tests
- a 300M-class model trained on a prepared 5GB public corpus slice
- streaming data loading with shuffle-buffer train sampling
- a diagnosed validation flaw that was fixed before spending on a longer run
- measurable improvement from 1000-step to 3000-step under corrected validation coverage
- disciplined artifact boundaries: checkpoints and tarballs were not committed
- cost-gated engineering practice rather than blind scaling

The concise resume framing is: "Built a cost-gated A100 training pipeline for a 300M-class educational code/ML language model, fixed validation coverage from single-document prefix sampling to deterministic shuffle-buffer sampling, and validated a 5GB 3000-step run with lower final train and validation loss than the 1000-step baseline."
