# D12.9 External General Text Intake

## 1. Purpose
The purpose of D12.9 is to run a controlled `external_general_text` intake for the already downloaded `candidate_pg_0001` Project Gutenberg sample and produce processed review artifacts without approving tokenizer training, model training, or corpus mixing in this step.

## 2. Input Raw Source
Processed source:
- `candidate_id`: `candidate_pg_0001`
- `title`: `Alice's Adventures in Wonderland`
- `author`: `Lewis Carroll`
- `source_id`: `external_general_text_project_gutenberg_000001`
- `source_category`: `external_general_text`
- `project_role`: `supplement_only_not_project_backbone`
- `raw_path`: `data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice/alice_pg11_raw.txt`
- `source_note_path`: `data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice/SOURCE.md`

## 3. Processing Method
The intake script:
- validates the manifest, candidate record, raw file, and `SOURCE.md`
- keeps the raw file unchanged
- normalizes line endings
- strips trailing whitespace
- preserves paragraph boundaries
- removes empty sections
- segments the text into chapter-level documents
- assigns deterministic train/val splits with seed `1337`

Implementation path:
- `scripts/intake_external_general_text.py`

## 4. Header/Footer Handling
The raw Gutenberg file remains unchanged.

For processed review outputs only:
- Project Gutenberg header/footer markers were detected
- text before the first chapter and after the Gutenberg footer boundary was excluded from processed review text
- `header_footer_removed_in_processed = true` was recorded in output metadata and manifest state

## 5. Outputs
Generated outputs:
- `data/real_corpus/processed/external_general_text.processed.jsonl`
- `data/real_corpus/splits/external_general_text.train.jsonl`
- `data/real_corpus/splits/external_general_text.val.jsonl`
- `data/real_corpus/metadata/external_general_text.dropped_files.jsonl`
- `data/real_corpus/metadata/external_general_text.intake_summary.json`

Processed record fields include:
- `id`
- `source_id`
- `candidate_id`
- `source_category`
- `split`
- `text`
- `metadata.title`
- `metadata.author`
- `metadata.landing_page`
- `metadata.raw_path`
- `metadata.source_note_path`
- `metadata.header_footer_removed_in_processed`
- `metadata.project_role`

## 6. Train/Val Split
Observed split result:
- `processed_docs = 12`
- `train_docs = 11`
- `val_docs = 1`

The split is document-level and deterministic.
At least one validation document was retained.

## 7. Secret Scan Result
Secret-scan checks run against the processed and split JSONL outputs found:
- `result = explanatory/license-only`

The only observed match was a benign literary use of the word `secret` inside the book text.
No real secret-like content was detected in the emitted review artifacts.

## 8. Manifest Status
Manifest state after D12.9:
- `approval_status = processed_pending_training_approval`
- `processed_file_count = 12`
- `train_docs = 11`
- `val_docs = 1`
- `header_footer_removed_in_processed = true`
- `allowed_for_training = false`
- `allowed_to_commit = true`
- `external_download = true`
- `data_added = true`

## 9. What It Does Not Do
D12.9 does not:
- download any new external data
- process any source other than the controlled Alice sample
- train a tokenizer
- train a model
- run model training
- modify model code
- mix `external_general_text` into `synthetic_expanded`
- change `allowed_for_training` to `true`

## 10. Next Step
Recommended next step:
- D12.10 review the processed `external_general_text` outputs and decide whether this source can be approved for later tokenizer/training inclusion while still keeping provenance separated from `synthetic_expanded`.
