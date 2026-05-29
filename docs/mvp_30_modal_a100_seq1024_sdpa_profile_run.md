# MVP-30 Modal A100 Seq1024 SDPA Profiling Run

## Scope

This record documents the imported Modal A100 `seq1024` 50-step SDPA profiling run. It is a profiling run, not model-quality training evidence.

## Command

```text
modal run scripts/modal_a100_streaming_runner.py --mode profile_5gb_50step_seq1024_sdpa
```

## Execution

| Field | Value |
| --- | --- |
| Modal app | completed |
| GPU | A100-40GB |
| mode | `profile_5gb_50step_seq1024_sdpa` |
| context length | `1024` |
| batch size | `4` |
| grad accum | `4` |
| attention backend | `sdpa` |
| max steps | `50` |
| result package | `/vol/results/mvp30_a100_5gb_50step_seq1024_sdpa_profile_results.tar.gz` |
| OOM | `false` |
| artifact validation blockers | `0` |

The result package was imported as small JSON/JSONL/Markdown artifacts only. The raw tarball and checkpoint are not committed.

## Cost

The expected cost window was `$0.05-$0.20`. The run stayed in the short bounded profiling band, although Modal startup, clone, prepared-data extraction, and result packaging overhead still apply. GPU billing stops after `App completed`; Modal Volume storage cost continues.

## Loss Sanity

| Metric | Value |
| --- | --- |
| first train loss | `9.911758` |
| final train loss | `1.450320` |
| final validation loss | `9.930368` |
| metrics rows | `50` |
| validation rows | `1` |

These losses are sanity signals only. They should not be treated as model-quality evidence.

## Throughput And Memory

| Metric | Value |
| --- | --- |
| summary tokens/sec | `41430.475003` |
| mean per-step tokens/sec | `44774.595547` |
| average step time | `0.395458s` |
| peak GPU memory allocated | `2.649026 GiB` |
| peak GPU memory reserved | `8.412109 GiB` |
| MFU | unavailable / `null` in metrics |

The later step rows are steadier than the first warmup step. The run lands close to the seq1024 memory preflight memory footprint while improving over that 10-step run’s throughput.

## Seq512 Baseline Comparison

| Metric | Seq512 SDPA baseline | Seq1024 profiling run |
| --- | --- | --- |
| context length | `512` | `1024` |
| batch size | `8` | `4` |
| summary tokens/sec | `44100.712407` | `41430.475003` |
| mean per-step tokens/sec | `46732.188322` | `44774.595547` |
| average step time | `0.371513s` | `0.395458s` |
| peak allocated memory | `2.645120 GiB` | `2.649026 GiB` |
| peak reserved memory | `8.416016 GiB` | `8.412109 GiB` |

Relative to seq512, this seq1024 run is a little slower and uses essentially the same memory, which is exactly the sort of bounded systems signal the project wanted before any longer run.

## Seq1024 10-step Preflight Comparison

| Metric | Seq1024 10-step preflight | Seq1024 50-step profiling run |
| --- | --- | --- |
| summary tokens/sec | `27151.115060` | `41430.475003` |
| mean per-step tokens/sec | `40433.276612` | `44774.595547` |
| average step time | `0.603437s` | `0.395458s` |
| peak allocated memory | `2.649026 GiB` | `2.649026 GiB` |
| peak reserved memory | `8.412109 GiB` | `8.412109 GiB` |

Compared with the 10-step preflight, the 50-step profile is much steadier and much faster on the average-step view, while memory remains flat. That supports seq1024 as a viable bounded profiling shape at `batch_size=4`.

## Artifact Validation

- post-run artifact validation blockers: `0`
- metrics rows: `50`
- validation rows: `1`
- checkpoint imported into git: no

## Imported Artifacts

Imported artifacts:

```text
experiments/a100/fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile/results_imported_modal_streaming/
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

## Meaning

This run validates the current A100-40GB SDPA path as a bounded seq1024 profiling baseline. It gives a clean comparison point for future work without claiming model-quality improvement.

## Next Step

Recommended next step: MVP-30.A should analyze the seq1024 profiling metrics. After that, decide whether to try seq1024 `batch_size=8` memory preflight, a naive/manual attention baseline, or a FlashAttention feasibility audit.
