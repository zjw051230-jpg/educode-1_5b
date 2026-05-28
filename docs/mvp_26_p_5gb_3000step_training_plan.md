# MVP-26.P 5GB 3000-step Modal Training Plan and Cost Gate

## Scope

This plan prepares the next bounded 5GB Modal training decision after MVP-25.C. It does not run Modal, does not request GPU, does not train, does not run backward, does not call `optimizer.step()`, and does not save a checkpoint.

## Why this can now be considered

MVP-25.A found that the 5GB 1000-step training-side signal improved, but validation was too narrow because it used a sequential prefix and covered only one validation document. MVP-25.B fixed validation sampling locally. MVP-25.C then verified the fix against the real 5GB validation split with a CPU-only Modal preflight.

MVP-25.C result:

| Field | Value |
| --- | --- |
| `preflight_status` | `passed` |
| `val_sampling_policy` | `shuffle_buffer` |
| `val_shuffle_seed` | `7331` |
| `val_shuffle_buffer_size` | `64` |
| `validation_max_blocks_per_document` | `8` |
| `validation_unique_doc_count` | `15` |
| `validation_batches_evaluated` | `10` |
| `validation_tokens_evaluated` | `40960` |
| `validation_prefix_only_risk` | `false` |
| `blocker_count` | `0` |

This removes the MVP-25.A blocker that validation coverage was too narrow for the next bounded 5GB run. It does not prove model quality improved; it only proves the validation measurement path is now broad enough for the next training decision.

## Current execution readiness

The 5GB 3000-step config exists:

```text
configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json
```

The Modal runner currently does not define a `train_5gb_3000` mode. Do not run a 3000-step Modal job until a follow-up runner-preparation step adds and validates that mode.

Intended future command after the runner mode exists:

```powershell
modal run scripts/modal_a100_streaming_runner.py --mode train_5gb_3000
```

## Config check

| Setting | Value |
| --- | --- |
| data loading | `streaming` |
| train sampling policy | `shuffle_buffer` |
| train shuffle seed | `1337` |
| train shuffle buffer size | `1024` |
| validation sampling policy | `shuffle_buffer` |
| validation shuffle seed | `7331` |
| validation shuffle buffer size | `64` |
| validation max blocks per document | `8` |
| max steps | `3000` |
| batch size | `8` |
| gradient accumulation steps | `4` |
| context / sequence length | `512` |
| eval interval | `300` |
| expected validation rows | `10` |
| expected train tokens seen | `49,152,000` |
| expected validation tokens evaluated | `40,960` |
| scheduler policy | `constant` |
| output dir | `experiments/a100/fineweb_edu_5gb_300m_3000step_public16k_execute` |

Token calculation:

```text
3000 steps * 8 batch_size * 512 sequence_length * 4 gradient_accumulation_steps = 49,152,000 train tokens
10 validation batches * 8 batch_size * 512 sequence_length = 40,960 validation tokens
```

## Difference from the 5GB 1000-step run

| Item | 5GB 1000-step | Planned 5GB 3000-step |
| --- | --- | --- |
| max steps | `1000` | `3000` |
| eval interval | `100` | `300` |
| expected validation rows | `10` | `10` |
| expected train tokens | `16,384,000` | `49,152,000` |
| checkpoint interval | `1000` | `3000` |
| train sampling | `shuffle_buffer`, seed `1337`, size `1024` | same |
| validation sampling | old run used `sequential_prefix` | fixed `shuffle_buffer`, seed `7331`, size `64`, max 8 blocks/doc |
| interpretation | systems/scaling evidence, weak validation representativeness | bounded longer-run evidence with stronger validation measurement |

## Validation coverage path in training

The training script reads `validation_sampling` through `build_validation_sampling_settings(...)` and passes the settings into `create_streaming_batch_iterator(...)` for the validation iterator. The run summary records:

- `val_sampling_policy`
- `val_shuffle_seed`
- `val_shuffle_buffer_size`
- `validation_max_blocks_per_document`
- `validation_unique_doc_count`
- `validation_batches_evaluated`
- `validation_tokens_evaluated`
- `validation_prefix_only_risk`
- `val_data_probe`

The 3000-step config already contains the validated MVP-25.C settings.

## Modal runner gate

Current runner status:

- `train_5gb_1000`: present
- `preflight_5gb_validation_coverage`: present and passed
- `train_5gb_3000`: not present

Required next preparation before training:

1. Add `train_5gb_3000` to `MODE_SPECS`.
2. Point it at `configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json`.
3. Use `/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz`.
4. Write small result package to a distinct path such as:

```text
/vol/results/mvp26_a100_5gb_3000step_public16k_streaming_results.tar.gz
```

5. Preserve the existing result package boundary: summary/config/metadata/metrics only, no checkpoints, no raw data, no prepared splits.

## Cost estimate

The 5GB 1000-step Modal A100 run reported about `341.63` training seconds. A 3000-step run is 3x the step count, so the training loop should be roughly `1025` seconds before startup, image, clone, extraction, and artifact packaging overhead.

Modal pricing checked on the official pricing page records `Nvidia A100, 40 GB` at `$0.000583 / sec`, and Volumes at `$0.09 / GiB / mo` with included free tier details on that page. Modal bills compute by actual active time rather than idle allocation: https://modal.com/pricing

Rough cost envelope:

| Component | Estimate |
| --- | --- |
| A100-40GB training loop only | about `$0.60` (`1025 sec * $0.000583/sec`) |
| A100-40GB with startup/extraction/package overhead | roughly `$0.65-$0.90` |
| Relative to 5GB 1000-step | about `3x` the GPU training-loop cost |
| CPU / memory / Volume read overhead | small compared with GPU time |
| Volume storage | continues after the run while Volume data remains stored |

The job should stop GPU billing when the Modal app completes. Volume storage cost can continue independently after the GPU function exits.

## Cost gate

Before running, get explicit approval for:

- Modal A100-40GB GPU training
- the estimated `3x` step count relative to the 5GB 1000-step run
- small result package creation under `/vol/results/`
- no checkpoint import into git
- no direct 10000-step run

## Success criteria

The 5GB 3000-step run should be considered successful only if all of these hold:

- Modal app completes successfully.
- `summary.json` reports `success=true`.
- `metrics.jsonl` has `3000` rows.
- `validation_metrics.jsonl` has `10` rows.
- all train losses, validation losses, and gradient norms are finite.
- `checkpoint_reload_match=true`.
- post-run artifact validation passes with `blocker_count=0`.
- train sampling remains `shuffle_buffer`.
- validation sampling remains `shuffle_buffer`.
- `validation_unique_doc_count > 1`.
- `validation_prefix_only_risk=false`.
- local import includes only approved small artifacts.

## Stop conditions

Stop and do not proceed to any longer run if:

- `train_5gb_3000` mode is still missing.
- Modal cannot find the prepared 5GB package.
- result package creation fails.
- metrics row counts do not match expected rows.
- any train loss, validation loss, or gradient norm is non-finite.
- validation coverage regresses to `validation_unique_doc_count <= 1`.
- `validation_prefix_only_risk=true`.
- checkpoint reload fails.
- post-run artifact validation reports blockers.
- cost approval is not explicit.

## Why not jump to 10000-step

The 5GB 1000-step run improved train-side sampling and produced finite systems evidence, but its validation measurement was not representative. MVP-25.C fixes the measurement path, not model quality. A 3000-step run is the next bounded scale step to test whether the longer run remains stable under the corrected validation path. A 10000-step run should wait until 3000-step artifacts and validation coverage are healthy.
