# D17 Draft Corpus Review Gate Plan

## 1. Purpose
The purpose of this document is to define the review gate that keeps the D17 draft queue separate from the formal training corpus.

This step does not review draft body text yet.
It only defines the gate that future draft candidates must pass before any later approval discussion.

## 2. Gate Principles
The review gate exists to enforce all of the following:
- draft queue content is not training data by default
- candidate drafts must remain project-authored or otherwise explicitly approved later
- no private data may enter the queue
- no external copied text may enter the queue
- educational relevance must remain aligned to the project backbone:
  - CS
  - ML
  - Python
  - Transformer training systems

## 3. Required Checks for Any Future Draft
Before any future candidate draft is considered for promotion beyond the queue, review should confirm:
- the file matches a registered `topic_id`
- the file path matches the registered category and subcategory
- the metadata header is present
- `approved_for_training` is still `false` until the reviewer changes it explicitly
- `contains_external_text` is `false`
- `contains_private_data` is `false`
- the content is educational and domain-relevant
- the content is not a bulk low-signal text dump
- the content does not make unsupported model-quality claims

## 4. Stop Conditions
Stop and reject or quarantine a draft if any of the following hold:
- the draft copies external text
- the draft includes private or sensitive data
- the draft is unrelated to the project backbone
- the draft bypasses the topic registry
- the draft path does not match the reserved category location
- the draft attempts to mark itself training-approved without explicit review

## 5. Suggested Review States
Suggested later review states for registry-driven workflows:
- `reserved_not_written`
- `draft_written_pending_review`
- `needs_revision`
- `reviewed_not_approved`
- `approved_for_promotion_consideration`

This document does not apply those states yet.
It only records a recommended direction for later governance.

## 6. Promotion Boundary
Even a well-reviewed draft should not automatically become formal corpus data.
Any later promotion should remain a separate explicit step that may require:
- category-level approval
- provenance confirmation
- formatting normalization
- intake tooling
- corpus-balance review

## 7. Next Step
Recommended next step:
- implement a small read-only inspector that checks draft queue files against `topic_registry.jsonl` and reports header or path mismatches
