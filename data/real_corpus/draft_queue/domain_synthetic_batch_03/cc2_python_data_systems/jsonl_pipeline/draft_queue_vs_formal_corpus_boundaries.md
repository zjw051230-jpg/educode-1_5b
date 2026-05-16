---
draft_status: candidate
topic_id: PDS-007
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Draft Queue vs Formal Corpus Boundaries

## Concept
A draft queue is a staging area for candidate content. A formal corpus is the reviewed destination. Mixing them too early makes later provenance checks unreliable.

## Explanation
Draft assets are expected to be incomplete, uneven, or still under review. That is why metadata such as `approved_for_training: false` matters. It creates a hard boundary between material that is safe to inspect and material that is safe to train on.

In practice, the boundary affects file paths, naming, and workflow. Draft content can include review notes, intentionally narrow examples, and temporary gaps in coverage. A formal corpus should not inherit those assumptions without an explicit promotion step.

This distinction also helps with tool design. Draft generators can optimize for transparency and small examples, while formal-corpus tools can optimize for stability and scale. If both stages share one directory, it becomes easy to run the wrong command on the wrong files.

## Minimal Example
A reviewer should be able to answer these questions quickly:
- Is this file still a draft candidate?
- Which worker generated it?
- Does it claim training approval?
- Can it be traced back to a topic reservation?

The metadata header answers all four without opening another system.

## Common Pitfalls
- Copying draft files into a raw corpus area “just for convenience”.
- Using the same status values for reserved, candidate, and approved states.
- Forgetting that review notes are acceptable in drafts but not necessarily in promoted assets.
- Treating path boundaries as optional.

## Review Notes
The cleaner the draft/formal boundary is today, the less cleanup is required when these assets move into a real review or promotion workflow.
