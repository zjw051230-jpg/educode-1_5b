# MVP-18.S Next-Scale Decision

## Purpose

This decision note selects the next scale route after MVP-18 restored the intended public16k streaming batch path on A800.

The decision is limited to planning. It does not run training, rent or enter GPU hardware, download data, train tokenizer/model artifacts, modify training main logic, or commit checkpoints, raw corpus files, processed data, split files, or result tarballs.

## Current Evidence

MVP-18 completed a 300M public16k A800 streaming run with:

- `max_steps=1000`;
- `batch_size=8`;
- `gradient_accumulation_steps=4`;
- `sequence_length=512`;
- `data_loading_mode=streaming`;
- `tokens_seen=16384000`;
- `metrics_rows=1000`;
- `validation_rows=10`;
- `checkpoint_reload_match=true`;
- post-run artifact validation and import validation passed.

This resolves the earlier host-side precompute bottleneck for the current bounded setup. It does not establish model quality.

## Options Reviewed

### Option 1: MVP-19 streaming 3000-step on the existing 500MB corpus

Run the current 3000-step public16k config with the MVP-17 streaming path and the already prepared 500MB FineWeb-Edu split package.

Pros:

- Tests the longer-run version of the same path that MVP-18 validated.
- Reuses the current tokenizer, model scale, data package, and artifact validator.
- Avoids adding a new data-preparation variable before proving the restored larger-batch path over a longer run.
- Keeps GPU work bounded and reviewable.

Cons:

- Still not a quality-oriented run.
- Still bounded to the 500MB prepared corpus.
- Consumes another GPU session before addressing scheduler/sampling cleanup.

Decision: recommended next GPU execution if GPU time is available.

### Option 2: MVP-20 2GB FineWeb-Edu prepared corpus

Prepare a larger public corpus slice outside the GPU container, then create processed/split packages for later GPU runs.

Pros:

- Addresses the next data-scale bottleneck.
- Better prepares future quality-oriented or longer systems runs.
- Keeps data preparation on local or CPU/data hosts where bandwidth and storage are easier to control.

Cons:

- Adds data logistics and validation work before the 3000-step streaming path has been tested.
- Increases transfer and storage cost.
- Should not be mixed into the same milestone as the next GPU execution.

Decision: recommended after MVP-19, or earlier only if GPU time is not available but CPU/data preparation time is available.

### Option 3: MVP-21 1B 10-step streaming smoke

Create a larger 1B-class smoke configuration and run a very short streaming execution check.

Pros:

- Tests whether the streaming data path remains compatible with a larger model scale.
- Provides an early read on memory headroom and config validation for future scaling.

Cons:

- Introduces model-scale risk before the 300M streaming path has completed its 3000-step follow-up.
- A 10-step run is useful for systems compatibility but not for learning behavior.
- Requires careful scope boundaries to avoid becoming a premature architecture-scale detour.

Decision: defer until after MVP-19 and data/logistics cleanup, unless the goal explicitly shifts to model-scale smoke testing.

### Option 4: Scheduler and sampling cleanup

Clean up scheduler application and bounded sampling behavior before future quality-oriented runs.

Pros:

- Addresses known engineering caveats from MVP-18: scheduler config was present but not applied.
- Improves interpretability of later training curves.
- Reduces the risk of over-reading bounded-prefix behavior.

Cons:

- Does not itself validate the 3000-step streaming path.
- Should be implemented with test-first coverage and local dry-run validation before any GPU execution.

Decision: important before quality-oriented runs, but not required before the immediate MVP-19 systems follow-up if MVP-19 remains a bounded systems-validation run.

## Recommended Route

1. MVP-19.P: prepare the 3000-step streaming execution/import plan.
2. MVP-19: run A800 streaming 3000-step on the existing 500MB prepared public16k corpus if GPU time is available.
3. MVP-20: prepare a 2GB FineWeb-Edu public corpus on local or CPU/data-host infrastructure, not inside the GPU container.
4. MVP-21: do scheduler/sampling cleanup before any quality-oriented run or larger-model experiment.

## Decision Boundary

The next route should stay conservative: prove the restored 300M streaming path over 3000 steps before adding a larger corpus or larger model. If GPU time is not available, use the pause to prepare MVP-20 data logistics and scheduler/sampling cleanup locally.

## Selected Next Step

Selected next step: MVP-19.P, a local execution/import plan for the A800 streaming 3000-step public16k run.

MVP-19 execution should happen only after explicit approval and should still be described as bounded training-systems evidence.
