# MVP-2 FineWeb-Edu Public Corpus Source Decision

## 1. Purpose
The purpose of MVP-2 is to select the first public corpus source for the A100 pretraining MVP and define a bounded fetch plan without downloading a large dataset in this step.

This step is source decision and fetch planning only.
It does not download a large corpus, enter A100, train a tokenizer, train a model, or modify model code.

## 2. Selected Dataset
- dataset: `HuggingFaceFW/fineweb-edu`
- config: `sample-10BT`
- intended_use: public corpus source for the A100 pretraining MVP
- license: `odc-by`
- source format: Hugging Face datasets streaming / parquet

## 3. Why This Dataset Was Selected
FineWeb-Edu `sample-10BT` was selected because it is:
- public
- text-generation friendly
- educationally filtered
- streaming supported
- suitable for bounded local slices before any larger fetch or training step

## 4. Why Not Use Random Zenodo or Marketplace Chinese QA Data Now
This step does not choose a random Zenodo or marketplace Chinese QA dataset because those options currently introduce avoidable risk for the A100 MVP:
- license clarity may be weak or inconsistent
- corpus quality is unknown
- many such sources are instruction/SFT shaped rather than pretraining-corpus shaped
- some include mental-health style responses that would require additional safety review before corpus approval

## 5. Slice Plan
Planned bounded local slices:
- `10MB` dry-run test
- `50MB` smoke slice
- `100MB` first train slice
- `500MB` optional extended slice

The first committed config in MVP-2 targets the `50MB` smoke slice only.

## 6. Guardrails
- no large real download in MVP-2
- no A100 execution in MVP-2
- no tokenizer training in MVP-2
- no model training in MVP-2
- no model code changes in MVP-2
- no automatic promotion into other corpus lines in MVP-2

## 7. What MVP-2 Does Not Do
MVP-2 does not:
- fetch a large FineWeb-Edu slice
- create `raw.jsonl`
- write parquet shards into the repo
- enter A100
- run training
- train a tokenizer
- train a model
- modify model code

## 8. Next Step
Recommended next step:
- MVP-3 fetch a bounded `50MB` FineWeb-Edu `sample-10BT` slice using the dry-run-safe fetch script and committed config
