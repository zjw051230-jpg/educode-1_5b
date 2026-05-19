---
draft_status: candidate
topic_id: B05-RTS-0072
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Dashboard Speedup But Work Dropped

A runtime reviewer usually gets this topic wrong when the title is read without the artifacts that produced it.

**Learning objective:** Review a metrics dashboard that reports speedup because fewer eval rows were logged, not because training got faster.

## Comparison target
The same runtime scene is summarized two ways below. The goal is to decide which representation preserves the diagnostic truth.

| signal | packet A | packet B | which is safer? |
|---|---|---|---|
| latest step | 12617 | 12618 | B if the save event is confirmed |
| val_loss | 2.160 | 2.100 | depends on denominator visibility |
| reserved_gb | 58.3 | 62.3 | B if eval spike is real |
| event typing | missing | explicit eval_end/save | B |
| throughput | 143560 | 148960 | compare with boundary timing |

## Concrete anchor
This file uses **metrics interpretation**. The table is not decorative; each cell is a claim that must map back to a concrete artifact.

## Artifact packet
```text
metrics.jsonl: event=eval_end step=12617 val_loss=2.100
metrics.jsonl: event=checkpoint_save step=12618 duration_ms=688
summary.json: latest_step=12618
memory.log: reserved_gb=62.3
```

## Interpretation
Packet B is only safer when its extra specificity comes from source artifacts rather than prettier formatting. If packet A omitted event typing, the omission itself is a runtime clue.

## Failure mode diagnosis
The common mistake is treating the richer-looking table as more truthful by default. In runtime work, the better representation is the one whose fields can be traced back to actual events.

## Short conclusion
Prefer the representation that keeps artifact provenance visible, even if it is less aesthetically compact.

## Next evidence to collect
- compare dashboard aggregates with raw eval row counts
- verify whether dropped rows changed the throughput denominator
