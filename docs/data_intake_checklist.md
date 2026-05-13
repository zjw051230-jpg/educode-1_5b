# Data Intake Checklist

## 0. Source Decision Gate
- Do not intake files until a source decision record exists.
- Do not intake files until the user explicitly approves the source path.
- Do not intake private or unclear-license material.
- Record `source_category`, `approval_status`, `license_or_ownership`, `privacy_risk`, `expected_file_types`, `allowed_for_training`, and `allowed_to_commit`.
- Record `allowed_for_training` and `allowed_to_commit` separately.
- A source may be allowed for local training but not allowed for Git commit.

## 1. Before Adding Data
- Is the data user-created, public domain, or permissively licensed?
- Is the license recorded?
- Is the source recorded?
- Does it contain private data?
- Does it contain API keys or secrets?
- Is the file text/code/markdown/jsonl?
- Is it small enough for this phase?
- Should it be committed or kept local only?

## 2. Source Metadata
Each source must record:
- source_id
- source_type
- license
- path
- approved_for_training
- contains_private_data
- notes

## 3. Cleaning Checklist
- normalize line endings
- remove binary files
- remove secrets/API keys
- strip excessive whitespace
- preserve code indentation
- preserve useful markdown headings
- remove duplicated huge blocks
- keep multilingual/code/math text if relevant

## 4. Split Checklist
- split by document where possible
- default 90/10 train/val
- fixed seed
- no leakage
- validation set not used for training metrics

## 5. Git Safety Checklist
- do not commit large raw data by default
- do not commit private data
- do not commit secrets
- keep generated corpora ignored if large
- check git status before commit
- run secret scan before public release

## 6. Approval Rule
No data should be used for training unless it is explicitly approved for this project.
