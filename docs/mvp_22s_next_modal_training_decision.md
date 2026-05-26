# MVP-22.S Next Modal Training Decision

## Context

Modal A100-40GB has now completed and imported two 2GB prepared-data streaming runs:

- 1000-step: `16384000` tokens seen, import validation passed.
- 3000-step: `49152000` tokens seen, import validation passed.

Both runs validate the systems path, but final validation loss did not clearly improve from 1000 to 3000 steps. The next GPU use should be selected deliberately rather than extending step count by inertia.

## Option A: 2GB 5000-Step

### Pros

- Continues validating the same data scale under a longer bounded run.
- Reuses the already uploaded 2GB prepared package.
- Uses an already prepared config from the 2GB queue.
- Provides additional stability evidence for logging, checkpointing, and streaming over more steps.

### Cons

- Final validation loss did not clearly improve from 1000 to 3000 steps.
- The result may add limited evidence beyond stability.
- It still uses bounded-prefix sampling and does not address scheduler behavior.

### Expected Cost

A conservative planning range is about `$1.5-$4`, depending on Modal runtime, queue behavior, and current pricing.

### Decision

Optional, not default. Use this only if the priority is stability evidence for the 2GB queue.

## Option B: 5GB 1000-Step

### Pros

- Expands data scale, which is more meaningful than only extending the 2GB step count.
- Uses the already prepared local 5GB split package.
- Tests the Modal backend against the next prepared corpus scale.
- Keeps step count bounded while increasing data variety.

### Cons

- Requires uploading the 5GB prepared package to Modal Volume.
- Volume storage increases by about `2.1GB`.
- Training should not start until `preflight_5gb_1000` passes.

### Expected Cost

- Volume storage increase: about `2.1GB × $0.09/GiB/month ≈ $0.19/month`.
- 1000-step training: roughly `$0.5-$1.5`, depending on actual Modal runtime and pricing.

### Decision

Recommended next GPU run if continuing remote training.

## Option C: Scheduler / Sampling Cleanup Before More Training

### Pros

- Addresses `scheduler_config_present_but_not_applied` before making stronger claims.
- Addresses bounded-prefix caveats before spending more GPU budget.
- Improves credibility of future comparisons.
- Local work is free before the next GPU run.

### Cons

- Requires engineering changes and fresh local validation.
- Requires new preflight before remote execution.
- Delays the next GPU result.

### Expected Cost

Local planning or implementation is free. Any later Modal training incurs separate runtime and Volume costs.

### Decision

Recommended before any quality-oriented claim.

## Recommended Route

1. Do local scheduler/sampling cleanup planning or implementation.
2. Run Modal 5GB 1000-step preflight after uploading `/prepared/fineweb_edu_5gb_prepared_splits.tar.gz`.
3. Run Modal 5GB 1000-step training only after preflight passes and explicit approval is given.
4. Keep 2GB 5000-step as an optional stability supplement rather than the default next run.

## Stop Conditions

Stop before additional training if:

- Volume upload is missing or unverified;
- preflight fails;
- readiness reports blockers;
- expected cost is not approved;
- the command would fetch Hugging Face data on the GPU worker;
- the run would download or commit checkpoints by default.
