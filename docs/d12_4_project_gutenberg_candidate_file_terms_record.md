# D12.4 Project Gutenberg Candidate File-Level Terms Record

## 1. Purpose
The purpose of D12.4 is to record a file-level planning review for three small-sample Project Gutenberg candidate works without downloading any body text.

## 2. Shared Source Notes
- Project Gutenberg external text is supplement only.
- Project backbone remains CS/ML/Python/Transformer training-systems education.
- Use landing page URLs rather than deep links.
- Terms and jurisdiction notes must be preserved.
- Current status is `reviewed_for_planning`, not downloaded.

## 3. Candidate Records
| candidate_id | title | author | gutenberg_landing_page | source_category | intended_use | terms_notes | jurisdiction_notes | current_decision |
|---|---|---|---|---|---|---|---|---|
| `candidate_pg_0001` | `Alice's Adventures in Wonderland` | `Lewis Carroll` | `https://www.gutenberg.org/ebooks/11` | `external_general_text` | `small general English text supplement for tokenizer diversity` | `planning review only; no text downloaded; preserve Project Gutenberg source/terms notes if later used` | `U.S. public-domain status must be checked from the selected ebook header; non-U.S. use requires local copyright review` | `reviewed_for_planning_not_downloaded` |
| `candidate_pg_0002` | `The Adventures of Sherlock Holmes` | `Arthur Conan Doyle` | `https://www.gutenberg.org/ebooks/1661` | `external_general_text` | `small general English prose supplement for tokenizer diversity` | `planning review only; no text downloaded; preserve Project Gutenberg source/terms notes if later used` | `U.S. public-domain status must be checked from the selected ebook header; non-U.S. use requires local copyright review` | `reviewed_for_planning_not_downloaded` |
| `candidate_pg_0003` | `Frankenstein; or, The Modern Prometheus` | `Mary Wollstonecraft Shelley` | `https://www.gutenberg.org/ebooks/84` | `external_general_text` | `small general English prose supplement for tokenizer diversity` | `planning review only; no text downloaded; preserve Project Gutenberg source/terms notes if later used` | `U.S. public-domain status must be checked from the selected ebook header; non-U.S. use requires local copyright review` | `reviewed_for_planning_not_downloaded` |

## 4. Approval State
Current approval state remains:
- `allowed_for_training` remains `false`
- `allowed_to_commit` remains `false`
- `data_added` remains `false`
- `external_download` remains `false`
- candidates are not approved for intake until D12.5

## 5. Next Step
Recommended next step:
- D12.5 select exactly one candidate for small text download approval and update the manifest only after final terms review.
