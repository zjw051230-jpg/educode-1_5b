---
draft_status: candidate
topic_id: B05-RTS-0064
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Stale Summary And Missing Event

The narrow goal here is to decide what stale summary and missing event means in one specific runtime scene.

**Learning objective:** Diagnose a run where summary.json says eval passed but the final eval_end event never reached metrics.jsonl.

## Comparison target
The same runtime scene is summarized two ways below. The goal is to decide which representation preserves the diagnostic truth.

| signal | packet A | packet B | which is safer? |
|---|---|---|---|
| latest step | 12593 | 12594 | B if the save event is confirmed |
| val_loss | 1.880 | 1.820 | depends on denominator visibility |
| reserved_gb | 61.8 | 65.8 | B if eval spike is real |
| event typing | missing | explicit eval_end/save | B |
| throughput | 140120 | 145520 | compare with boundary timing |

## Concrete anchor
This file uses **metrics interpretation**. The table is not decorative; each cell is a claim that must map back to a concrete artifact.

## Artifact packet
```text
metrics.jsonl: event=eval_end step=12593 val_loss=1.820
metrics.jsonl: event=checkpoint_save step=12594 duration_ms=656
summary.json: latest_step=12594
memory.log: reserved_gb=65.8
```

## Interpretation
Packet B is only safer when its extra specificity comes from source artifacts rather than prettier formatting. If packet A omitted event typing, the omission itself is a runtime clue.

## Failure mode diagnosis
The common mistake is treating the richer-looking table as more truthful by default. In runtime work, the better representation is the one whose fields can be traced back to actual events.

## Short conclusion
Prefer the representation that keeps artifact provenance visible, even if it is less aesthetically compact.

## Next evidence to collect
- capture the metrics tail around the missing eval_end boundary
- compare summary write time with checkpoint save time
