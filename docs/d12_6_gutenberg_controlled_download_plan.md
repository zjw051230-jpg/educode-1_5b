# D12.6 Gutenberg Controlled Download Command Plan

## 1. Purpose
The purpose of D12.6 is to create a controlled download plan for `candidate_pg_0001` without downloading body text and without approving training use.

## 2. Selected Candidate
- `candidate_id`: `candidate_pg_0001`
- `title`: `Alice's Adventures in Wonderland`
- `author`: `Lewis Carroll`
- `gutenberg_landing_page`: `https://www.gutenberg.org/ebooks/11`
- `source_category`: `external_general_text`
- `project_role`: `supplement only`

## 3. Final Terms Check Summary
- use landing page as canonical source reference
- avoid bulk scraping
- preserve Project Gutenberg source and terms notes
- check selected ebook header before intake
- non-U.S. jurisdiction status must be considered
- this project will only use this as a small general text supplement

## 4. Planned Raw Path
`data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice/`

## 5. Future Download Command Plan
This is a future command plan only and is not executed in D12.6.

```text
mkdir -p data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice
```

Manually open the landing page `https://www.gutenberg.org/ebooks/11`, enter the plain text download entry, and save the result as:

`data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice/alice_pg11_raw.txt`

At the same time, save a source note as:

`data/real_corpus/raw/external_general_text/project_gutenberg_small_sample/candidate_pg_0001_alice/SOURCE.md`

`SOURCE.md` should include:
- title
- author
- landing page
- access date
- terms notes
- whether Project Gutenberg license/header/footer retained
- local jurisdiction note
- decision

## 6. Required Post-Download Checks
After a future D12.7 download, the workflow must:
- inspect file header
- inspect Project Gutenberg license/header/footer
- check approximate size
- run secret scan
- confirm no private data
- update manifest
- keep `source_category` `external_general_text`
- do not mix into `synthetic_expanded`

## 7. Current Approval Status
- `approved_for_download`: `false`
- `allowed_for_training`: `false`
- `allowed_to_commit`: `false`
- `external_download`: `false`
- `data_added`: `false`

## 8. Next Step
Recommended next step:
- D12.7 manually download `candidate_pg_0001` small text sample and create `SOURCE.md`, then inspect before intake.
