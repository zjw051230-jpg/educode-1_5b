# E1.R1 Research Paper Schema and Taxonomy Alignment

## 1. Purpose
The purpose of E1.R1 is to align the E-line research paper assistant framework around a standardized metadata schema, explicit source-policy guardrails, and a standardized paper-to-corpus task taxonomy.

## 2. E1.R Findings
E1.R found that:
- the E1 directory structure was basically complete
- raw paper Git ignore behavior was correct
- no raw paper files were being tracked except `.gitkeep`
- no formal corpus pollution was detected
- intake, tokenizer training, and model training had not been run
- the main blocker was metadata field-name mismatch between the intended schema and the draft template/registry fields
- the main taxonomy gap was that standard `task_name` entries were not fully listed
- warnings included a pending E1 `git_commit` field in `docs/experiment_index.md` and missing explicit citation/grounding prohibitions in the source policy

## 3. Fixes Applied
E1.R1 applied the following fixes:
- standardized the formal E-line metadata field names in the metadata schema document
- updated the template JSON to use the standardized field names directly
- updated the registry demo row to use the standardized field names directly
- added explicit no-fabricated-citation and no-ungrounded-generation guardrails to the source policy
- rewrote the task taxonomy into task-family guidance plus a standardized `task_name` catalog
- updated the E1 framework document to reflect the E1.R1 alignment status
- updated `README.md` and `docs/experiment_index.md` so E1 and E1.R1 are recorded consistently

## 4. Metadata Schema Alignment
The formal E-line metadata schema now standardizes the following fields:
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

Compatibility notes were preserved in the schema document so earlier draft names can be mapped forward, but the formal E-line registry and template now use the standardized names directly.

## 5. Source Policy Guardrails
The source policy now explicitly states:
- no fabricated citations, titles, venues, author lists, years, DOIs, arXiv IDs, or experimental claims
- no ungrounded paper generation presented as if it came from real sources

This closes the earlier gap where general provenance rules existed but citation and grounding prohibitions were not written as direct guardrails.

## 6. Task Taxonomy Alignment
The paper-to-corpus taxonomy now uses a two-layer structure:
- task family guidance
- standardized `task_name` catalog

The standardized task set now includes all required E1.R1 task names:
- `paper_reading_note`
- `contribution_extraction`
- `method_summary`
- `method_comparison`
- `related_work_classification`
- `experiment_design`
- `ablation_planning`
- `limitation_detection`
- `reviewer_critique`
- `rebuttal_planning`
- `abstract_revision`
- `introduction_logic_chain`
- `citation_grounding_check`
- `paper_to_code_explanation`
- `reproduction_plan`
- `failure_mode_analysis`

Each task record now includes purpose, input source, output format, citation/source-id requirement, and training-candidate conditions.

## 7. Registry / Template Status
The template file remains template-only and does not represent a real paper.
The registry currently contains a template/demo row only.
No real paper record has been added in E1.R1.

Required conservative values remain explicit in the demo state:
- `allowed_for_training`: `false`
- `allowed_for_rag`: `pending`
- `review_status`: `inbox_unreviewed`

## 8. Gitignore / Raw Paper Safety Recheck
The raw paper inbox remains protected by Git ignore rules.
The tracked file expectation remains:
- `data/research_papers/inbox/raw_papers/.gitkeep`

E1.R1 does not add raw papers to Git.

## 9. Formal Corpus Pollution Recheck
E1.R1 does not move any paper content into:
- `data/real_corpus/raw/synthetic_expanded/`
- `data/real_corpus/processed/`
- `data/real_corpus/splits/`

This step is documentation and metadata-alignment only.

## 10. What E1.R1 Does Not Do
E1.R1 does not:
- download papers
- process concrete papers
- parse PDFs
- create a real paper corpus
- enter the formal corpus
- run intake
- train a tokenizer
- train a model
- modify model code

## 11. Next Step
Recommended next step after E1.R1:
- keep the current framework empty of real paper content until a deliberate paper-registration step is requested
- if real papers are later introduced, register them metadata-first and keep them inbox-only by default
- discuss a narrow E2 step for grounded note-taking, method-summary derivation, or RAG evaluation before any training-candidate discussion
