# D12 External / General Text Supplement Plan

## 1. Purpose
The purpose of D12 is to define a controlled plan for adding a small amount of external/general text as a supplement to the existing domain synthetic corpus.

The current domain synthetic corpus has already validated the tokenizer, data, model, loss, checkpoint, validation, and bounded local training pipeline, but it remains small.
D12 therefore plans a limited external/general text supplement to improve tokenizer coverage and language diversity without changing the project’s core identity.

## 2. Current Baseline
Current accepted baseline:
- domain synthetic corpus files = `45`
- train docs = `41`
- val docs = `4`
- domain BPE observed vocab = `3988`
- 50-step domain BPE training accepted
- 100-step domain BPE training accepted
- 100-step train loss lower but final validation loss higher
- conclusion: data scale and validation quality are the next bottleneck

## 3. Project Backbone Constraint
EduCode-1.5B remains a CS / ML / Python / Transformer training-systems educational domain model pipeline.

This means:
- external general text is only a supplement, not the project identity
- the external supplement must not replace the CS / ML educational domain corpus
- future tokenizer or training reports must continue to distinguish the educational-domain backbone from any general-text supplement

## 4. Candidate Supplement Type
The first supplement phase should consider only:
- a small public-domain or clearly permitted general English text sample
- target size: `1MB` to `10MB`
- purpose: tokenizer diversity and general language grounding
- not for claiming broad model capability

The first supplement phase should not consider:
- unknown-license web scrape
- copyrighted books, textbooks, or course PDFs
- private notes or chats
- medical, financial, or legal high-risk corpora
- large internet dumps

## 5. Source Review Requirements
Every external source must be recorded before any training use.

Each source record must include:
- `source_id`
- `source_name`
- `source_url`
- `source_category`
- `license_or_terms`
- `access_date`
- `selected_files`
- `raw_size_estimate`
- `allowed_for_training`
- `allowed_to_commit`
- `redistribution_allowed`
- `attribution_required`
- `privacy_risk`
- `jurisdiction_notes`
- `notes`

## 6. Intake Rules
Before any external text is allowed into tokenizer or training inputs, it must:
- live in a separate raw directory
- use a separate source manifest
- produce a separate processed JSONL
- produce a separate train/val split
- pass secret scan checks
- pass license/terms review
- avoid directly overwriting or replacing `synthetic_expanded`

This keeps provenance, reviewability, and later rollback straightforward.

## 7. Proposed Directory Plan
If a source is later approved, the following paths can be created:
- `data/real_corpus/raw/external_general_text/`
- `data/real_corpus/metadata/source_manifest.external_general_text.jsonl`
- `data/real_corpus/processed/external_general_text.processed.jsonl`
- `data/real_corpus/splits/external_general_text.train.jsonl`
- `data/real_corpus/splits/external_general_text.val.jsonl`

## 8. Integration Strategy
When future corpus or tokenizer work mixes multiple approved sources, source provenance must remain visible.

At minimum, later processing and reporting should preserve the following source categories:
- `synthetic_domain`
- `external_general_text`

Tokenizer training may combine the sources later, but milestone reports must continue to distinguish where the text came from and why it was included.

## 9. Guardrails
The supplement plan must preserve the following guardrails:
- no external data without manifest
- no unknown license
- no private data
- no high-risk medical / financial / legal domain shift
- no large data commit
- no model quality claim from a tiny supplement

## 10. Next Step
Recommended next step:
- D12.1 external general text source decision record

This still starts with source review and documentation first, not large downloads or direct corpus mixing.
