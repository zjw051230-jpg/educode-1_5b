# MVP-29 Modal A100 Seq1024 SDPA Memory Preflight Run

## Scope

This record documents the imported Modal A100 context length 1024 SDPA memory preflight. It is a memory and throughput preflight, not model-quality training evidence.

## Command

```text
modal run scripts/modal_a100_streaming_runner.py --mode preflight_5gb_10step_seq1024_sdpa_memory
```

## Execution

| Field | Value |
| --- | --- |
| Modal app | completed |
| GPU | A100-40GB |
| mode | `preflight_5gb_10step_seq1024_sdpa_memory` |
| context length | `1024` |
| batch size | `4` |
| grad accum | `4` |
| attention backend | `sdpa` |
| max steps | `10` |
| result package | `/vol/results/mvp29_a100_5gb_10step_seq1024_sdpa_memory_preflight_results.tar.gz` |
| OOM | `false` |
| artifact validation blockers | `0` |

The result package was imported as small JSON/JSONL/Markdown artifacts only. The raw tarball and checkpoint are not committed.

## Cost

The expected cost window was `$0.03-$0.15`. The run was only 10 steps, though Modal startup, clone, prepared-data extraction, and result packaging overhead still apply. Actual billing should be checked in Modal. GPU billing stops after `App completed`; Modal Volume storage cost continues.

## Loss Sanity

| Metric | Value |
| --- | --- |
| first train loss | `9.911758` |
| final train loss | `2.392136` |
| final validation loss | `9.044042` |
| metrics rows | `10` |
| validation rows | `1` |
| validation unique docs | `4` |
| validation prefix-only risk | `false` |

These losses are only sanity checks for a 10-step memory preflight.

## Memory And Throughput

| Metric | Value |
| --- | --- |
| summary tokens/sec | `27151.115060` |
| mean per-step tokens/sec | `40433.276612` |
| average step time | `0.603437s` |
| peak GPU memory allocated | `2.649026 GiB` |
| peak GPU memory reserved | `8.412109 GiB` |
| MFU | unavailable / `null` in metrics |

The first step includes warmup/startup effects and is much slower than the later rows. Later rows settle around roughly `45k` tokens/sec with per-step time around `0.36s`.

## Seq512 Baseline Comparison

| Metric | Seq512 SDPA baseline | Seq1024 memory preflight |
| --- | --- | --- |
| context length | `512` | `1024` |
| batch size | `8` | `4` |
| grad accum | `4` | `4` |
| tokens per optimizer step | `16384` | `16384` |
| average step time | `0.371513s` | `0.603437s` |
| peak allocated memory | `2.645120 GiB` | `2.649026 GiB` |
| peak reserved memory | `8.416016 GiB` | `8.412109 GiB` |

The first seq1024 probe used batch size `4`, keeping tokens per optimizer step equal to the seq512 baseline. It confirmed no OOM under this conservative shape.

## Artifact Paths

Imported artifacts:

```text
experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/results_imported_modal_streaming/
```

Included small files:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`
- `import_validation_summary.json`

Not committed:

- raw result tarball
- checkpoint files
- prepared splits

## Meaning

The run validates that the current A100-40GB SDPA path can complete a bounded seq1024 memory preflight at `batch_size=4`, `grad_accum=4`, with finite losses, memory metrics, and artifact validation blockers `0`.

It does not prove seq1024 quality improvement, does not validate seq1024 batch size `8`, and does not justify a direct seq1024 3000-step run.

## Next Step

Recommended next step: MVP-29.A should analyze the seq1024 memory preflight metrics and compare them against the seq512 SDPA baseline. After that, decide whether to try seq1024 `batch_size=8` or a seq1024 50-step profiling run.
