---
draft_status: candidate
topic_id: PDS-019
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Status Field Meanings for Draft Assets

## Concept
Status fields communicate where an asset is in the review pipeline. The values should be few, explicit, and hard to misread.

## Explanation
When draft assets move between workers, reviewers, and later promotion steps, a status field prevents guesswork. A reader should not need tribal knowledge to interpret whether a file is merely reserved, actively written, ready for review, or approved.

Status values also help separate content quality from workflow state. A file can be clearly written and still remain a draft candidate because it has not passed review. That distinction is important when multiple directories look similar.

For this project, a conservative draft status such as `candidate` pairs well with `approved_for_training: false`. The two fields reinforce each other: one describes workflow stage, the other describes training eligibility.

## Minimal Example
Possible meanings in a broader workflow:
- `reserved_not_written`: topic allocated, file not yet generated
- `candidate`: draft file exists and awaits review
- `approved`: explicitly promoted after review

The exact vocabulary matters less than documenting it in one place.

## Common Pitfalls
- Reusing one status value for several different states.
- Setting workflow status without updating training-approval flags.
- Assuming file path alone communicates readiness.
- Creating status values that sound precise but lack written meaning.

## Review Notes
Short, well-defined status fields reduce accidental misuse of draft assets and make batch summaries easier to interpret.
