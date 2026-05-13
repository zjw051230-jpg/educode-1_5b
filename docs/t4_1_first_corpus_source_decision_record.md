# T4.1 First Corpus Source Decision Record

## 1. Purpose
This step creates a decision record for selecting the first approved real-data source.

## 2. Files Added or Updated
- `docs/t4_1_first_corpus_source_decision.md`
- `data/real_corpus/metadata/source_decision.template.json`
- `data/real_corpus/metadata/source_manifest.template.jsonl`
- `docs/data_intake_checklist.md`

## 3. Decision
Current decision state:
- recommended first source: user-created local CS/ML/code notes
- approval status: pending user source selection
- no real data added
- no external data downloaded
- no training allowed yet

## 4. Next Required User Input
The next step requires the user to provide:
- approved local path
- source category
- license / ownership
- whether allowed for training
- whether allowed for Git commit
- whether it may contain private data
- expected file types

## 5. What It Does Not Do
This step does not:
- copy data
- download data
- train anything
- write a pipeline
- execute `git push`
