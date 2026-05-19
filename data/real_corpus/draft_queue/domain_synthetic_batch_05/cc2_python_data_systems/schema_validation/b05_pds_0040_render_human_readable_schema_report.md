---
draft_status: candidate
topic_id: B05-PDS-0040
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Render Human Readable Schema Report

## Incident summary
This failure analysis trains the reader to render a compact human-readable schema report from toy validation results.

## Failure surface
- working area: `schema_validation`
- anchor: small pseudo-run log
- visible symptom: counts, labels, or shapes disagree with local expectations

## Short evidence pack
```text
expected: train=8, val=1, test=1
observed: train=8, val=2, test=0
leakage_check: duplicate document_family_id in train and val
```

## Root cause
The pipeline applied a late-stage convenience step that contradicted an earlier assumption. That contradiction, not the final exception, is the thing the learner should notice.

## Repair boundary
A good repair changes the smallest number of assumptions while preserving reviewability. If the fix hides evidence, the fix is wrong for draft review.

## Verification cue
After repair, the same evidence pack should become boring: no duplicate family ids, no missing split bucket, and no unexplained count drift.

## Takeaway
The topic stays specific because it targets one narrow move: render a compact human-readable schema report from toy validation results.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.
