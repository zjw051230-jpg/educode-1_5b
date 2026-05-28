# MVP-28 Modal A100 5GB 50-step SDPA Profile Run

## Scope

This record documents the successful bounded SDPA attention profiling run. It is systems/profiling evidence, not model-quality training evidence.

## Command

```text
modal run scripts/modal_a100_streaming_runner.py --mode profile_5gb_50step_sdpa
```

## Execution

| Field | Value |
| --- | --- |
| Modal app | completed |
| GPU | A100-40GB |
| mode | `profile_5gb_50step_sdpa` |
| attention backend | `sdpa` |
| max steps | `50` |
| repo commit | `091c13c` |
| result package | `/vol/results/mvp28_a100_5gb_50step_sdpa_profile_results.tar.gz` |
| artifact validation blockers | `0` |

The run used Modal Volume prepared 5GB FineWeb-Edu splits. The result package was imported as small JSON/JSONL/Markdown artifacts only. The raw tarball and checkpoint are not committed.

## Cost

The expected cost window was `$0.05-$0.20`. This run is much shorter than the 5GB 3000-step run and completed successfully; actual billing should be checked in Modal. GPU billing stops after `App completed`. Modal Volume storage cost continues.

## Loss Sanity

| Metric | Value |
| --- | --- |
| first train loss | `9.869211` |
| final train loss | `4.328258` |
| final validation loss | `8.897261` |
| metrics rows | `50` |
| validation rows | `1` |
| validation unique docs | `2` |
| validation prefix-only risk | `false` |

These losses are only sanity checks for a 50-step profiling run.

## Profiling Metrics

| Metric | Value |
| --- | --- |
| summary tokens/sec | `44100.712407` |
| mean per-step tokens/sec | `46732.188322` |
| mean step time | `0.371513s` |
| peak GPU memory allocated | `2.645120 GiB` |
| peak GPU memory reserved | `8.416016 GiB` |
| MFU | unavailable / `null` in metrics |

MFU is enabled in config but the current training loop emits `null`, so it remains a caveat rather than a blocker.

## Why This Matters

- The bounded profiling readiness gate was validated by a real A100 run.
- The bounded profile artifact validation gate was validated by a real A100 run.
- The project now has a committed SDPA baseline profiling artifact.
- The result gives a concrete throughput and memory baseline before implementing naive attention or optional FlashAttention paths.

## Artifact Paths

Imported artifacts:

```text
experiments/a100/fineweb_edu_5gb_300m_50step_public16k_sdpa_profile/results_imported_modal_streaming/
```

Included small files:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`

Not committed:

- raw result tarball
- checkpoint files
- prepared splits

## Next Step

Recommended next step: MVP-28.A should analyze SDPA profiling metrics and decide whether to implement a naive attention baseline or prepare an optional FlashAttention path.
