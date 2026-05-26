# MVP-23.P Cleanup Implementation Checklist

## Scheduler checklist

### Config schema

- [ ] Add explicit `scheduler.policy` support.
- [ ] Allow `constant` for fixed-LR baseline configs.
- [ ] Allow `warmup_cosine` for applied scheduler configs.
- [ ] Reject unknown scheduler policies.
- [ ] Validate `warmup_steps` is a non-negative integer when required.
- [ ] Validate `min_lr_ratio` is within an accepted range, such as `0.0 <= min_lr_ratio <= 1.0`.
- [ ] Preserve old configs by interpreting `enabled=false` as `constant` for future runs.

### Learning rate schedule function

- [ ] Add a pure function for constant LR.
- [ ] Add a pure function for warmup + cosine LR.
- [ ] Cover step `1`, warmup boundary, midpoint, and final step.
- [ ] Keep `optimizer.learning_rate` as the base LR.
- [ ] Do not change optimizer type.

### Optimizer/scheduler step order

- [ ] Set the LR used for the step before metrics logging.
- [ ] Keep gradient accumulation unchanged.
- [ ] Keep gradient clipping before optimizer step.
- [ ] For `constant`, keep the optimizer LR unchanged.
- [ ] For `warmup_cosine`, update optimizer param group LR deterministically per optimizer step.

### Metrics logging

- [ ] Log the actual LR used for each optimizer step.
- [ ] Keep the existing `learning_rate` metrics field name.
- [ ] Confirm fixed-LR configs still log a constant LR.
- [ ] Confirm warmup/cosine configs log changing LR values.

### Summary logging

- [ ] Record `scheduler_config_present`.
- [ ] Record `scheduler_enabled`.
- [ ] Record `scheduler_policy`.
- [ ] Record `scheduler_applied`.
- [ ] Record `learning_rate_mode`.
- [ ] Record `scheduler_config_present_but_not_applied=false` for deliberate `constant` policy.
- [ ] Record `scheduler_config_present_but_not_applied=true` only for an enabled scheduler that was not applied.

### Dry-run behavior

- [ ] Dry-run should report scheduler policy metadata.
- [ ] Dry-run should not perform optimizer or scheduler steps.
- [ ] Dry-run should not write misleading `scheduler_applied=true`.

### Backward compatibility

- [ ] Do not rewrite historical MVP-21/MVP-22 summaries.
- [ ] Keep old metrics field names stable.
- [ ] Preserve fixed-LR comparability by using explicit `constant` policy.
- [ ] Document any config migration in the implementation report.

### Tests

- [ ] Test config validation for `constant`.
- [ ] Test config validation for `warmup_cosine`.
- [ ] Test invalid scheduler policy rejection.
- [ ] Test warmup/cosine numerical outputs.
- [ ] Test summary caveat fields for constant vs applied scheduler.
- [ ] Test metrics LR logging with a tiny local smoke path only in the implementation milestone.

## Sampling checklist

### Streaming iterator API extension

- [ ] Add `sampling_policy` argument.
- [ ] Add `shuffle_seed` argument.
- [ ] Add `shuffle_buffer_size` argument.
- [ ] Keep default behavior equivalent to current sequential prefix mode.
- [ ] Avoid loading the full corpus into memory.

### Shuffle buffer

- [ ] Implement bounded document-level shuffle buffer.
- [ ] Use `random.Random`, not global randomness.
- [ ] Emit deterministic order for a fixed seed.
- [ ] Treat `shuffle_buffer_size <= 1` as prefix-equivalent.
- [ ] Preserve source validation checks before yielding text.

### Seed handling

- [ ] Use `data.shuffle_seed` when present.
- [ ] Fall back to `run.seed`.
- [ ] Derive stable split-specific seeds.
- [ ] Derive cycle-specific seeds if cycling occurs.
- [ ] Record resolved seeds in stats and summary.

### Repeat/cycle behavior

- [ ] Keep `cycle_restarts` tracking.
- [ ] Increment cycle count only after a full pass is exhausted and more batches are needed.
- [ ] Derive a new deterministic cycle seed for shuffle-buffer mode.
- [ ] Raise an error if a cycle produces no full batches.

### train_data_probe fields

- [ ] Preserve `records_seen`.
- [ ] Preserve `docs_used`.
- [ ] Preserve `empty_text_count`.
- [ ] Preserve `token_ids_streamed`.
- [ ] Preserve `blocks_yielded`.
- [ ] Preserve `cycle_restarts`.
- [ ] Add `sampling_policy`.
- [ ] Add `shuffle_seed`.
- [ ] Add `shuffle_buffer_size`.
- [ ] Add `bounded_prefix_batches_only` or enough fields for summary to compute it honestly.

### Summary fields

- [ ] Record `sampling_policy`.
- [ ] Record `shuffle_seed`.
- [ ] Record `shuffle_buffer_size`.
- [ ] Record train and val `cycle_restarts`.
- [ ] Set `bounded_prefix_batches_only=true` for sequential-prefix sampling.
- [ ] Set `bounded_prefix_batches_only=false` only when non-prefix sampling actually ran.

### Tests

- [ ] Test sequential-prefix order compatibility.
- [ ] Test shuffle-buffer deterministic order for fixed seed.
- [ ] Test different seeds produce different order on a small input.
- [ ] Test `shuffle_buffer_size=1` remains prefix-equivalent.
- [ ] Test cycle restart accounting.
- [ ] Test stats fields in `to_dict()`.
- [ ] Test dry-run or inspection does not require reading a large corpus.
