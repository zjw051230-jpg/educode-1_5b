# E1 Paper-to-Corpus Task Taxonomy

## 1. Purpose
This taxonomy defines the kinds of research-paper assistant tasks that may be built from paper sources while preserving the boundary between source material, RAG use, and possible training candidates.

It uses a two-layer structure:
- A. task family guidance
- B. standardized `task_name` records

## A. Task Family Guidance

### A1. Source Registration and Grounding Tasks
These tasks establish provenance, citation grounding, and source visibility.
They do not by themselves create training-approved content.

### A2. Reading and Understanding Tasks
These tasks help a user interpret a paper, organize key ideas, and connect a paper to code or implementation decisions.
They may become training candidates only when the outputs are user-authored or project-authored non-replicative artifacts with clear grounding.

### A3. Analysis and Comparison Tasks
These tasks compare methods, classify related work, identify limitations, or structure tradeoffs.
They require explicit paper grounding and should avoid reproducing long paper passages.

### A4. Planning and Critique Tasks
These tasks create experiment plans, reproduction plans, rebuttal plans, critique drafts, and failure-mode analyses.
They may become training candidates only when they are clearly project-authored or user-authored analytical outputs rather than copied source text.

### A5. Blocked Transformations
The following remain blocked in E1 and E1.R1:
- bulk ingest of raw paper full text into formal corpus paths
- quote-heavy pseudo-summaries that mostly restate original text
- fabricated citations or fabricated grounding claims
- ungrounded related-work, method, or experiment statements presented as sourced facts

## B. Standard `task_name` Records

### 1. `paper_reading_note`
- purpose: capture concise reading notes about a paper for future retrieval or review
- input source: registered paper record, user-provided notes, optional reviewed RAG references
- output format: note entry, bullet summary, or compact markdown note
- citation/source_id requirement: must reference `paper_id` or an equivalent registered source identifier
- can_be_training_candidate: true only when the output is user-authored or project-authored note text that does not reproduce long source passages

### 2. `contribution_extraction`
- purpose: identify the main claimed contributions of a paper in normalized form
- input source: registered paper record, user-provided notes, optional reviewed abstract or reviewed summary
- output format: contribution bullets, contribution table row, or structured JSON-like summary
- citation/source_id requirement: must reference `paper_id` and should stay tied to a registered source or note record
- can_be_training_candidate: true only when the extraction is a grounded project-authored structured summary rather than copied prose

### 3. `method_summary`
- purpose: summarize the method at a structured level for later lookup or review
- input source: registered paper record, user notes, reviewed summary notes, optional reviewed RAG references
- output format: short structured method summary, table row, or checklist
- citation/source_id requirement: must reference `paper_id` and cite the source record internally
- can_be_training_candidate: true when the summary is non-replicative, grounded, and review-approved

### 4. `method_comparison`
- purpose: compare two or more methods across assumptions, components, or tradeoffs
- input source: two or more registered paper records, user notes, reviewed summaries
- output format: comparison table, contrast bullets, or analytical note
- citation/source_id requirement: must reference every compared `paper_id`
- can_be_training_candidate: true only for project-authored or user-authored comparative analysis with explicit source grounding

### 5. `related_work_classification`
- purpose: classify a paper into a related-work grouping, theme, or methodology bucket
- input source: registered paper record, paper list, reviewed metadata, optional user notes
- output format: label set, taxonomy row, or grouped related-work note
- citation/source_id requirement: must reference `paper_id` and the classification source context
- can_be_training_candidate: true only for compact project-authored labels or summaries that avoid copying source prose

### 6. `experiment_design`
- purpose: propose an experiment design inspired by grounded paper context
- input source: registered paper record, user notes, reviewed method summaries, optional RAG references
- output format: experiment plan, checklist, parameter table, or evaluation outline
- citation/source_id requirement: must reference the motivating `paper_id` values or user-note source IDs
- can_be_training_candidate: true only when framed as project-authored planning rather than a reproduced experiment section

### 7. `ablation_planning`
- purpose: define ablation ideas, axes, and controls related to a grounded paper method
- input source: registered paper record, user notes, reviewed method summaries
- output format: ablation matrix, checklist, or planning note
- citation/source_id requirement: must reference the relevant `paper_id`
- can_be_training_candidate: true only when the content is analytical planning authored by the project or user

### 8. `limitation_detection`
- purpose: identify limitations, caveats, or uncertainty areas in a grounded paper or note set
- input source: registered paper record, user notes, reviewed summaries, optional RAG references
- output format: limitation bullets, risk note, or structured critique row
- citation/source_id requirement: must reference the relevant `paper_id` and keep claims grounded
- can_be_training_candidate: true only for grounded analytical outputs that do not fabricate evidence or reproduce long passages

### 9. `reviewer_critique`
- purpose: draft a reviewer-style critique grounded in a paper record or note set
- input source: registered paper record, user notes, reviewed summary artifacts
- output format: critique bullets, review outline, or structured review card
- citation/source_id requirement: must reference the relevant `paper_id` or note source and keep claims traceable
- can_be_training_candidate: true only when clearly marked as project-authored critique derived from grounded source context

### 10. `rebuttal_planning`
- purpose: outline possible rebuttal directions to a grounded critique or limitation set
- input source: registered paper record, critique notes, user notes, reviewed summaries
- output format: rebuttal plan, evidence checklist, or response outline
- citation/source_id requirement: must reference the related `paper_id` and critique source context
- can_be_training_candidate: true only for grounded planning artifacts, not for fabricated claims of experimental support

### 11. `abstract_revision`
- purpose: revise or tighten an abstract while staying grounded in existing registered source context or user-authored notes
- input source: registered paper record, user-authored draft abstract, reviewed notes
- output format: revised abstract draft, sentence-level rewrite, or revision checklist
- citation/source_id requirement: must reference the relevant `paper_id` or note source when the revision claims grounding
- can_be_training_candidate: true only when the revised text is a project-authored or user-authored derivative and not copied paper prose

### 12. `introduction_logic_chain`
- purpose: structure the motivation-to-problem-to-method logic chain for a paper or paper set
- input source: registered paper record, user notes, reviewed summaries, optional related-work grouping
- output format: logic outline, argument chain bullets, or section scaffold
- citation/source_id requirement: must reference the relevant `paper_id` values or note source IDs
- can_be_training_candidate: true only when the output is a project-authored analytical structure rather than copied introduction text

### 13. `citation_grounding_check`
- purpose: verify that claims, references, and cited identifiers are grounded in registered records or user-provided notes
- input source: registered paper records, draft outputs, user notes, reviewed citation lists
- output format: pass/fail checklist, grounding report, or issue list
- citation/source_id requirement: must reference the checked `paper_id` set or note source IDs explicitly
- can_be_training_candidate: false unless reduced to compact project-authored review metadata that contains no copied paper text

### 14. `paper_to_code_explanation`
- purpose: explain how a grounded paper idea maps to code, implementation concepts, or engineering components
- input source: registered paper record, user notes, reviewed method summaries, local project code context
- output format: explanation note, mapping table, or implementation guide
- citation/source_id requirement: must reference the relevant `paper_id` and any code context used
- can_be_training_candidate: true only for grounded project-authored explanations that avoid copying paper passages

### 15. `reproduction_plan`
- purpose: create a plan for reproducing a grounded paper result or method locally
- input source: registered paper record, user notes, reviewed summaries, local project constraints
- output format: reproduction checklist, dependency plan, or staged execution note
- citation/source_id requirement: must reference the relevant `paper_id` and any supporting notes
- can_be_training_candidate: true only as project-authored planning text with explicit source grounding

### 16. `failure_mode_analysis`
- purpose: analyze possible failure modes, weak assumptions, or breakdown conditions for a grounded paper method
- input source: registered paper record, user notes, reviewed summaries, optional comparison notes
- output format: failure-mode table, risk analysis note, or structured critique
- citation/source_id requirement: must reference the relevant `paper_id` or note source context
- can_be_training_candidate: true only for grounded analytical outputs that remain non-replicative and review-approved
