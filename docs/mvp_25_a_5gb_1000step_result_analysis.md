# MVP-25.A 5GB 1000-step Result Analysis

## Scope

This analysis reviews the already-imported Modal A100 5GB 1000-step streaming results from MVP-24. It does not run Modal, does not enter GPU hosts, does not run training, does not train tokenizer/model, and does not modify training code.

Analyzed artifacts:

- `experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_streaming/summary.json`
- `experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_streaming/summary.md`
- `experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_streaming/metrics.jsonl`
- `experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_streaming/validation_metrics.jsonl`
- `experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_streaming/run_config.json`
- `experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_streaming/run_metadata.json`
- `experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_streaming/post_run_artifact_validation_summary.json`
- `docs/mvp_24_modal_a100_5gb_1000step_streaming_run.md`
- `docs/mvp_24_modal_a100_5gb_1000step_execution_receipt.md`

Local analysis script:

```text
scripts/analyze_mvp25_a_5gb_1000step_results.py
```

## Direct answers

| Question | Answer |
| --- | --- |
| Final train loss | `3.160682` in `summary.json`; raw last metric `3.1606817841529846` |
| Final validation loss | `9.214416` in `summary.json`; raw last validation metric `9.214415550231934` |
| Does train loss overall decline? | Yes. It moves from `9.869211196899414` at step 1 to `3.1606817841529846` at step 1000. The curve is noisy, and the minimum train loss is lower at `2.0369462072849274`, but the first-to-last direction is clearly down. |
| Is validation loss stable? | Bounded but not clearly improving. It ranges from `8.753873825073242` to `9.705306053161621`, with population stddev `0.2625032980239115`; final validation loss is higher than the first validation loss. |
| Does `metrics.jsonl` have 1000 rows? | Yes: `1000` rows, matching `summary.metrics_rows`. |
| Does `validation_metrics.jsonl` have 10 rows? | Yes: `10` rows, matching `summary.validation_rows`. |
| Is shuffle buffer / streaming config recorded clearly? | Yes. `data_loading_mode=streaming`, `sampling_policy=shuffle_buffer`, `train_sampling_policy=shuffle_buffer`, `shuffle_seed=1337`, `shuffle_buffer_size=1024`, and `bounded_prefix_batches_only=false` are recorded in summary/config metadata. |
| Does this run still have prefix-only risk? | Train path: mostly no, because train sampling is `shuffle_buffer` and `bounded_prefix_batches_only=false`. Validation path: yes, representativeness remains weak because validation uses `sequential_prefix` and the probe reports only `1` validation document used for `10` validation batches. |

## Script output summary

The local analysis script passed:

```json
{
  "analysis_status": "passed",
  "train_metrics_row_count": 1000,
  "validation_row_count": 10,
  "first_train_loss": 9.869211196899414,
  "last_train_loss": 3.1606817841529846,
  "first_validation_loss": 9.034560203552246,
  "last_validation_loss": 9.214415550231934,
  "min_train_loss": 2.0369462072849274,
  "min_validation_loss": 8.753873825073242,
  "max_validation_loss": 9.705306053161621,
  "validation_loss_range": 0.9514322280883789,
  "validation_loss_population_stddev": 0.2625032980239115,
  "train_loss_direction_first_to_last": "down",
  "validation_loss_direction_first_to_last": "up",
  "sampling_policy": "shuffle_buffer",
  "train_sampling_policy": "shuffle_buffer",
  "val_sampling_policy": "sequential_prefix",
  "shuffle_seed": 1337,
  "shuffle_buffer_size": 1024,
  "bounded_prefix_batches_only": false
}
```

## Loss behavior

### Train loss

The training loss shows the expected optimization signal for a bounded systems run:

- Step 1 train loss: `9.869211196899414`
- Step 1000 train loss: `3.1606817841529846`
- Minimum train loss: `2.0369462072849274`

This is a strong first-to-last decrease. However, the final loss is not the minimum loss, so the run should be described as noisy but directionally descending rather than monotonically decreasing.

### Validation loss

Validation loss does not provide a clean quality-improvement signal:

- Step 100 validation loss: `9.034560203552246`
- Step 1000 validation loss: `9.214415550231934`
- Minimum validation loss: `8.753873825073242`
- Maximum validation loss: `9.705306053161621`
- Range: `0.9514322280883789`
- Population stddev: `0.2625032980239115`

The values stay finite and bounded, with no runaway divergence, but they fluctuate around a high-loss band. The final validation loss is higher than the first validation checkpoint, so this run should not be used as evidence of validation-quality improvement.

## Streaming and sampling assessment

The 5GB run fixes the largest interpretability issue from the earlier 2GB Modal runs on the train side:

- `data_loading_mode=streaming`
- `train_sampling_policy=shuffle_buffer`
- `sampling_policy=shuffle_buffer`
- `shuffle_seed=1337`
- `shuffle_buffer_size=1024`
- `bounded_prefix_batches_only=false`
- train probe reached `max_shuffle_buffer_occupancy=1024`
- train probe saw `1054` records and used `1054` documents

This means the training path is no longer simply reading a sequential JSONL prefix for this run. The train-side prefix-only risk is materially reduced.

The validation path remains intentionally sequential:

- `val_sampling_policy=sequential_prefix`
- `val_data_probe.records_seen=1`
- `val_data_probe.docs_used=1`
- `val_data_probe.used_batches=10`

That is acceptable for a bounded artifact-validation run, but it is too narrow for making model-quality claims. The validation metric is better interpreted as a consistency/health check than as representative held-out quality.

## Comparison with 2GB 1000-step and 2GB 3000-step runs

| Run | Train sampling | Scheduler metadata | Final train loss | Final val loss | Train docs used | Validation rows | Notes |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 2GB 1000-step | prefix-style streaming metadata; `bounded_prefix_batches_only=true` | `scheduler_policy=not_applied` | `3.008913` | `9.012106` | `39` | `10` | Lower final train/val loss than 5GB 1000-step, but weaker sampling metadata and prefix-only caveat. |
| 2GB 3000-step | prefix-style streaming metadata; `bounded_prefix_batches_only=true` | `scheduler_policy=not_applied` | `3.156151` | `9.043165` | `115` | `10` | Longer systems run passed, but still has prefix-only train sampling caveat. |
| 5GB 1000-step | `shuffle_buffer`, seed `1337`, size `1024`; `bounded_prefix_batches_only=false` | `scheduler_policy=constant`, `learning_rate_mode=constant` | `3.160682` | `9.214416` | `1054` | `10` | Better train sampling and metadata clarity, but validation loss is not improved and validation set remains too narrow. |

Improvements in 5GB 1000-step:

1. Train-side sampling is much better documented and less prefix-biased.
2. Scheduler semantics are explicit: fixed LR is recorded as `constant`, not an accidental `not_applied` caveat.
3. The train probe covers far more documents than the earlier 2GB imported runs (`1054` vs `39`/`115`).
4. Throughput remains comparable or slightly better at about `47957.8` tokens/sec.
5. Artifact validation still passes: finite losses, finite gradients, checkpoint reload match, and matching JSONL row counts.

Problems or caveats:

1. Final validation loss is worse than both 2GB imported Modal runs.
2. Final train loss is worse than 2GB 1000-step and roughly similar to 2GB 3000-step.
3. Validation is still based on a very small sequential prefix, so validation loss is not representative enough for scale decisions.
4. The 1000-step 5GB run is primarily systems/scaling evidence, not model-quality evidence.

## Blockers

No artifact-validation blocker was found:

- required files exist
- `metrics.jsonl` row count is `1000`
- `validation_metrics.jsonl` row count is `10`
- post-run artifact validation status is `success`
- post-run blocker count is `0`
- checkpoint reload match is `true`

Analysis blocker for next training decision:

- validation representativeness is weak because validation uses `sequential_prefix` and only `1` validation document is reported by the probe.

This is not a blocker for closing MVP-25.A, but it is a blocker for claiming model-quality improvement or jumping directly to a much longer run.

## Recommendation

Do not jump directly to 5GB 10000-step.

Recommended next step: fix or strengthen the validation path before spending on longer 5GB training. The minimum useful next work is to make validation coverage more representative and explicitly reported, for example by preparing or sampling a larger validation slice and ensuring the validation probe uses more than one document.

After that validation fix, the next training run should be 5GB 3000-step, not 5GB 10000-step. A 5GB 3000-step run is the right incremental scaling step because it tests whether shuffle-buffer train sampling plus stronger validation coverage produces a stable trend over more tokens. A 5GB 10000-step run should wait until 5GB 3000-step validates both artifact health and validation behavior.
