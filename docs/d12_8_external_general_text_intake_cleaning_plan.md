# D12.8 External General Text Intake / Cleaning Plan

## 1. Purpose
The purpose of D12.8 is to define a controlled intake and cleaning plan for the already downloaded `candidate_pg_0001` Project Gutenberg sample without running intake, without creating processed JSONL outputs, and without approving training use in this step.

## 2. Current Raw Source
Current inspected source:
- `candidate_id`: `candidate_pg_0001`
- `title`: `Alice's Adventures in Wonderland`
- `author`: `Lewis Carroll`
- `source_category`: `external_general_text`
- `project_role`: `supplement_only_not_project_backbone`
- `raw_local_path`: `data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice/alice_pg11_raw.txt`
- `source_note_path`: `data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice/SOURCE.md`
- `approval_status`: `downloaded_pending_intake_review`
- `allowed_for_training`: `false`
- `allowed_to_commit`: `true`
- `external_download`: `true`
- `data_added`: `true`

The raw file currently retains the Project Gutenberg header and footer exactly as downloaded in D12.7.

## 3. Project Backbone Constraint
EduCode-1.5B remains a CS / ML / Python / Transformer training-systems educational project.

This means:
- `external_general_text` remains a small supplement only
- the downloaded Gutenberg sample must not replace the `synthetic_expanded` educational backbone
- future tokenizer and training reports must continue to distinguish `synthetic_domain` inputs from any `external_general_text` inputs

## 4. Raw vs Processed Policy
The raw Project Gutenberg file and its adjacent `SOURCE.md` are provenance artifacts and should remain unchanged.

A later intake step should therefore:
- read from the raw file
- preserve the raw file exactly as downloaded
- write cleaned content only to separate processed outputs
- keep all external-general-text outputs separate from `synthetic_expanded`

Planned future output lineage:
- raw input: `data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice/alice_pg11_raw.txt`
- processed output: `data/real_corpus/processed/external_general_text.processed.jsonl`
- train split: `data/real_corpus/splits/external_general_text.train.jsonl`
- val split: `data/real_corpus/splits/external_general_text.val.jsonl`

## 5. Header/Footer Handling Plan
The raw file should keep the original Project Gutenberg source and terms text.

A later intake implementation should remove Project Gutenberg boilerplate only in processed training-oriented text.

Preferred handling rule:
- if explicit `*** START OF THE PROJECT GUTENBERG EBOOK ... ***` and `*** END OF THE PROJECT GUTENBERG EBOOK ... ***` markers are present, use them as the default trimming boundaries
- preserve the original raw file unchanged even when processed text is trimmed
- record in processed metadata that header/footer removal was applied
- if the markers are missing, ambiguous, or inconsistent, stop for manual review instead of guessing

## 6. Planned Outputs
A future controlled intake step should produce only the following external-general-text artifacts:
- `data/real_corpus/processed/external_general_text.processed.jsonl`
- `data/real_corpus/splits/external_general_text.train.jsonl`
- `data/real_corpus/splits/external_general_text.val.jsonl`

These outputs should contain cleaned text segments derived only from the selected Gutenberg sample.

No future output should be written into `synthetic_expanded` paths.

## 7. Split Plan
Because the current approved raw source is a single book-sized text file, train/val splitting should avoid leakage from adjacent or overlapping text spans.

Recommended split strategy:
- segment the cleaned text into logical units before splitting
- prefer chapter-level segmentation when chapter headings are available
- if later chunking is needed, keep all chunks from the same chapter in the same split
- use a deterministic split seed of `1337`
- target a small held-out validation share while ensuring that the validation set contains whole held-out sections rather than overlapping windows from training sections
- if reliable section boundaries cannot be found, stop for manual review rather than creating a noisy random split

## 8. Manifest Update Plan
D12.8 does not change the manifest state.

A later successful intake step should update manifest or metadata bookkeeping to record:
- processed output path
- train split path
- val split path
- whether header/footer removal was applied in processed text
- whether post-cleaning secret scan checks passed
- the next approval state after intake review

Even after intake, `allowed_for_training` should remain `false` until a separate review explicitly approves the processed external text for training use.

## 9. Guardrails
- only the already downloaded `candidate_pg_0001` file may be considered
- no new Gutenberg files may be downloaded in this step
- no raw text may be edited in place
- no processed external text may be mixed into `synthetic_expanded`
- no tokenizer training may run in this step
- no model training may run in this step
- no approval state may be upgraded to training-ready in this step
- provenance and source notes must remain preserved beside the raw file

## 10. What D12.8 Does Not Do
D12.8 does not:
- run intake
- clean the raw text
- create processed JSONL outputs
- create train/val split JSONL files
- modify the raw downloaded file
- change `allowed_for_training` to `true`
- train a tokenizer
- train a model
- mix external text into `synthetic_expanded`

## 11. Next Step
Recommended next step:
- D12.9 implement and run a controlled `external_general_text` intake script for the single downloaded Gutenberg sample, then review the processed outputs before any training approval.
