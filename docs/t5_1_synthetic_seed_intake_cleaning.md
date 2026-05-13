# T5.1 Synthetic Seed Intake / Cleaning

## 1. Purpose
The purpose of T5.1 is to implement a minimal intake and cleaning script for the project-authored synthetic seed corpus only.

This step turns the earlier T5 planning document into a bounded executable path for:
- manifest-gated intake
- text cleaning
- deterministic document-level train/validation split generation
- processed output writing
- lightweight audit output

## 2. Files Added
- `scripts/intake_synthetic_seed_corpus.py`
- `data/real_corpus/processed/synthetic_seed.processed.jsonl`
- `data/real_corpus/splits/synthetic_seed.train.jsonl`
- `data/real_corpus/splits/synthetic_seed.val.jsonl`
- `data/real_corpus/metadata/synthetic_seed.dropped_files.jsonl`
- `data/real_corpus/metadata/synthetic_seed.intake_summary.json`

## 3. Script Behavior
The script:
- reads only `data/real_corpus/raw/synthetic_seed/`
- reads `data/real_corpus/metadata/source_manifest.synthetic_seed.jsonl`
- verifies `source_id = source_synthetic_seed_000001`
- verifies `allowed_for_training = true`
- verifies `privacy_risk = none`
- processes only `.md`, `.txt`, and `.py` files in the synthetic seed directory
- normalizes line endings
- strips trailing whitespace
- preserves code indentation by avoiding left-strip normalization
- skips empty files after cleaning
- scans for basic secret-like patterns including `api_key`, `secret`, `password`, `private_key`, and `sk-`
- writes processed JSONL output
- creates a deterministic document-level split with seed `1337`
- keeps at least one validation document when the corpus is small
- records dropped files in a separate JSONL file
- writes a lightweight intake summary JSON file

## 4. Outputs
Generated outputs:
- `data/real_corpus/processed/synthetic_seed.processed.jsonl`
- `data/real_corpus/splits/synthetic_seed.train.jsonl`
- `data/real_corpus/splits/synthetic_seed.val.jsonl`
- `data/real_corpus/metadata/synthetic_seed.dropped_files.jsonl`
- `data/real_corpus/metadata/synthetic_seed.intake_summary.json`

Each processed JSONL entry includes:
- `id`
- `source_id`
- `source_path`
- `source_category`
- `split`
- `text`
- `metadata`

## 5. Validation Result
Observed result from the T5.1 run:
- processed docs: `8`
- train docs: `7`
- val docs: `1`
- dropped files: `0`
- secret scan hits: `0`

The script completed successfully and all expected output files were created.

## 6. What It Does Not Do
This step does not:
- read any repo directory outside the synthetic seed corpus input path and its manifest/output targets
- download data
- scan user private files
- train a tokenizer
- train a model
- run training
- install packages
- perform `git push`

## 7. Current Limitations
- the script is hard-bounded to the synthetic seed corpus only
- the secret scan is intentionally basic and pattern-based
- only `.md`, `.txt`, and `.py` are supported
- there is no deduplication stage yet
- there is no richer metadata extraction beyond minimal audit fields
- the corpus is synthetic and too small to represent real training data behavior

## 8. Next Step
Recommended next step:
- T5.2 BPE 8k tokenizer training plan
- or T6 validation loop plan
