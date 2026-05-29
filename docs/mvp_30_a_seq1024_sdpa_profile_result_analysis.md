# MVP-30.A Seq1024 SDPA Profile Result Analysis

## Scope

This analysis reads the imported Modal A100 seq1024 50-step SDPA profiling artifact. It does not run Modal, does not request GPU, does not start training, and does not implement a new attention backend.

## Result

The seq1024 50-step SDPA profiling run succeeded. Modal app completed in MVP-30.RUN, import validation passed in MVP-30.R, and post-run artifact validation reported blocker count `0`.

| Field | Value |
| --- | --- |
| context length | `1024` |
| batch size | `4` |
| grad accum | `4` |
| attention backend | `sdpa` |
| max steps | `50` |
| OOM | `false` |
| metrics rows | `50` |
| validation rows | `1` |
| final train loss | `1.450320` |
| final validation loss | `9.930368` |

This is not quality training evidence. Fifty steps are enough to validate the execution shape, no-OOM behavior, finite losses, and stable metric recording, but not enough to evaluate model quality.

## Throughput

| Metric | Seq1024 value |
| --- | --- |
| summary tokens/sec | `41430.475003` |
| mean step tokens/sec | `44774.595547` |
| average step time | `0.395458s` |

The run is a little slower than the seq512 SDPA baseline, which is expected for longer context. The later rows are steadier than the first warmup step. That makes the 50-step profile a better systems baseline than the 10-step preflight.

## Memory

| Metric | Seq1024 value |
| --- | --- |
| peak allocated memory | `2.649026 GiB` |
| peak reserved memory | `8.412109 GiB` |
| MFU | unavailable / `null` |

The run did not OOM. Peak memory stayed essentially unchanged versus seq512 because this seq1024 profile deliberately used `batch_size=4` instead of `8`.

## Seq512 Comparison

| Metric | Seq512 SDPA baseline | Seq1024 profile | Delta |
| --- | --- | --- | --- |
| summary tokens/sec | `44100.712407` | `41430.475003` | `-2670.237404` |
| mean step tokens/sec | `46732.188322` | `44774.595547` | `-1957.592775` |
| average step time | `0.371513s` | `0.395458s` | `+0.023945s` |
| peak allocated memory | `2.645120 GiB` | `2.649026 GiB` | `+0.003906 GiB` |
| peak reserved memory | `8.416016 GiB` | `8.412109 GiB` | `-0.003907 GiB` |

Compared with seq512, seq1024 is slightly slower and slightly more expensive in step time, while memory is effectively flat. That is a good bounded systems result for this exact shape.

## Seq1024 10-step Comparison

| Metric | Seq1024 10-step preflight | Seq1024 50-step profile | Delta |
| --- | --- | --- | --- |
| summary tokens/sec | `27151.115060` | `41430.475003` | `+14279.359943` |
| average step time | `0.603437s` | `0.395458s` | `-0.207979s` |
| peak allocated memory | `2.649026 GiB` | `2.649026 GiB` | `0.000000 GiB` |
| peak reserved memory | `8.412109 GiB` | `8.412109 GiB` | `0.000000 GiB` |

The 50-step profile is much faster than the 10-step preflight because the preflight was dominated by startup and early warmup. By step 50, the loop has settled into a stable cadence.

## Why Throughput Looks Better Than The 10-step Preflight

The short preflight overweights the first slow step and startup overhead. The 50-step profile amortizes those costs, so the summary throughput climbs and the average step time falls. This is normal and exactly why the 50-step run is the better profiling baseline.

## Loss Caveat

`final_train_loss=1.450320` and `final_validation_loss=9.930368` are sanity signals only. They do not prove quality improvement, and they should not be used as long-training evidence.

## Does This Prove Seq1024 Long Training Is Safe?

No. It proves only that this bounded seq1024 shape can complete 50 steps on A100-40GB without OOM and with stable artifact validation. It does not prove that seq1024 3000-step training is safe.

## Next Decision

Do not jump directly to seq1024 3000-step.

Recommended next step:

```text
MVP-31.P seq1024 batch_size=8 memory preflight plan
```

Why this next:

- batch size `8` is still the main unanswered systems question
- it tests whether the memory headroom remains comfortable at the larger batch
- it keeps the investigation in bounded preflight territory

Secondary options:

- naive/manual attention baseline, if the goal is backend comparison
- FlashAttention feasibility audit, if the goal is implementation planning

Do not claim SDPA beats naive attention or FlashAttention until those paths exist and are measured.
