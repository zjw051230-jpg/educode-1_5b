# T5 Real Data Intake / Cleaning Script Plan

## 1. Purpose
The purpose of T5 is to define the future intake and cleaning script for the EduCode real-data path.

This step stays at the planning level only.
It does not implement the script, does not run any processing, and does not start training.

## 2. Current Input Scope
The first planned input target is:
- `data/real_corpus/raw/synthetic_seed/`

This keeps the first intake and cleaning design bounded to a safe, project-authored seed corpus before wider real-data intake is introduced.

## 3. Planned Script Responsibilities
The future cleaning script should:
- read from `data/real_corpus/raw/synthetic_seed/`
- check the source manifest before processing
- scan allowed `.md`, `.txt`, and `.py` files
- normalize text safely
- preserve code indentation
- remove secrets and API keys
- write processed JSONL output
- generate train/validation split files
- record dropped files and the reasons they were dropped

## 4. Intake Validation Steps
Before processing files, the future script should verify:
- the source manifest exists
- the source is approved for training
- the source path matches the manifest entry
- the file extension is allowed
- the file is text-like rather than binary
- the file does not exceed early-stage size expectations without explicit approval

## 5. Cleaning Rules
The future cleaning stage should apply these rules:
- normalize line endings
- strip excessive trailing whitespace
- preserve useful markdown headings
- preserve code blocks and code indentation
- keep multilingual technical text when relevant
- remove obvious secrets, tokens, and API keys
- remove empty files or effectively empty files
- record files that are skipped or dropped

## 6. Processed Output Plan
The future processed output should be JSONL under the processed corpus area.

Each processed entry should include:
- document id
- source id
- split
- cleaned text
- minimal metadata needed for auditability

## 7. Split Generation Plan
The future script should:
- create a default 90/10 train/validation split
- prefer document-level split over token-level random slicing
- keep the validation set fixed once created
- record the split seed
- avoid train/validation leakage

## 8. Logging and Audit Trail
The future script should emit a lightweight audit trail including:
- processed file count
- dropped file count
- dropped file reasons
- output paths
- split seed
- manifest source id

## 9. What T5 Does Not Do
This step does not:
- implement the cleaning script
- run file processing
- run training
- train a tokenizer
- download data
- install packages
- execute `git push`

## 10. Recommended Next Step
Recommended next step:
- T5.1: implement a minimal intake/cleaning script for the synthetic seed corpus only

That follow-up should still stay bounded:
- synthetic seed corpus only
- no external downloads
- no model training
- no tokenizer training
