# D8 Synthetic Expanded 45-File Intake

## 1. Purpose
The purpose of D8 is to re-run the expanded synthetic corpus intake so the processed, train, and validation outputs reflect the approved 45-file `synthetic_expanded` source created through D7.

## 2. Input Corpus
- input root: `data/real_corpus/raw/synthetic_expanded/`
- source_id: `source_synthetic_expanded_000001`
- source type: project-authored synthetic educational corpus
- approved file count: `45`
- categories covered:
  - ML notes
  - Python teaching examples
  - Transformer notes
  - training systems notes
  - bilingual technical notes

The intake script recursively scanned the full `synthetic_expanded` tree and excluded only the top-level corpus README from candidate content.

## 3. Processed Outputs
Updated outputs:
- `data/real_corpus/processed/synthetic_expanded.processed.jsonl`
- `data/real_corpus/splits/synthetic_expanded.train.jsonl`
- `data/real_corpus/splits/synthetic_expanded.val.jsonl`
- `data/real_corpus/metadata/synthetic_expanded.dropped_files.jsonl`
- `data/real_corpus/metadata/synthetic_expanded.intake_summary.json`

Observed counts:
- candidate files: `45`
- processed docs: `45`
- dropped files: `0`
- secret_scan_hits: `0`

## 4. Train/Val Split
Using the existing deterministic split seed (`1337`) and 90/10 split policy, the refreshed outputs produced:
- train docs: `41`
- val docs: `4`

This keeps the split bounded and reproducible while reflecting the expanded 45-file corpus.

## 5. Secret Scan Result
Post-intake JSONL validation passed for processed, train, and validation outputs.

The requested grep-based secret scan produced matches only for explanatory training vocabulary such as `token` inside educational text.
There were no matches for higher-risk patterns such as `api_key`, `secret`, `password`, `private_key`, or `sk-`.

Result: `explanatory-only`

## 6. What It Does Not Do
This step does not:
- download data
- copy external corpus text
- read private user files
- train a tokenizer
- train a model
- run training
- modify model code

## 7. Limitations
- this is still a synthetic project-authored corpus, not an external real-world dataset
- the 45-file corpus is larger than the earlier 15-file batch, but still small for meaningful language-model quality claims
- the current outputs validate intake coverage and reproducibility, not tokenizer quality or model quality

## 8. Next Step
Recommended next step:
- D9 retrain expanded/domain BPE tokenizer on the 45-file corpus
