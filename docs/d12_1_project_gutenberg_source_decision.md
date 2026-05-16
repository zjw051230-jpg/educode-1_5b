# D12.1 Project Gutenberg Source Decision Record

## 1. Purpose
The purpose of D12.1 is to record Project Gutenberg as a candidate source for a small external/general text supplement without downloading any data.

This step is source review and planning only.
It does not acquire Gutenberg text, create a raw corpus, or allow automatic training use.

## 2. Source Candidate
- source_id: `external_general_text_project_gutenberg_000001`
- source_name: `Project Gutenberg small public-domain text sample`
- source_url: `https://www.gutenberg.org/`
- source_category: `external_general_text`
- intended_use: tokenizer diversity and small general-language supplement
- project_role: supplement only, not project backbone

## 3. Terms / License Notes
Recorded review notes:
- Project Gutenberg states that the vast majority of ebooks are public domain in the United States.
- Project Gutenberg terms warn that copyright status may differ outside the United States.
- Any future use must preserve source/terms notes and avoid misleading redistribution.
- If Project Gutenberg license or trademark references are removed from text, the remaining text may be unrestricted under U.S. intellectual property law according to Project Gutenberg license notes.
- This project will treat Gutenberg as a reviewed candidate, not automatically approved bulk data.

## 4. Decision
- decision: `candidate_approved_for_small_sample_planning`
- allowed_for_training: `pending_final_sample_review`
- allowed_to_commit: `pending_final_sample_review`
- redistribution_allowed: `pending_terms_review_per_selected_files`
- attribution_required: `likely yes / preserve source notes`
- privacy_risk: `low`
- external_download: `false` in D12.1

## 5. Planned Initial Scope
- target size: `1MB - 10MB`
- selected_files: `pending`
- use plain text only
- store raw under a separate `external_general_text` directory
- keep a separate manifest
- keep source category during processing

## 6. Guardrails
- no bulk scrape
- no unknown-license source
- no private data
- no medical / financial / legal domain shift
- no direct mixing into `synthetic_expanded`
- no training until source manifest and small-sample intake are complete

## 7. What D12.1 Does Not Do
D12.1 does not:
- download Gutenberg data
- create a raw external corpus
- train a tokenizer
- train a model
- enter A100

## 8. Next Step
Recommended next step:
- D12.2 create `external_general_text` directory skeleton and manifest placeholder, still without downloading data
