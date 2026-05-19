# E1 Research Paper Metadata Schema

## 1. Purpose
The purpose of the E1 metadata schema is to define the minimum reviewable record for each research paper source that enters the research paper assistant framework.

This schema is for provenance and usage control.
It does not grant training approval.

## 2. Required Record Identity
Every paper source record should include:
- `paper_id`
- `title`
- `authors`
- `year`
- `venue`
- `source_type`
- `source_path`
- `source_origin`

Meaning:
- `paper_id` is the stable local identifier used across metadata, derived artifacts, and review notes
- `source_path` points to the current local source location or small registry artifact
- `source_origin` records whether the source was user-provided, project-generated, or template-only

## 3. License and Use-Control Fields
Every record should also include:
- `license_status`
- `license_notes`
- `use_scope`
- `training_eligibility`

Recommended value shapes:
- `license_status`: `unknown_pending_review`, `open_license_confirmed`, `restricted_no_training`, `user_notes_only`, or other explicit reviewed value
- `use_scope`: array values such as `source_library`, `rag_candidate`, `metadata_only`, `user_notes_candidate`, `project_summary_candidate`, `training_candidate_pending_review`
- `training_eligibility`: `not_approved`, `conditionally_reviewable`, or `approved_only_after_formal_review`

Important rule:
- no record may be treated as training-approved only because it exists in the registry

## 4. Content-State Fields
Each record should track whether the source includes:
- `contains_full_text`
- `contains_user_notes`
- `contains_project_authored_summary`
- `abstract_status`
- `method_summary_status`

Purpose:
- separate original paper text from user-authored or project-authored derived content
- make it clear which downstream transformations may be safer to review for corpus use

## 5. Provenance and Review Fields
Each record should include:
- `provenance_status`
- `citation`
- `notes`
- `review_status`

Recommended review states:
- `inbox_only`
- `metadata_recorded`
- `rag_only`
- `derived_notes_ready_for_review`
- `draft_queue_candidate`
- `training_rejected`
- `template_only`

## 6. Minimal Example
See:
- `data/research_papers/metadata/paper_source_record.template.json`

The template is intentionally conservative:
- full text present
- training not approved
- use scope limited to source-library / RAG / metadata handling until later review

## 7. What E1 Metadata Does Not Do
This schema does not:
- parse paper PDFs automatically
- decide that a paper is open-license enough for training
- authorize copying full text into the formal corpus
- replace later human review of summaries, notes, or derived assistant data
