# MVP-23.P Scheduler Cleanup Plan

## Current Caveat

The current A100/A800 training script records a scheduler caveat in completed run summaries:

```text
scheduler_config_present=true
scheduler_applied=false
scheduler_policy=not_applied
scheduler_config_present_but_not_applied=true
```

This caveat means a top-level `scheduler` config section exists, but the training loop does not construct or step any scheduler. The current behavior is fixed learning rate from the optimizer config.

## Evidence from MVP-21/MVP-22 Summaries

MVP-21 Modal 2GB 1000-step summary records:

| field | value |
|---|---|
| `scheduler_config_present` | `true` |
| `scheduler_applied` | `false` |
| `scheduler_policy` | `not_applied` |
| `scheduler_config_present_but_not_applied` | `true` |

MVP-22 Modal 2GB 3000-step summary records the same scheduler fields.

Metrics inspection confirms fixed LR logging:

| run | first logged LR | final logged LR |
|---|---:|---:|
| 2GB 1000-step | `0.0003` | `0.0003` |
| 2GB 3000-step | `0.0003` | `0.0003` |

The configs contain:

```json
"scheduler": {
  "enabled": false,
  "name": null,
  "reason": "MVP-10 found scheduler_config_present_but_not_applied=true; do not claim a scheduler until the execution script applies one or the report explicitly marks it disabled."
}
```

## Current Script Behavior

`scripts/run_a100_300m_fineweb_edu_10step_training.py` currently:

1. reads `optimizer.learning_rate` into a local `learning_rate` value;
2. creates `torch.optim.AdamW(..., lr=learning_rate, ...)`;
3. runs `optimizer.step()` after gradient clipping;
4. writes `learning_rate=learning_rate` into every metrics row;
5. writes summary fields with `scheduler_applied=false`, `scheduler_policy="not_applied"`, and `scheduler_config_present_but_not_applied=scheduler_config_present`.

There is no scheduler object, no scheduler step order, and no per-step LR lookup from optimizer param groups.

## Proposed Scheduler Policy

Introduce explicit scheduler policy semantics instead of treating every `scheduler` section as accidental intent.

Recommended policies:

| policy | behavior | summary expectation |
|---|---|---|
| `constant` | deliberately keep fixed optimizer LR | `scheduler_applied=false`, `scheduler_config_present_but_not_applied=false` |
| `warmup_cosine` | linear warmup, then cosine decay to configured min LR | `scheduler_applied=true`, `scheduler_policy="warmup_cosine"` |
| `linear_warmup_decay` | linear warmup, then linear decay to configured min LR | optional later policy |

The first implementation should support `constant` and `warmup_cosine`. `linear_warmup_decay` can remain a planned alternative unless a config explicitly needs it.

## Minimal Implementation Plan

1. Extend config interpretation with a small scheduler policy reader:
   - default policy: `constant` when `scheduler.enabled=false`;
   - require `scheduler.name` or `scheduler.policy` for enabled schedulers;
   - reject unknown policies during validation.
2. Add a pure LR schedule function for `warmup_cosine`:
   - inputs: `base_lr`, `step`, `max_steps`, `warmup_steps`, `min_lr_ratio`;
   - output: scalar learning rate.
3. Apply LR before or after optimizer step consistently:
   - recommended: set LR at the start of each optimizer step using the current step number;
   - log the LR actually used for that optimizer step.
4. Keep `constant` simple:
   - no scheduler object;
   - optimizer LR stays fixed;
   - metrics still log `0.0003` or the configured fixed LR.
5. Update summary fields:
   - `scheduler_config_present`;
   - `scheduler_enabled`;
   - `scheduler_policy`;
   - `scheduler_applied`;
   - `scheduler_config_present_but_not_applied`;
   - `learning_rate_mode`.
6. Add tests before implementation:
   - policy parsing for disabled scheduler;
   - constant LR metrics semantics;
   - warmup/cosine LR values at first, warmup boundary, midpoint, and final step;
   - summary caveat field behavior.

## Config Changes Needed

For fixed-LR comparability configs, make the intent explicit:

```json
"scheduler": {
  "enabled": false,
  "policy": "constant",
  "reason": "Fixed LR baseline for comparability with MVP-21/MVP-22 Modal 2GB runs."
}
```

For an applied warmup/cosine config:

```json
"scheduler": {
  "enabled": true,
  "policy": "warmup_cosine",
  "warmup_steps": 100,
  "min_lr_ratio": 0.1
}
```

The optimizer section should keep `learning_rate` as the base LR.

## Validation Plan

Local validation should remain CPU-safe and must not run training by default for this planning stage.

For implementation stage, validate with:

1. unit tests for the schedule function;
2. config validator tests for allowed policies and invalid settings;
3. dry-run summary check showing policy metadata without optimizer steps;
4. a tiny approved local smoke run only in the later implementation milestone, not in MVP-23.P;
5. metrics inspection confirming per-step `learning_rate` changes only when `warmup_cosine` is enabled.

## Backward Compatibility

Historical MVP-21/MVP-22 summaries should not be rewritten. They accurately report the old behavior.

Future fixed-LR runs should use `policy="constant"` so that fixed LR is deliberate and comparable, not an accidental caveat. New summary logic should keep the old fields but change the caveat calculation:

```text
scheduler_config_present_but_not_applied = scheduler_enabled and not scheduler_applied
```

or an equivalent condition that does not flag explicit `constant` policy.

This keeps old result interpretation intact while making new runs clearer.

## What This Does Not Do

- Does not run training.
- Does not change model architecture.
- Does not change optimizer type.
- Does not claim the previous 2GB runs were invalid.
- Does not make model-quality claims.
- Does not decide final production LR policy for long pretraining.
