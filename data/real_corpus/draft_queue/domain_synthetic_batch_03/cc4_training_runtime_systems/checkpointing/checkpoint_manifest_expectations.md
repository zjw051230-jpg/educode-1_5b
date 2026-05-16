---
draft_status: candidate
topic_id: RTS-007
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Checkpoint Manifest Expectations

## Concept
A checkpoint manifest is a small index that explains what artifacts belong to a run.
It is especially helpful when a run produces multiple save points.

## Explanation
Instead of asking reviewers to inspect filenames by guesswork, a manifest can list:
- checkpoint names
- global steps
- save timestamps
- whether each file is resumable or final-only
- which file is considered best for validation
- which file is just the latest chronological save

A manifest helps keep experiment directories readable.
It also reduces accidental use of the wrong artifact.

## Minimal Example
A checkpoint folder may contain:
- `step_0100.pt`
- `step_0200.pt`
- `best_val.pt`
- `latest.pt`
- `manifest.json`

The manifest might explain that `best_val.pt` is the lowest validation snapshot while `latest.pt` is the most recent save.
Those are not always the same file.

## Common Pitfalls
One pitfall is relying on filename sorting alone.
Another is storing aliases like `best` or `latest` without documenting what they mean.
A third is forgetting to update the manifest after deleting old saves.
A fourth is letting the manifest drift from the actual directory contents.

## Review Notes
The main value of a manifest is reducing ambiguity.
For educational runtime systems, that ambiguity matters because many failures happen after a handoff between the person who launched a run and the person who reviews it.
A small index file can save a large amount of cleanup time.
