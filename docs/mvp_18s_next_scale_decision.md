# MVP-18.S Next-Scale Decision

## Purpose

This note records the next-scale decision after MVP-18 restored the public16k streaming path with `batch_size=8` / `gradient_accumulation_steps=4` on A800.

The decision is limited to documentation and route selection. It does not run training, enter A100/A800, train tokenizer/model artifacts, download data, modify training main logic, or commit checkpoints, `raw.jsonl`, processed data, split files, or result tarballs.

## Current Evidence

MVP-18 completed the 300M public16k A800 streaming 1000-step run with:

- `data_loading_mode=streaming`;
- `batch_size=8`;
- `gradient_accumulation_steps=4`;
- `max_steps=1000`;
- `tokens_seen=16384000`;
- `final_train_loss=2.877289`;
- `final_val_loss=8.752452`;
- `metrics_rows=1000`;
- `validation_rows=10`;
- `checkpoint_reload_match=true`;
- post-run artifact validation passed.

This resolves the current host-RAM precompute blocker. It does not prove model quality.

## A. MVP-19 Streaming 3000-Step on 500MB

Run the existing 3000-step public16k config with the MVP-17 streaming iterator and the prepared 500MB FineWeb-Edu split package.

Pros:

- Directly validates longer streaming stability on the same restored path.
- Reuses the current tokenizer, 300M model config, 500MB prepared splits, import validator, and artifact policy.
- Keeps the next GPU run bounded and comparable to the MVP-18 result.
- Avoids adding corpus-scale or model-scale variables before proving the 3000-step streaming path.

Cons:

- Still uses only the 500MB prepared corpus.
- Still risks bounded-corpus overfitting or repeated-prefix behavior.
- Still remains training-systems evidence, not a serious quality-oriented training run.

Decision: recommended short next GPU run if using the current setup and if GPU time is available.

## B. MVP-20 2GB FineWeb-Edu Prepared Corpus

Prepare a larger public corpus slice outside the GPU container and package processed train/validation splits for later GPU execution.

Pros:

- Improves data scale beyond the current 500MB slice.
- Reduces the bounded tiny-corpus problem before more serious longer training.
- Moves network-bound and CPU-bound data preparation away from paid GPU sessions.
- Creates a better base for later training-quality experiments.

Cons:

- Requires local or CPU-cloud data preparation.
- Requires larger transfer packages and stronger checksum/logistics discipline.
- Adds a new data variable before the 3000-step streaming run if done first.

Decision: recommended next data step before serious longer training.

## C. MVP-21 1B 10-Step Streaming Smoke

Create a bounded 1B-class streaming smoke to validate larger-model materialization and memory behavior.

Pros:

- Tests whether the streaming data path remains compatible with larger model materialization.
- Gives an early memory and config read for the next model scale.
- Can stay short and bounded if scoped as a 10-step smoke only.

Cons:

- Should come after the 300M streaming path is stable.
- Should come after data-scale and config review decisions are clearer.
- A 10-step smoke is systems compatibility evidence only, not training evidence.

Decision: secondary, after 300M streaming and config review.

## D. Scheduler / Sampling Cleanup

Clean up scheduler application and bounded sampling behavior before any quality-oriented claim.

Pros:

- Improves training-curve interpretability.
- Addresses `scheduler_config_present_but_not_applied=true` from MVP-18.
- Reduces over-reading risk from `bounded_prefix_batches_only=true`.
- Makes later longer runs easier to compare.

Cons:

- Requires code changes and verification even if the change is smaller than a GPU run.
- Should be tested locally before any GPU execution.
- Does not itself prove longer streaming stability.

Decision: should be done before claiming training quality.

## Recommended Route

1. MVP-19.P: prepare 3000-step streaming execution/import plan.
2. MVP-19: A800 streaming 3000-step if GPU time is available.
3. MVP-20: prepare 2GB public corpus using local/CPU host, not GPU fetch.
4. MVP-21: scheduler/sampling cleanup before quality-oriented run.

## Decision Boundary

The immediate route should not jump to H200/B200 or a larger model just because the host-RAM blocker is fixed. The evidence supports one more bounded 300M streaming stability run, followed by data logistics and scheduler/sampling cleanup before stronger training-quality claims.
