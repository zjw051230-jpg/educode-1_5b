# E1 Research Paper Source Policy

## 1. Purpose
The purpose of this policy is to define what kinds of research-paper material may enter the repository, what use scopes are allowed by default, and what remains blocked from formal training use.

## 2. Default Handling Rule
Default rule:
- research paper source files are treated as source-library material, not training corpus material

This default applies especially to:
- user-dropped PDFs
- copied paper full text
- exported article HTML or text
- scanned OCR output from papers

## 3. Allowed-by-Default Uses
Without extra approval, a paper source may be used for:
- source cataloging
- metadata recording
- citation tracking
- reading queues
- RAG-candidate organization
- user-authored notes linked back to the paper
- project-authored summaries that do not replicate long original passages

## 4. Blocked-by-Default Uses
Without explicit later review, a paper source may not be used for:
- copying unreviewed paper full text into `data/real_corpus/raw/synthetic_expanded/`
- converting long paper passages directly into training corpus text
- pretending a restricted or unclear paper is open-license
- mixing raw paper text into approved training corpora without provenance and policy review

## 5. Potentially Reviewable Training Inputs
Only the following kinds of content may later be considered for formal training review:
- open-license full text with confirmed terms
- user-authored notes
- project-authored non-replicative structured outputs
- metadata, abstracts, citations, taxonomy labels, and method summaries

Important rule:
- reviewable does not mean approved
- later formal review is still required before any promotion to a training corpus path

## 6. Provenance Requirement
Every paper-related artifact must remain traceable to its source record.
At minimum, preserve:
- `paper_id`
- source path
- title
- citation
- license status
- use scope

## 7. RAG vs Training Separation
`rag_library/` and formal training corpus paths serve different purposes:
- RAG storage is for retrieval-oriented access to source knowledge
- training corpus paths are for approved model-ingestion material

A paper may be acceptable for RAG but still disallowed for training.

## 8. Policy Integrity Rule
The project must not create false records such as:
- claiming only open data was used when restricted paper text was actually used
- calling copied excerpts "synthetic" when they are only light rewrites of original text
- omitting license uncertainty from metadata

## 9. What This Policy Does Not Do
This policy does not:
- download papers
- parse PDFs
- make legal determinations beyond recording reviewed status
- approve downstream intake or training
