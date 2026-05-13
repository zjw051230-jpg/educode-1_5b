# T4.1 First Approved Local Corpus Source Decision

## 1. Purpose
The purpose of T4.1 is to move from the T4 data intake structure into the first approved local corpus source decision stage.

This step does not:
- copy real data into the repo
- download external data
- read the contents of private user files

This step only defines the approval rule and metadata recording method for the first source candidates.

## 2. Source Review Schema
The source review schema for first-source decisions must record these seven core fields:
- `source_category`
- `approval_status`
- `license_or_ownership`
- `privacy_risk`
- `expected_file_types`
- `allowed_for_training`
- `allowed_to_commit`

Why they matter:
- `allowed_for_training` and `allowed_to_commit` must be recorded separately
- a source may be allowed for local training while still not being allowed for Git commit
- `approval_status` must never default to approved; explicit user approval is required before intake

## 3. Recommended First Source
Recommended first source type:
- user-created local study notes / hand-written CS-ML-code examples

Why this is the recommended first source:
- ownership is clear
- license risk is low
- it is aligned with the EduCode theme
- it is sufficient for a first small real-data pipeline test
- it is easier to clean and audit than downloaded sources

Important limit:
- this step does not require placing any file into the repo
- only files or folders explicitly named and approved by the user should enter a later intake step

## 4. Candidate Source Categories

### Candidate A: User-created CS / ML notes
Status: recommended first source

Pros:
- user-owned
- low legal risk
- aligned with model theme

Risks:
- may contain personal paths or names
- may be small or stylistically narrow

Approval requirement:
- user must explicitly approve the source path before intake

### Candidate B: User-created Python/code snippets
Status: recommended secondary source

Pros:
- useful for code token patterns
- aligned with EduCode

Risks:
- may contain local paths or secrets
- requires secret scan before use

Approval requirement:
- user approval and secret scan before intake

### Candidate C: Public domain / permissive educational text
Status: later source

Pros:
- more realistic text
- scalable

Risks:
- requires license review

Approval requirement:
- source URL and license must be recorded before use

### Candidate D: Synthetic educational examples
Status: optional supplement

Pros:
- controllable
- useful for format diversity

Risks:
- synthetic distribution differs from real local data
- should not be described as real web data

Approval requirement:
- generation method must be documented

## 5. First Source Decision
Current decision:
- `first_source_type`: `user_created_local_notes`
- `approval_status`: `pending_user_source_selection`
- `data_added_to_repo`: `no`
- `external_download`: `no`
- `training_allowed`: `not yet`
- `commit_raw_data`: `not decided`
- `next_action`: user chooses one small approved folder or file set

## 6. Source Selection Requirements
Before any file is used, record:
- `source_id`
- `local_path`
- `source_category`
- `approval_status`
- `license_or_ownership`
- `privacy_risk`
- `expected_file_types`
- `allowed_for_training`
- `allowed_to_commit`
- `contains_private_data`
- `contains_secrets`
- `size_estimate`
- `notes`

## 7. Safety Rules
Safety rules for the first approved local source:
- no private credentials
- no API keys
- no private chats unless explicitly approved
- no copyrighted PDFs, books, or course packs without permission
- no unclear-license downloaded datasets
- no large raw data committed by default
- run secret scan before public release

## 8. What T4.1 Does Not Do
This step does not:
- copy real data
- create corpus content
- download data
- write a cleaning script
- train a tokenizer
- train a model
- modify configs
- execute `git push`

## 9. Recommended Next Step
Recommended next step:
- T4.2: Approved Local Source Manifest

T4.2 requires the user to provide one explicit approved path, for example:
- a small markdown/txt/python folder
- user-written study notes
- a small sample set explicitly allowed for this project
