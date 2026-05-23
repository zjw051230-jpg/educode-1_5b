# E1 Research Paper Metadata Schema

## 1. Purpose
The purpose of the E1 metadata schema is to define the standard reviewable record for each research paper source that enters the research paper assistant framework.

This schema is for provenance, review state, and usage control.
Registration alone does not grant training approval or RAG approval.

## 2. Standard E-line Field Names
Every formal E-line paper registry record and template must use these standard field names:
- `paper_id`
- `title`
- `authors`
- `venue`
- `year`
- `url`
- `local_raw_path`
- `source_type`
- `license`
- `license_confidence`
- `full_text_use_scope`
- `allowed_for_training`
- `allowed_for_rag`
- `contains_external_text`
- `user_note_available`
- `review_status`
- `notes`

No near-synonym replacement fields should be used as the formal E-line registry schema.

## 3. Field Meanings
Identity and bibliographic fields:
- `paper_id`: stable local identifier used across metadata, notes, RAG references, and derived artifacts
- `title`: paper title or note title when the source is a user-authored note record
- `authors`: author list when known
- `venue`: venue, archive, journal, conference, workshop, or other source label when known
- `year`: publication or release year when known
- `url`: external landing page, DOI page, arXiv page, OpenAlex page, PMC Open Access page, or other canonical source link when known

Local source and type fields:
- `local_raw_path`: current local inbox path for a raw paper file or related source artifact when one exists
- `source_type`: source category such as `pdf`, `arxiv`, `openalex`, `pmc_oa`, `user_note`, or `other`

License and use-control fields:
- `license`: explicit reviewed license label, or `unknown` when not yet confirmed
- `license_confidence`: review confidence such as `unknown`, `low`, `medium`, `high`, or `confirmed`
- `full_text_use_scope`: default or reviewed scope such as `source_library_only`, `rag_only`, `metadata_only`, `open_license_training_candidate`, or `user_authored_note`
- `allowed_for_training`: boolean gate for formal training use; default must remain `false` until later formal review explicitly changes it
- `allowed_for_rag`: reviewed RAG state such as `pending`, `approved`, or `rejected`

Content-state and review fields:
- `contains_external_text`: whether the source record depends on non-project-authored paper text or another external text source
- `user_note_available`: whether user-authored notes are already attached or available for this paper record
- `review_status`: current review stage such as `inbox_unreviewed`, `metadata_recorded`, `rag_only`, `derived_notes_ready_for_review`, or `training_rejected`
- `notes`: freeform review notes, license notes, provenance reminders, or compatibility notes

## 4. Default Conservative Posture
Default assumptions for a newly registered paper source:
- `allowed_for_training` must be `false`
- `allowed_for_rag` should remain `pending` until reviewed
- `review_status` should start as `inbox_unreviewed`
- `full_text_use_scope` should remain conservative unless later review explicitly expands it

Important rule:
- no record becomes training-approved merely because it exists in the registry

## 5. Compatibility Notes for Older Draft Fields
Earlier E1 draft records used near-synonym fields.
Those mappings are:
- `source_path` -> `local_raw_path`
- `license_status` / `license_notes` -> `license` / `license_confidence` / `notes`
- `use_scope` -> `full_text_use_scope`
- `training_eligibility` -> `allowed_for_training`
- `contains_user_notes` -> `user_note_available`

These mappings are compatibility notes only.
The formal E-line registry and template must now use the standard field names from Section 2.

## 6. Template and Registry Requirement
The following files must use the standard field names directly:
- `data/research_papers/metadata/paper_source_record.template.json`
- `data/research_papers/metadata/paper_source_registry.jsonl`

If the project keeps a demo row in the registry, that row must stay clearly marked as template/demo only and must not imply that a real paper has been reviewed.

## 7. What This Schema Does Not Do
This schema does not:
- download papers
- parse PDFs automatically
- authorize copying paper full text into the formal corpus
- grant training approval
- replace later human review of notes, summaries, RAG outputs, or training-candidate artifacts
