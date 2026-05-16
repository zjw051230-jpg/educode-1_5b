# D12.10 External General Text Intake Review

## 1. Purpose
The purpose of D12.10 is to review the D12.9 `external_general_text` intake outputs for the controlled Project Gutenberg Alice sample and decide whether they can be approved for limited tokenizer retraining and bounded mixed-corpus experiments.

## 2. Reviewed Input
Reviewed source:
- `source_id`: `external_general_text_project_gutenberg_000001`
- `candidate_id`: `candidate_pg_0001`
- `title`: `Alice's Adventures in Wonderland`
- `author`: `Lewis Carroll`
- `source_category`: `external_general_text`
- `project_role`: `supplement_only_not_project_backbone`
- `raw_path`: `data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice/alice_pg11_raw.txt`
- `source_note_path`: `data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice/SOURCE.md`

Reviewed processed outputs:
- `data/real_corpus/processed/external_general_text.processed.jsonl`
- `data/real_corpus/splits/external_general_text.train.jsonl`
- `data/real_corpus/splits/external_general_text.val.jsonl`
- `data/real_corpus/metadata/external_general_text.intake_summary.json`
- `data/real_corpus/metadata/external_general_text.dropped_files.jsonl`

## 3. Processed Outputs
Observed output summary:
- `processed_docs = 12`
- `train_docs = 11`
- `val_docs = 1`
- `dropped_files = 1`
- `total_processed_characters = 143929`
- `header_footer_removed_in_processed = true`

No token estimate was precomputed in the D12.9 outputs.

## 4. Provenance Check
Provenance checks passed:
- all processed records use `source_category = external_general_text`
- all processed records use `candidate_id = candidate_pg_0001`
- metadata retains:
  - `title`
  - `author`
  - `landing_page`
  - `raw_path`
  - `source_note_path`
- the raw Gutenberg text remains unchanged
- the adjacent `SOURCE.md` remains present beside the raw file

Conclusion:
- processed outputs retain provenance correctly
- raw source tracking remains intact

## 5. Header/Footer Handling
The raw Gutenberg file still preserves the original Project Gutenberg source and terms text.

The processed outputs:
- exclude Gutenberg header/footer text from training-oriented records
- record that fact through `header_footer_removed_in_processed = true`
- retain a dropped-entry record for the excluded front matter before the first chapter

Conclusion:
- raw text remains unchanged
- processed text removed Gutenberg header/footer and records that fact

## 6. JSONL Check
JSONL validation on:
- `external_general_text.processed.jsonl`
- `external_general_text.train.jsonl`
- `external_general_text.val.jsonl`

Result:
- `jsonl ok`

Conclusion:
- the processed and split review artifacts are structurally valid JSONL

## 7. Secret Scan Result
Secret-scan review was run in two parts:
- credential-style patterns: `api_key | password | private_key | sk-`
- content-word patterns: `secret | token`

Observed result:
- no credential-style secret hits
- one ordinary literary body-text hit on the word `secret`
- classification: `explanatory/license-only`

Conclusion:
- no real secrets found

## 8. Approval Decision
Decision:
- D12.9 `external_general_text` intake is accepted
- the processed outputs are approved only as a small external general text supplement
- the outputs are allowed for tokenizer retraining and bounded mixed-corpus experiments
- this approval does not allow the Gutenberg supplement to redefine the project backbone
- this review is not evidence of model quality

Approval scope:
- `small external general text supplement only`
- permitted for later tokenizer retraining
- permitted for later bounded mixed-corpus experiments
- not permitted to replace the CS / ML / Python / Transformer training-systems project backbone

## 9. Guardrails
- no new external data is approved by this step
- no additional Gutenberg files are approved by this step
- no tokenizer training is run in this step
- no model training is run in this step
- no model code is modified in this step
- `external_general_text` remains separate from `synthetic_expanded`
- later training reports must continue to distinguish the educational-domain backbone from this supplement

## 10. Next Step
Recommended next step:
- use the now-reviewed `external_general_text` supplement only in explicitly bounded future tokenizer retraining or mixed-corpus planning steps, while preserving source-category separation and keeping the supplement subordinate to the project backbone.
