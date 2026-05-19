# E1 User Paper Drop Instructions

## 1. Purpose
These instructions tell the user where to place paper materials for the research paper assistant workflow without accidentally mixing raw source files into the formal training corpus.

## 2. Where To Put Things
Use:
- `data/research_papers/inbox/raw_papers/` for PDFs or source paper files
- `data/research_papers/inbox/paper_lists/` for paper lists, reading queues, URLs, BibTeX snippets, or small text manifests

Use:
- `data/research_papers/metadata/` only for compact metadata and registry files

Do not put paper full text into:
- `data/real_corpus/raw/synthetic_expanded/`
- `data/real_corpus/processed/`

## 3. What To Include With A Paper Drop
Helpful fields to provide when possible:
- title
- authors
- year
- venue
- link or citation
- why the paper matters
- whether you want RAG use, reading help, reproduction help, or future corpus derivation planning

## 4. What Happens Next
After a paper drop, the framework should:
1. register the source in `paper_source_registry.jsonl`
2. assign or confirm a `paper_id`
3. record license and use-scope status
4. keep the paper inbox-only until a later reviewed step creates derived artifacts

## 5. Important Safety Rules
Default assumptions:
- the paper is not training-approved
- raw full text stays source-library only unless later review says otherwise
- long paper passages should not be copied into candidate training corpora
- uncertain licensing must stay explicit in metadata

## 6. Small Example
Example drop pattern:
- place `attention_is_all_you_need.pdf` in `data/research_papers/inbox/raw_papers/`
- create or update a metadata record with a local `paper_id`
- later add user notes or project-authored method summaries in reviewed derived paths
