---
draft_status: candidate
topic_id: B05-RTS-0070
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Nan Val Loss From One Batch

Instead of explaining nan val loss from one batch in the abstract, this file starts from a concrete artifact packet.

**Learning objective:** Differentiate a single corrupt validation batch from a systemic numeric instability.

## Comparison target
The same runtime scene is summarized two ways below. The goal is to decide which representation preserves the diagnostic truth.

| signal | packet A | packet B | which is safer? |
|---|---|---|---|
| latest step | 12611 | 12612 | B if the save event is confirmed |
| val_loss | 1.880 | 1.820 | depends on denominator visibility |
| reserved_gb | 51.5 | 55.5 | B if eval spike is real |
| event typing | missing | explicit eval_end/save | B |
| throughput | 142700 | 148100 | compare with boundary timing |

## Concrete anchor
This file uses **config snippet**. The table is not decorative; each cell is a claim that must map back to a concrete artifact.

## Artifact packet
```text
metrics.jsonl: event=eval_end step=12611 val_loss=1.820
metrics.jsonl: event=checkpoint_save step=12612 duration_ms=680
summary.json: latest_step=12612
memory.log: reserved_gb=55.5
```

## Interpretation
Packet B is only safer when its extra specificity comes from source artifacts rather than prettier formatting. If packet A omitted event typing, the omission itself is a runtime clue.

## Failure mode diagnosis
The common mistake is treating the richer-looking table as more truthful by default. In runtime work, the better representation is the one whose fields can be traced back to actual events.

## Short conclusion
Prefer the representation that keeps artifact provenance visible, even if it is less aesthetically compact.

## Next evidence to collect
- isolate the offending batch id and sample count
- compare neighboring batches to rule out full-loop instability
