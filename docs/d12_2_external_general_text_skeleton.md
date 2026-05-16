# D12.2 External General Text Skeleton and Manifest Placeholder

## 1. Purpose
The purpose of D12.2 is to create the directory skeleton and manifest placeholder needed for a future external/general text intake path without downloading any external data.

This step prepares the repo structure only.
It does not add Project Gutenberg text or approve any external sample for training.

## 2. Directories Added
Created or populated paths:
- `data/real_corpus/raw/external_general_text/`
- `data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/`
- `data/real_corpus/metadata/source_manifest.external_general_text.jsonl`

Files added in the raw skeleton:
- `data/real_corpus/raw/external_general_text/README.md`
- `data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/.gitkeep`

No Project Gutenberg body text files were added.

## 3. Manifest Placeholder
Created placeholder manifest:
- `data/real_corpus/metadata/source_manifest.external_general_text.jsonl`

Current placeholder values explicitly record:
- `allowed_for_training = false`
- `allowed_to_commit = false`
- `data_added = false`
- `external_download = false`

This means the manifest exists only to reserve provenance structure for a future reviewed sample.

## 4. Current Approval Status
The current external-general-text path is not approved for training or data commit.

Current status:
- candidate source recorded earlier in D12.1
- directory skeleton now exists
- manifest placeholder now exists
- no external text has been downloaded
- no selected files have been approved

Only after D12.3 selects a concrete small sample and completes a file-level terms review should the approval flags be revisited.

## 5. What It Does Not Do
D12.2 does not:
- download Project Gutenberg data
- create any raw external text files beyond README/placeholder files
- create processed JSONL content
- create train/val split content
- train a tokenizer
- train a model
- run training

## 6. Guardrails
The current skeleton preserves the following guardrails:
- no external data without manifest
- no training approval without terms review
- no direct mixing into `synthetic_expanded`
- no assumption that candidate status equals training approval
- no data commit from the external path until a later step explicitly allows it

## 7. Next Step
Recommended next step:
- D12.3 select a concrete small Project Gutenberg sample candidate and complete a file-level terms review before any external text is downloaded or processed
