---
draft_status: candidate
topic_id: PDS-005
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Minimal Fields for Processed Records

## Concept
A processed record should include only the fields needed for later review, batching, and traceability. Minimal fields are easier to validate and less likely to drift.

## Explanation
For a synthetic draft corpus, a compact schema is a feature, not a limitation. If every row has a stable `id`, a `text` payload, a `source_category`, and a small amount of provenance such as `topic_id` or `language`, most educational checks become straightforward.

The schema should stay small enough that a reviewer can hold it in working memory. When the record grows many optional fields, different draft files begin to use different conventions, and later tooling spends more effort normalizing metadata than inspecting content quality.

A minimal record can still be expressive. For example, `text` stores the learning content, `id` helps deduplicate, `source_category` keeps draft assets distinct from formal corpora, and `language` supports simple reporting. Extra fields should only appear when a concrete review task needs them.

## Minimal Example
```json
{
  "id": "pds-005-example-01",
  "topic_id": "PDS-005",
  "text": "Validation should reject empty training examples.",
  "source_category": "synthetic_examples",
  "language": "en"
}
```

## Common Pitfalls
- Storing redundant counts that can be recomputed later.
- Adding nested metadata blobs without a reviewer use case.
- Omitting stable IDs and then struggling to compare revisions.
- Mixing processing state with content fields.

## Review Notes
A minimal processed record is easier to audit, easier to rewrite, and easier to promote later if the draft is approved. Extra metadata is only helpful when it solves a specific review problem.
