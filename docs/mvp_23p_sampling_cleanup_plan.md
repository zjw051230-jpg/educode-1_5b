# MVP-23.P Sampling Cleanup Plan

## Current Caveat

The current streaming runs are marked:

```text
bounded_prefix_batches_only=true
```

This means the run consumed the beginning of the prepared JSONL split until it had enough streaming batches. It did not prove randomized coverage of the prepared corpus.

## Evidence from train_data_probe

MVP-21 Modal 2GB 1000-step summary:

| field | value |
|---|---:|
| `train_batches_used` | `4000` |
| `train_data_probe.records_seen` | `39` |
| `train_data_probe.docs_used` | `39` |
| `train_data_probe.cycle_restarts` | `0` |
| `bounded_prefix_batches_only` | `true` |

MVP-22 Modal 2GB 3000-step summary:

| field | value |
|---|---:|
| `train_batches_used` | `12000` |
| `train_data_probe.records_seen` | `115` |
| `train_data_probe.docs_used` | `115` |
| `train_data_probe.cycle_restarts` | `0` |
| `bounded_prefix_batches_only` | `true` |

These records show that the longer run read more prefix documents, but still only consumed an ordered prefix of the train split.

## Why bounded prefix is a limitation

The current runs are valid systems evidence: they prove Modal, prepared data, tokenizer, model/loss, optimizer, validation, logging, checkpoint reload, and import validation can work together.

They are weaker as training interpretation evidence because document ordering can dominate the data slice. If the first records are easier, harder, duplicated, unusually formatted, or domain-skewed, the run may reflect that prefix more than the full prepared corpus distribution. This matters more when comparing 1000-step, 3000-step, 5000-step, or 5GB runs.

## Current Streaming Iterator Behavior

`scripts/streaming_lm_batch_iterator.py` currently:

1. opens one JSONL file in order;
2. yields non-empty approved `text` records as encountered;
3. tokenizes each document;
4. appends optional EOS;
5. creates sliding next-token blocks;
6. groups blocks into batches;
7. restarts the whole batch factory only if more batches are required after file exhaustion.

The iterator has no `shuffle` argument, no shuffle buffer, no document-order randomization, and no shard/window sampling. The A100 configs set `data.shuffle=true`, but the current streaming path does not consume that flag.

## Candidate Solutions

| solution | pros | cons |
|---|---|---|
| document-level full shuffle | simple conceptually; deterministic with seed | requires loading or indexing many documents; less host-RAM friendly |
| seed-controlled shuffle buffer | streaming-friendly; bounded memory; deterministic enough for runs | local randomness only within buffer window; not a full global shuffle |
| shard/window sampling | scalable for larger corpora; can improve coverage | needs shard metadata and more plumbing |
| random access by offsets | strong sampling control | requires offset index generation and validation |

## Recommended First Fix

Implement a seed-controlled document shuffle buffer in the streaming text iterator.

Recommended first policy:

```text
sampling_policy=shuffle_buffer
shuffle_seed=<run seed or explicit data seed>
shuffle_buffer_size=<bounded integer, e.g. 1024 documents>
```

This is the best next step because it preserves the current host-RAM-efficient streaming design and does not require random-access indexing. It also directly addresses the prefix-only caveat for bounded runs.

## Streaming Iterator Changes Needed

Extend the streaming iterator API with optional sampling controls:

```text
sampling_policy: sequential_prefix | shuffle_buffer
shuffle_seed: int | None
shuffle_buffer_size: int
cycle_index: int
```

Required behavior:

1. `sequential_prefix` keeps current behavior and records `bounded_prefix_batches_only=true`.
2. `shuffle_buffer` fills a document buffer, emits documents in seeded pseudo-random order, then continues refilling.
3. If the file is exhausted and another cycle is needed, increment `cycle_restarts` and derive a new deterministic cycle seed.
4. Record sampling metadata in `train_data_probe` and `val_data_probe`.
5. Set `bounded_prefix_batches_only=false` only when the actual iterator used non-prefix sampling.

Validation data should normally stay deterministic and may remain `sequential_prefix` unless the config explicitly requests validation shuffling.

## Determinism / Seed Policy

Use a local `random.Random` instance rather than global random state.

Recommended seed derivation:

```text
base_seed = data.shuffle_seed if present else run.seed
split_seed = base_seed + stable_split_offset
cycle_seed = split_seed + cycle_index
```

Record the resolved seed values in summaries so that future runs can reproduce document order.

The implementation should not rely on Python process-global randomness or filesystem ordering beyond reading the configured JSONL path.

## Validation Plan

For the implementation milestone, add tests before changing behavior:

1. `sequential_prefix` preserves current ordered output.
2. `shuffle_buffer` changes document order deterministically for a fixed seed.
3. different seeds produce different orders on a small synthetic JSONL.
4. `shuffle_buffer_size=1` behaves like prefix and must not clear the prefix caveat.
5. `cycle_restarts` increments when required batches exceed one pass.
6. `train_data_probe` includes `sampling_policy`, `shuffle_seed`, `shuffle_buffer_size`, `cycle_restarts`, and `bounded_prefix_batches_only` semantics.
7. dry-run or inspection checks must not read large data beyond bounded probes.

## What This Does Not Do

- Does not run training.
- Does not download data.
- Does not introduce random-access corpus indexing yet.
- Does not claim model quality.
- Does not require changing model architecture.
- Does not make historical MVP-21/MVP-22 runs non-comparable; it only clarifies that future runs should avoid prefix-only sampling when making stronger interpretations.
