# MVP-26 Modal A100 5GB 3000-step Streaming Run

## Scope

This document records the imported Modal A100 result for `train_5gb_3000` using the 5GB FineWeb-Edu prepared-data package, public 16k tokenizer, 300M-class EduCode model configuration, streaming data loading, shuffle-buffer train sampling, and the MVP-25.C validation-side shuffle-buffer coverage fix.

This import step did not run Modal again, did not request GPU, did not train, did not import checkpoints, and did not stage or commit the raw result tarball.

## Run command

The completed training command was:

```powershell
modal run scripts/modal_a100_streaming_runner.py --mode train_5gb_3000
```

The Modal app completed successfully.

## Source result package

| Field | Value |
| --- | --- |
| Local package | `mvp26_a100_5gb_3000step_public16k_streaming_results.tar.gz` |
| Modal result package | `/vol/results/mvp26_a100_5gb_3000step_public16k_streaming_results.tar.gz` |
| Modal mode | `train_5gb_3000` |
| GPU requested | `A100-40GB` |
| Reported repo commit | `f703e07` |
| Training status | `success` |
| App completed | `true` |

Only approved small result artifacts were extracted into:

```text
experiments/a100/fineweb_edu_5gb_300m_3000step_public16k_execute/results_imported_modal_streaming/
```

Imported files:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`
- `import_validation_summary.json`

## Run metadata

| Field | Value |
| --- | --- |
| Run ID | `20260528_192024_fineweb_edu_5gb_300m_3000step_public16k_execute` |
| Runtime device | `cuda` |
| Runtime dtype | `bf16` |
| GPU | `NVIDIA A100-SXM4-40GB` |
| GPU memory | `39.494 GiB` |
| Python | `3.11.12` |
| Torch | `2.12.0+cu130` |
| CUDA | `13.0` |
| Git commit | `f703e0788879d91851ead933a767fc5ad1f995bf` |
| Start time | `2026-05-28T19:20:24` |
| End time | `2026-05-28T19:37:47` |
| Elapsed seconds | `1024.568388` |
| Status | `success` |

## Metrics summary

| Metric | Value |
| --- | --- |
| First train loss | `9.869211` |
| Final train loss | `3.029707` |
| Final validation loss | `8.341638` |
| Final gradient norm | `0.998806` |
| Metrics rows | `3000` |
| Validation rows | `10` |
| Tokens seen | `49,152,000` |
| Approximate tokens/sec | `47,973.37161` |
| Checkpoint reload match | `true` |
| Post-run blockers | `0` |

All reported train loss, validation loss, and gradient finite checks passed.

## Comparison with 5GB 1000-step

| Item | 5GB 1000-step | 5GB 3000-step |
| --- | --- | --- |
| Max steps | `1000` | `3000` |
| Tokens seen | `16,384,000` | `49,152,000` |
| Final train loss | `3.160682` | `3.029707` |
| Final validation loss | `9.214416` | `8.341638` |
| Validation sampling | `sequential_prefix` | `shuffle_buffer` |
| Validation unique docs | not representative; probe used `1` doc | `15` |
| Validation prefix-only risk | present by policy | `false` |
| Elapsed seconds | `341.633667` | `1024.568388` |

The 3000-step run is about 3x the step count of the 1000-step run and completed with a similar throughput profile.

## Validation coverage significance

MVP-25.C fixed the validation measurement path before this run. The 3000-step result confirms the training run used the corrected validation-side policy:

| Field | Value |
| --- | --- |
| Validation sampling policy | `shuffle_buffer` |
| Validation shuffle seed | `7331` |
| Validation shuffle buffer size | `64` |
| Validation max blocks per document | `8` |
| Validation unique doc count | `15` |
| Validation batches evaluated | `10` |
| Validation tokens evaluated | `40,960` |
| Validation prefix-only risk | `false` |

This makes the 3000-step validation signal more representative than the earlier 5GB 1000-step result. It is still training-systems and measurement evidence, not a model-quality claim.

## Cost note

This was a cost-bearing Modal A100-40GB training run. Based on the measured elapsed seconds and the pre-run estimate, the run appears consistent with the expected `$0.65-$0.90` envelope. GPU billing should stop after `App completed`; Modal Volume storage can continue independently while data remains stored.

## Checkpoint and artifact boundary

The Modal training run produced a checkpoint on the remote worker:

```text
experiments/a100/fineweb_edu_5gb_300m_3000step_public16k_execute/checkpoints/checkpoint_step_3000.pt
```

The checkpoint was not imported and must not be committed. The raw result tarball remains untracked and must not be committed. The imported directory contains only small result and validation artifacts.

## Local validation evidence

Validator:

```text
scripts/validate_mvp26_modal_a100_5gb_3000step_imported_results.py
```

Validation result:

| Field | Value |
| --- | --- |
| Validation status | `passed` |
| Blocker count | `0` |
| Metrics rows actual | `3000` |
| Validation rows actual | `10` |
| Validation unique docs | `15` |
| Validation prefix-only risk | `false` |
| Checkpoint reload match | `true` |
| Post-run artifact validation passed | `true` |

## Next step

Analyze the 5GB 3000-step result before approving any longer run. Do not jump directly to 10000-step without a separate analysis and cost gate.
