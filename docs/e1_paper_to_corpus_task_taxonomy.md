# E1 Paper-to-Corpus Task Taxonomy

## 1. Purpose
This taxonomy defines the kinds of research-paper assistant tasks that may be built from paper sources while preserving the boundary between source material, RAG use, and possible training candidates.

## 2. Source-Library Tasks
These tasks operate on source awareness, not corpus promotion:
- paper registration
- citation normalization
- topic tagging
- reading-list assembly
- source completeness checks

Output examples:
- metadata records
- paper lists
- review dashboards

## 3. RAG-Oriented Tasks
These tasks support retrieval-style assistance:
- paper lookup by topic
- citation retrieval
- method-comparison note lookup
- experiment-setting lookup
- benchmark/result reference lookup

Output examples:
- indexed retrieval chunks
- citation cards
- method reference tables

Important constraint:
- RAG indexing does not automatically create training-approved text

## 4. User-Authored Note Tasks
These tasks transform user knowledge, not paper text, into reviewable artifacts:
- reading notes
- paper comparison notes
- reproduction checklists
- critique outlines
- question banks

These are stronger future training candidates than raw paper text because they are user-authored derivatives rather than copied source passages.

## 5. Project-Authored Structured Derivation Tasks
These tasks produce project-authored outputs constrained away from replication:
- method-summary tables
- terminology glossaries
- citation graphs
- benchmark taxonomy rows
- paper-to-concept mapping
- reproduction dependency checklists

Important rule:
- these outputs should compress, structure, or normalize knowledge rather than reproduce long source passages

## 6. Draft-Queue Candidate Tasks
These tasks may create future review-only assistant corpus items:
- paper discussion prompts
- reviewer-style critique prompts
- method tradeoff explanations
- experiment design quizzes
- reproduction troubleshooting scenarios

Before any such artifact can be promoted, it should:
- keep source provenance
- avoid long copied text
- record whether it depends on user notes, metadata, or reviewed summaries

## 7. Blocked Task Types
The following tasks are not allowed in E1:
- bulk ingest of raw paper full text into formal corpus paths
- quote-heavy pseudo-summaries that mainly restate original text
- license-obscured transformations
- fabricated citations or fabricated claims of open licensing

## 8. Recommended Future Review Order
Recommended later order:
1. metadata registration
2. user note collection
3. project-authored structured summary layer
4. RAG evaluation
5. draft assistant artifacts
6. only then discuss any formal training-candidate subset
