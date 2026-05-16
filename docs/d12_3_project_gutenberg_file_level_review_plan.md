# D12.3 Project Gutenberg File-Level Review Plan

## 1. Purpose
The purpose of D12.3 is to plan how a small number of Project Gutenberg files may be selected as an `external_general_text` supplement in a later step without downloading body text in this step.

This stage defines the review process only.
It does not download Project Gutenberg text.
It does not add raw text files to the repository.

## 2. Source Status
- `source_id`: `external_general_text_project_gutenberg_000001`
- `source_name`: `Project Gutenberg small public-domain text sample`
- `source_category`: `external_general_text`
- `project_role`: `supplement only`
- `data_added`: `false`
- `external_download`: `false`

## 3. Why File-Level Review Is Required
File-level review is required because:
- Project Gutenberg contains many U.S. public-domain texts, but each selected work should still be reviewed.
- Terms/use and jurisdiction notes must be recorded.
- We must avoid bulk scraping or unknown-license assumptions.
- We must keep the Gutenberg supplement separate from the domain synthetic corpus.

This review step helps distinguish source-level candidate approval from file-level intake approval.

## 4. Candidate Selection Criteria
Future candidate files should satisfy the following requirements:
- plain text format available
- small enough for a `1MB - 10MB` total sample
- no obvious copyright restriction note for the selected file
- no private/personal data
- suitable for general English language supplement
- source URL and access date recorded
- attribution/source notes preserved

## 5. Candidate Work List Placeholder
| candidate_id | title | author | gutenberg_url | plain_text_url | estimated_size | terms_notes | selected | reason |
|---|---|---|---|---|---|---|---|---|
| `candidate_pg_0001` | `pending` | `pending` | `pending` | `pending` | `pending` | `pending` | `no` | `pending` |
| `candidate_pg_0002` | `pending` | `pending` | `pending` | `pending` | `pending` | `pending` | `no` | `pending` |
| `candidate_pg_0003` | `pending` | `pending` | `pending` | `pending` | `pending` | `pending` | `no` | `pending` |

No concrete title should be filled in until it has been manually reviewed.

## 6. Approval States
Defined approval states for future candidate files:
- `candidate_only`
- `file_reviewed_not_downloaded`
- `approved_for_small_download`
- `downloaded_pending_intake`
- `processed_for_training`
- `rejected`

## 7. Manifest Update Rule
Only after a concrete file passes file-level review may the manifest be updated so that:
- `allowed_for_training` changes to `true`
- `allowed_to_commit` changes to `true` or `false` based on terms
- `selected_files` is updated with a concrete file list
- `data_added` changes to `true`

Until then, the external-general-text manifest remains a placeholder only.

## 8. Guardrails
- no bulk download
- no unknown-license files
- no external text in `synthetic_expanded`
- no training before intake
- no high-risk domain shift
- keep `external_general_text` separate

## 9. Next Step
Recommended next step:
- D12.4 manually select `1-3` candidate Gutenberg files and record file-level terms, still before download.
