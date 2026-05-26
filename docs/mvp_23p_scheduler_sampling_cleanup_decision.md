# MVP-23.P Scheduler and Sampling Cleanup Decision

## Purpose

Decide the local engineering direction after the Modal A100 2GB 1000-step and 3000-step streaming runs.

This is a planning and interpretability gate. It does not run training and does not make model-quality claims.

## Why Not Continue Blindly to 2GB 5000-Step

The Modal 2GB 3000-step run validated the longer systems path, but it did not clearly improve final validation loss over the 1000-step run:

| run | final_val_loss | tokens_seen |
|---|---:|---:|
| 2GB 1000-step | `9.012106` | `16384000` |
| 2GB 3000-step | `9.043165` | `49152000` |

The 3000-step result is useful because it proves that Modal, prepared-data transfer, streaming batches, logging, validation, checkpoint reload, and result import can work over a longer bounded run. It is not a strong reason to extend the same setup by inertia.

Two caveats now limit interpretation:

1. Scheduler behavior is not explicit enough. The config has a scheduler section, but the script does not apply a scheduler.
2. Sampling is still prefix-bounded. The streaming iterator reads ordered JSONL records until enough batches are produced.

Cleaning these up before the next paid GPU run makes future comparisons more credible.

## Scheduler Decision

The next implementation stage should introduce explicit scheduler semantics:

1. `constant` means deliberately fixed LR and should not be treated as an accidental caveat.
2. `warmup_cosine` means the training loop actually updates LR and logs the LR used per step.
3. Historical MVP-21/MVP-22 summaries should remain unchanged.

Recommended first implementation milestone:

```text
MVP-23.I implement scheduler metadata cleanup
```

This milestone should first make fixed-LR runs explicit and remove the accidental caveat for future `constant` configs. If `warmup_cosine` is added in the same milestone, it must include tests and metrics evidence that LR changes as expected.

## Sampling Decision

The next sampling implementation should avoid a large random-access redesign.

Recommended first implementation milestone:

```text
MVP-23.J implement streaming sampling shuffle buffer
```

A seed-controlled shuffle buffer is the best first fix because it preserves the host-RAM-efficient streaming path while making future bounded runs no longer prefix-only.

Future summaries should record:

```text
sampling_policy
shuffle_seed
shuffle_buffer_size
cycle_restarts
bounded_prefix_batches_only
```

`bounded_prefix_batches_only=false` should be set only when the actual data iterator used a non-prefix policy.

## Recommended Next Stage

1. `MVP-23.I` implement scheduler metadata cleanup.
2. `MVP-23.J` implement streaming sampling shuffle buffer.
3. `MVP-24.P` run local/Modal preflight on 2GB after cleanup.
4. `MVP-24` run 5GB 1000-step only after cleanup gate passes and cost is explicitly approved.

## Execution Boundaries

This planning stage does not:

- run Modal;
- enter A100/A800;
- run training;
- train tokenizer/model;
- download data;
- produce checkpoints;
- change model core architecture;
- modify the training main logic.

## Decision

Do local scheduler and sampling cleanup before more longer or larger-corpus GPU runs.

The preferred GPU route after cleanup is a 5GB 1000-step preflight and then a 5GB 1000-step run only after explicit approval. The 2GB 5000-step route remains optional stability evidence, not the default next action.
