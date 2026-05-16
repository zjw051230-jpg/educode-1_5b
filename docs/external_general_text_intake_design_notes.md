# External General Text Intake Design Notes

## 1. Input Raw Directory
Expected raw source directory:
- `data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice/`

Expected files:
- `alice_pg11_raw.txt`
- `SOURCE.md`

## 2. Expected Source Metadata
The intake step should verify and carry forward the following source information:
- `source_id`
- `source_category`
- `project_role`
- `candidate_id`
- `title`
- `author`
- `landing_page`
- `access_date`
- `raw_local_path`
- `source_note_path`
- `approval_status`

The adjacent `SOURCE.md` should remain the human-readable provenance note for the raw file.

## 3. Header/Footer Policy
Cleaning should operate on a processed copy only.

Recommended policy:
- keep the raw Gutenberg file unchanged
- prefer explicit Gutenberg `START` / `END` markers when trimming boilerplate
- do not rewrite book content beyond minimal whitespace normalization needed for structured JSONL output
- if trimming boundaries are unclear, stop for manual review

## 4. Output JSONL Schema
A future processed record can stay minimal and provenance-oriented.

Suggested fields:
- `doc_id`
- `source_id`
- `source_category`
- `project_role`
- `candidate_id`
- `title`
- `author`
- `raw_local_path`
- `source_note_path`
- `section_id`
- `section_title`
- `header_footer_removed`
- `text`

The train and val split JSONL files can reuse the same record structure.

## 5. Split Strategy
Because the current source is a single downloaded book, splitting should happen after logical section extraction.

Recommended strategy:
- detect chapter boundaries when possible
- emit one or more records per chapter or section
- keep all chunks derived from the same chapter in the same split
- assign splits deterministically with seed `1337`
- avoid overlapping train/val windows from the same local text neighborhood

## 6. Safety Checks
A future intake implementation should verify:
- the raw file exists
- `SOURCE.md` exists beside the raw file
- the manifest still points to the same selected candidate
- `source_category` remains `external_general_text`
- the output paths stay under external-general-text processed/split directories
- raw provenance is preserved
- post-cleaning outputs pass a secret scan before any later training approval

## 7. Non-Goals for the Intake Step
The future intake step should not:
- download additional files
- approve training automatically
- merge external text into `synthetic_expanded`
- train a tokenizer or model
