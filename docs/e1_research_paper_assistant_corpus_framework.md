# E1 Research Paper Assistant Corpus Framework

## 1. Purpose
E1 creates the initial repository framework for a research paper assistant corpus line.

This step is framework only.
It does not download papers, parse paper full text, run intake, train tokenizers, train models, or modify model code.

## 2. Problem Statement
The project now needs a safe way to accept user-provided research papers and paper lists while preserving a strict boundary between:
- source-library materials
- RAG-oriented materials
- reviewable derived artifacts
- formal training-candidate materials

Without that boundary, raw paper text could be mixed into the training pipeline without clear license or provenance review.

## 3. Directory Structure
E1 introduces:
- `data/research_papers/`
- `data/research_papers/inbox/`
- `data/research_papers/inbox/raw_papers/`
- `data/research_papers/inbox/paper_lists/`
- `data/research_papers/metadata/`
- `data/research_papers/derived/`
- `data/research_papers/draft_queue/`
- `data/research_papers/rag_library/`

Intended roles:
- `inbox/raw_papers/` stores user-provided source files and remains Git-ignored for large raw content
- `paper_lists/` stores small reviewable lists or manifests
- `metadata/` stores provenance and usage-control records
- `derived/` stores reviewed project-authored transformations
- `draft_queue/` stores review-only candidate assistant artifacts
- `rag_library/` stores retrieval-oriented organization outputs

## 4. Policy Boundary
Core E1 boundary:
- paper full text is source material by default, not training material

Allowed future training-candidate categories are limited to:
- open-license full text with confirmed terms
- user-authored notes
- project-authored non-replicative structured outputs
- metadata, abstracts, citations, and method summaries

Blocked behavior includes:
- copying unreviewed paper full text into formal corpus paths
- converting long paper passages directly into training text
- recording misleading licensing or provenance claims

## 5. Metadata Layer
E1 adds a paper-source registry and template record so every paper can carry:
- stable identity
- source path
- citation
- license status
- use scope
- training eligibility state
- content-state flags
- review status

This allows later steps to reason explicitly about what a paper may be used for.

## 6. Task Taxonomy
E1 distinguishes several later task families:
- source registration
- RAG indexing and lookup
- user-authored notes
- project-authored structured derivations
- review-only assistant draft generation

This taxonomy matters because not every useful paper workflow should become a training-data workflow.

## 7. Git and Repository Guardrail
E1 updates `.gitignore` so raw paper files under:
- `data/research_papers/inbox/raw_papers/`

remain excluded from commits by default, while `.gitkeep` can preserve the directory skeleton.

## 8. Result of This Step
After E1:
- the repository has a dedicated research-paper intake skeleton
- raw paper inbox handling is separated from formal corpus paths
- metadata and policy scaffolding exist for later reviewable paper workflows
- no paper full text has been promoted into the training corpus
- no intake or training stage has been run

## 9. Recommended Next Step
Recommended next step after E1:
- register a small number of user-provided paper records in the metadata registry
- keep them inbox-only
- then discuss a narrow E2 step for reviewed derived-note or method-summary generation without copying raw full text into the formal corpus
