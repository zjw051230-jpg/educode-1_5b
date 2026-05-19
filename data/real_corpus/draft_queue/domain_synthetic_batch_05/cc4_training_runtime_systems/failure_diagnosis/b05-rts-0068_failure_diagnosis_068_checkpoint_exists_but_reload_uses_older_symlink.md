---
draft_status: candidate
topic_id: B05-RTS-0068
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Older Symlink Used On Reload

This draft treats older symlink used on reload as a bounded incident reconstruction problem rather than a generic lesson.

**Learning objective:** Identify why a restore picked an older symlink target even though a newer checkpoint directory exists.

## Comparison target
The same runtime scene is summarized two ways below. The goal is to decide which representation preserves the diagnostic truth.

| signal | packet A | packet B | which is safer? |
|---|---|---|---|
| latest step | 12605 | 12606 | B if the save event is confirmed |
| val_loss | 2.020 | 1.960 | depends on denominator visibility |
| reserved_gb | 63.9 | 67.9 | B if eval spike is real |
| event typing | missing | explicit eval_end/save | B |
| throughput | 141840 | 147240 | compare with boundary timing |

## Concrete anchor
This file uses **mini code trace**. The table is not decorative; each cell is a claim that must map back to a concrete artifact.

## Artifact packet
```text
metrics.jsonl: event=eval_end step=12605 val_loss=1.960
metrics.jsonl: event=checkpoint_save step=12606 duration_ms=672
summary.json: latest_step=12606
memory.log: reserved_gb=67.9
```

## Interpretation
Packet B is only safer when its extra specificity comes from source artifacts rather than prettier formatting. If packet A omitted event typing, the omission itself is a runtime clue.

## Failure mode diagnosis
The common mistake is treating the richer-looking table as more truthful by default. In runtime work, the better representation is the one whose fields can be traced back to actual events.

## Short conclusion
Prefer the representation that keeps artifact provenance visible, even if it is less aesthetically compact.

## Next evidence to collect
- resolve the symlink target at the moment of reload
- compare target timestamps with summary latest_step
