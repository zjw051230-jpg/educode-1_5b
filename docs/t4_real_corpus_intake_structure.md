# T4 Real Corpus Intake Structure

## 1. Purpose
The purpose of T4 is to turn the T3 dataset planning step into a concrete directory structure and data intake checklist.

## 2. Files Added
- `data/real_corpus/README.md`
- `data/real_corpus/raw/.gitkeep`
- `data/real_corpus/processed/.gitkeep`
- `data/real_corpus/splits/.gitkeep`
- `data/real_corpus/metadata/.gitkeep`
- `data/real_corpus/metadata/source_manifest.template.jsonl`
- `data/real_corpus/processed/processed_text.template.jsonl`
- `data/real_corpus/splits/split_policy.md`
- `docs/data_intake_checklist.md`

## 3. What It Does
This step:
- creates the real corpus directory skeleton
- defines a source metadata template
- defines a processed JSONL template
- defines a split policy
- defines a data intake checklist
- keeps the current stage safe and no-data

## 4. What It Does Not Do
This step does not:
- download data
- add a real corpus
- train a tokenizer
- train a model
- write a data pipeline
- modify configs
- execute `git push`

## 5. Git Safety
- templates are safe to commit
- real raw data should be reviewed before committing
- large processed corpora should stay ignored or be handled later
- no secrets/private data should enter the repo

## 6. Next Step
Recommended next step:
- T4.1: choose the first approved local corpus source
- then T5: write the data intake / cleaning script plan
