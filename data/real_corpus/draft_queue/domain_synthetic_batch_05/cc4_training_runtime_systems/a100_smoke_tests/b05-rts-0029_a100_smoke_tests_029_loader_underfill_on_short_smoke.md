---
draft_status: candidate
topic_id: B05-RTS-0029
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Loader Underfill On Short Smoke

The narrow goal here is to decide what loader underfill on short smoke means in one specific runtime scene.

**Learning objective:** Review a smoke run where dataloader underfill lowers tokens/sec without any GPU-side fault.

Use this checklist on a bounded artifact packet before turning one runtime anomaly into a broad claim.

## Artifact packet
- `batch size log + throughput rows`
- topic_id: B05-RTS-0029
- writing_form: checklist
- concrete_anchor: before/after comparison

## Pass/fail gates
- [ ] The relevant artifact exists and is named explicitly.
- [ ] At least one neighboring artifact can confirm or deny the same story.
- [ ] The packet includes topic-specific numbers, not only labels.
- [ ] A phase boundary is visible if the anomaly happened near eval or checkpoint save.
- [ ] The apparent failure can be separated from a logging-only explanation.

## Example packet
```text
step=12487 train_tokens_per_sec=130470
step=12487 max_memory_allocated_gb=38.6
step=12487 max_memory_reserved_gb=65.8
step=12488 validation_start seq_len=3072 microbatch=4
step=12489 validation_end val_loss=1.750
```

## Decision table
| question | good sign | warning sign |
|---|---|---|
| do counters advance monotonically? | step and tokens_seen move together | one counter resets or stalls |
| do memory numbers tell one story? | allocated and reserved both stabilize | reserved climbs while allocated resets |
| does the artifact identify the phase? | train/eval/save event is explicit | event type must be guessed |
| can the anomaly be localized? | it begins at one boundary | it is described only as a vague slowdown |

## Failure mode diagnosis
A packet that fails the second and third gates is usually too weak for a strong conclusion. In practice that means the reader should downgrade the interpretation from "bug confirmed" to "artifact mismatch needs follow-up".

## What to inspect next if one gate fails
1. add the adjacent event rows
2. capture the exact config field that controls the phase boundary
3. restate the conclusion in terms of observed artifacts only

## Short decision
Mark the packet as diagnostic-ready only if the anomaly is tied to a concrete phase, a concrete number, and a concrete neighboring artifact.
