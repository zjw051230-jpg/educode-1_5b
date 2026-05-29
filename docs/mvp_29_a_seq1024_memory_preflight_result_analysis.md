# MVP-29.A Seq1024 SDPA Memory Preflight Result Analysis

## Scope

This analysis reads the imported Modal A100 seq1024 10-step SDPA memory preflight artifact. It does not run Modal, does not request GPU, does not start training, and does not implement any attention backend.

## Result

The seq1024 memory preflight succeeded. Modal app completed in MVP-29.RUN, import validation passed in MVP-29.R, and post-run artifact validation reported blocker count `0`.

| Field | Value |
| --- | --- |
| context length | `1024` |
| batch size | `4` |
| grad accum | `4` |
| attention backend | `sdpa` |
| max steps | `10` |
| OOM | `false` |
| metrics rows | `10` |
| validation rows | `1` |
| final train loss | `2.392136` |
| final validation loss | `9.044042` |

This is not quality training evidence. Ten steps are enough to validate the execution shape, no-OOM behavior, finite losses, and metric recording, but not enough to evaluate model quality.

## Throughput

| Metric | Seq1024 value |
| --- | --- |
| summary tokens/sec | `27151.115060` |
| mean step tokens/sec | `40433.276612` |
| average step time | `0.603437s` |

Throughput is lower than the seq512 SDPA baseline. This is expected: each token attends across a longer context, and the short 10-step run is more affected by warmup. The summary throughput includes the slow first step; later rows were closer to the mid-45k tokens/sec range.

## Memory

| Metric | Seq1024 value |
| --- | --- |
| peak allocated memory | `2.649026 GiB` |
| peak reserved memory | `8.412109 GiB` |
| MFU | unavailable / `null` |

The run did not OOM. Peak memory was roughly comparable to the seq512 profile because the seq1024 preflight deliberately reduced batch size from `8` to `4`. That keeps tokens per optimizer step unchanged:

```text
seq512:  8 * 512  * 4 = 16384 tokens
seq1024: 4 * 1024 * 4 = 16384 tokens
```

Attention memory can grow with sequence length squared, but halving the batch size offsets part of that pressure. PyTorch SDPA kernel behavior also matters, so this result should be treated as empirical evidence for this exact shape, not a proof for all seq1024 settings.

## Seq512 Comparison

| Metric | Seq512 SDPA baseline | Seq1024 memory preflight | Delta |
| --- | --- | --- | --- |
| context length | `512` | `1024` | `+512` |
| batch size | `8` | `4` | `-4` |
| summary tokens/sec | `44100.712407` | `27151.115060` | `-16949.597347` |
| average step time | `0.371513s` | `0.603437s` | `+0.231924s` |
| peak allocated memory | `2.645120 GiB` | `2.649026 GiB` | `+0.003906 GiB` |
| peak reserved memory | `8.416016 GiB` | `8.412109 GiB` | `-0.003907 GiB` |

The key systems result is that seq1024 is viable at batch size `4` for a short SDPA memory preflight, with lower throughput but no meaningful memory increase versus the conservative seq512 baseline.

## Loss Caveat

`final_train_loss=2.392136` and `final_validation_loss=9.044042` are only sanity signals. The run is too short to support quality claims or a scaling decision.

## Decision

Seq1024 can be the next profiling direction. It is not yet safe to jump to seq1024 3000-step because:

- only a 10-step memory preflight has passed
- batch size `8` has not been tested at seq1024
- the run does not establish quality improvement
- longer training would spend more before profiling stability is understood

The next best step is:

```text
MVP-30.P seq1024 50-step SDPA profiling plan
```

Rationale: seq1024 batch size `4` already passed no-OOM; a 50-step profile at the same conservative batch size would provide a better throughput/step-time/memory baseline before considering batch size `8` or longer training.

Secondary options:

- seq1024 batch_size=8 memory preflight, if the goal is maximum throughput probing
- naive/manual attention baseline, if the goal is backend comparison
- FlashAttention feasibility audit, if the goal is implementation planning

Do not claim SDPA beats naive or FlashAttention until those paths exist and are measured.
