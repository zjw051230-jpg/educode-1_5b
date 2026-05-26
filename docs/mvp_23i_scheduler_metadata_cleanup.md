# MVP-23.I Scheduler Metadata Cleanup

## Purpose

Implement the first scheduler cleanup step after MVP-23.P by making fixed learning-rate behavior explicit in the training and readiness metadata.

This implementation keeps the current training math unchanged. The default behavior remains fixed LR from `optimizer.learning_rate`.

## Previous Caveat

MVP-21 and MVP-22 Modal 2GB summaries recorded:

```text
scheduler_config_present=true
scheduler_applied=false
scheduler_policy=not_applied
scheduler_config_present_but_not_applied=true
```

That was accurate for the old script, but it made intentionally fixed-LR runs look like accidental scheduler omissions.

## Root Cause

The training script always used the optimizer learning rate directly:

```text
optimizer.learning_rate -> AdamW(lr=learning_rate) -> metrics learning_rate=learning_rate
```

No scheduler object was created or stepped. Summary generation then treated the mere presence of a top-level `scheduler` section as a caveat.

## Implemented Change

`scripts/run_a100_300m_fineweb_edu_10step_training.py` now includes lightweight scheduler metadata helpers:

- `get_scheduler_policy(config)`
- `build_scheduler_metadata(config, base_learning_rate, final_learning_rate)`

The helpers resolve missing scheduler config or scheduler config without `policy` as explicit `constant` policy. Unsupported policies, including `warmup_cosine`, fail clearly instead of being silently ignored.

Dry-run and training summaries now record:

```text
scheduler_config_present
scheduler_enabled
scheduler_policy
scheduler_applied
scheduler_config_present_but_not_applied
learning_rate_mode
base_learning_rate
final_learning_rate
```

## Constant LR Semantics

For the current fixed-LR route:

```text
scheduler_policy=constant
scheduler_applied=false
scheduler_config_present_but_not_applied=false
learning_rate_mode=constant
base_learning_rate=0.0003
final_learning_rate=0.0003
```

`future constant` means the fixed LR is deliberate. It is not an accidental scheduler caveat.

## Config Changes

The following configs now include explicit `scheduler.policy="constant"`:

- `configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json`
- `configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json`
- `configs/a100/fineweb_edu_2gb_300m_5000step_public16k_execute.json`
- `configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json`
- `configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json`

No learning-rate values, batch sizes, gradient accumulation settings, or max-step counts were changed.

## Dry-run Validation

The 2GB 1000-step dry-run should remain a no-training path and should report:

```text
exact_parameter_count=336106496
data_loading_mode=streaming
scheduler_policy=constant
scheduler_applied=false
scheduler_config_present_but_not_applied=false
learning_rate_mode=constant
no_training=true
```

The dry-run does not perform forward, backward, optimizer, scheduler, checkpoint, or training work.

## Readiness Validation

`scripts/check_a100_execution_readiness.py` now resolves scheduler metadata before writing `execution_readiness_summary.json`.

For `scheduler.policy="constant"`, readiness should not add a scheduler blocker or caveat. Readiness summary records:

```text
scheduler_policy=constant
learning_rate_mode=constant
```

Unsupported scheduler policy values produce a blocker:

```text
unsupported scheduler policy
```

## Backward Compatibility

Historical MVP-21 and MVP-22 imported summaries are not rewritten. They remain faithful records of the old behavior.

Future fixed-LR runs are comparable to the old runs because the optimizer learning rate and training loop math remain unchanged. The difference is metadata clarity.

## What This Does Not Do

- Does not run Modal.
- Does not enter A100/A800.
- Does not run real training.
- Does not train tokenizer/model.
- Does not download data.
- Does not produce or commit checkpoints.
- Does not change model core architecture.
- Does not implement `warmup_cosine`.
- Does not resolve `bounded_prefix_batches_only`.
- Does not implement sampling shuffle buffer.

## Next Step

Proceed to MVP-23.J streaming sampling shuffle buffer so future bounded runs can avoid prefix-only sampling caveats.
