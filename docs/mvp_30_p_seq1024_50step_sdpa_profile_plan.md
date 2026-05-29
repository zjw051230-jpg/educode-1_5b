# MVP-30.P Seq1024 50-step SDPA Profiling Plan

## Scope

This step plans a bounded seq1024 50-step SDPA profiling run. It does not run Modal, does not request GPU, does not start training, does not add the runner mode, and does not produce new runtime results.

## Why Consider Seq1024 50-step Profiling

MVP-29 proved the conservative seq1024 memory shape can run on Modal A100-40GB:

| Field | Value |
| --- | --- |
| context length | `1024` |
| batch size | `4` |
| grad accum | `4` |
| attention backend | `sdpa` |
| max steps | `10` |
| OOM | `false` |
| summary tokens/sec | `27151.115060` |
| mean step tokens/sec | `40433.276612` |
| average step time | `0.603437s` |
| peak allocated memory | `2.649026 GiB` |
| peak reserved memory | `8.412109 GiB` |

That is enough to justify a longer profiling run at the same conservative shape. It is not enough to justify long training.

## Why Not Direct Seq1024 3000-step

Do not run seq1024 3000-step directly:

- MVP-29 was only a 10-step memory preflight.
- The run does not establish model-quality improvement.
- Longer seq1024 training would spend more before collecting stable profiling evidence.
- Batch size `8` at seq1024 has not been tested.
- The current question is systems behavior, not quality training.

## Why Not Batch Size 8 First

Batch size `8` might improve throughput, but it changes the risk profile. The first seq1024 result used `batch_size=4` to keep optimizer-step tokens equal to the seq512 baseline:

```text
seq512:  8 * 512  * 4 = 16384 tokens
seq1024: 4 * 1024 * 4 = 16384 tokens
```

MVP-30 should extend the known-good seq1024 shape from 10 to 50 steps before changing batch size. A later batch-size-8 memory preflight can be planned if the 50-step profile is stable.

## Recommended Profiling Shape

| Field | Recommendation |
| --- | --- |
| context length | `1024` |
| batch size | `4` |
| grad accum | `4` |
| max steps | `50` |
| eval interval | `50` |
| expected metrics rows | `50` |
| expected validation rows | `1` |
| attention backend | `sdpa` |
| data loading | `streaming` |
| train sampling | `shuffle_buffer` |
| validation sampling | `shuffle_buffer` |
| result package | `/vol/results/mvp30_a100_5gb_50step_seq1024_sdpa_profile_results.tar.gz` |

Use a new config and mode. Do not reuse the seq512 50-step config because the run name, output directory, context length, batch size, profile mode, and result package must all be explicit.

## Profiling Goals

The 50-step run should measure:

- tokens/sec
- step time
- peak allocated GPU memory
- peak reserved GPU memory
- finite train loss as a sanity signal
- finite validation loss if validation runs
- artifact validation behavior
- reproducibility of result package contents

This remains systems profiling, not quality training.

## Seq512 Comparison Target

The seq512 50-step SDPA baseline:

| Metric | Seq512 baseline |
| --- | --- |
| context length | `512` |
| batch size | `8` |
| grad accum | `4` |
| summary tokens/sec | `44100.712407` |
| mean step tokens/sec | `46732.188322` |
| average step time | `0.371513s` |
| peak allocated memory | `2.645120 GiB` |
| peak reserved memory | `8.416016 GiB` |

MVP-30 should compare seq1024 batch-size-4 profiling against these values without claiming SDPA beats naive attention or FlashAttention.

## Cost Boundary

This planning step costs `$0`.

The next real A100 run should have low cost and be comparable to MVP-28 50-step SDPA profiling, though startup, clone, prepared-data extraction, and packaging overhead can dominate. It should be much cheaper than any 3000-step training run.

## Success Criteria

Future MVP-30 execution succeeds if:

- Modal app completed.
- A100-40GB was requested.
- `context_length=1024`.
- `batch_size=4`.
- `grad_accum=4`.
- `attention_backend=sdpa`.
- `metrics_rows=50`.
- `validation_rows=1`, derived from `eval_interval=50`.
- no OOM.
- losses are finite.
- memory and throughput fields are recorded.
- post-run artifact validation blocker count is `0`.
- raw tarball and checkpoint are not committed to git.

## Stop Conditions

Stop and report if:

- CUDA OOM occurs.
- loss becomes non-finite.
- readiness rejects the config.
- artifact validation reports blockers.
- the run accidentally targets batch size `8`, 3000/5000/10000 steps, or a non-SDPA backend.
- the result package includes checkpoint weights for git import.

## MVP-30.I Implementation Checklist

MVP-30.I should add:

- `configs/a100/fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile.json`
- Modal runner mode such as `profile_5gb_50step_seq1024_sdpa`
- readiness gate support for explicit `bounded_seq1024_sdpa_profile`
- artifact validator support for 50 metrics rows and 1 validation row
- local validator proving the good config passes and bad configs are rejected
- documentation with the next-run command and cost boundary

Do not execute the new mode during MVP-30.I.
