# D3 Synthetic Expanded Intake / Cleaning

## 1. Purpose
The purpose of D3 is to implement and run a bounded intake / cleaning step for the project-authored expanded synthetic corpus only.

This step turns the D2.2 raw corpus batch into reusable processed artifacts for later tokenizer and dataset work, while staying inside the approved synthetic-only data boundary.

## 2. Files Processed
The D3 script reads only:
- `data/real_corpus/raw/synthetic_expanded/`
- `data/real_corpus/metadata/source_manifest.synthetic_expanded.jsonl`

The script processes recursive `.md`, `.txt`, and `.py` corpus files under `synthetic_expanded/`.

Observed result:
- candidate files: `15`
- processed docs: `15`
- dropped files: `0`

The root `data/real_corpus/raw/synthetic_expanded/README.md` is treated as directory metadata rather than corpus content and is not included in the processed dataset.

## 3. Outputs
Generated outputs:
- `data/real_corpus/processed/synthetic_expanded.processed.jsonl`
- `data/real_corpus/splits/synthetic_expanded.train.jsonl`
- `data/real_corpus/splits/synthetic_expanded.val.jsonl`
- `data/real_corpus/metadata/synthetic_expanded.dropped_files.jsonl`
- `data/real_corpus/metadata/synthetic_expanded.intake_summary.json`

Each processed JSONL entry includes:
- `id`
- `source_id`
- `source_path`
- `source_category`
- `split`
- `text`
- `metadata`

## 4. Train / Val Split
The split is document-level and deterministic.

Split policy used:
- seed: `1337`
- target ratio: `90/10`
- minimum validation documents: `1`

Observed result:
- train docs: `13`
- val docs: `2`

## 5. Secret Scan Result
The intake script applies a basic pattern-based secret scan during cleaning.

Scanned patterns:
- `api_key`
- `secret`
- `password`
- `private_key`
- `sk-`

Observed result:
- secret scan hits: `0`
- no real secrets detected

## 6. What It Does Not Do
This step does not:
- read user private files
- download data
- copy external corpora
- train a tokenizer
- train a model
- run training
- modify model code
- perform `git push`

## 7. Limitations
- the intake path is hard-bounded to the expanded synthetic corpus source only
- the secret scan is intentionally basic and pattern-based
- only `.md`, `.txt`, and `.py` are supported
- there is no deduplication or richer metadata extraction yet
- the corpus remains small synthetic educational data and should not be described as broad real-world training data

## 8. Next Step
Recommended next step:
- D4 train updated BPE tokenizer
