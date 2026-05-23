# MVP-4 Public Corpus Tokenizer Decision

## 1. Current Public Corpus Slice
Current bounded public slice:
- dataset_id: `HuggingFaceFW/fineweb-edu`
- dataset_config: `sample-10BT`
- source raw file: `data/public_corpus/fineweb_edu_sample10bt_50mb/raw.jsonl`
- processed file: `data/public_corpus/fineweb_edu_sample10bt_50mb/processed/fineweb_edu_50mb.processed.jsonl`
- train split: `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.train.jsonl`
- val split: `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.val.jsonl`

Observed intake counts:
- processed_count: `11070`
- train_count: `10503`
- val_count: `567`
- dropped_empty_count: `0`
- dropped_duplicate_count: `1`

## 2. Tokenizer Options
### Option 1 — Reuse existing mixed/domain 8k tokenizer for MVP-5 smoke
Existing tokenizer artifact:
- `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`

Pros:
- fastest path into MVP-5 data/model/loss smoke
- no new tokenizer training required in this step
- already integrated into existing smoke configuration patterns in this repository

Cons:
- tokenizer was trained on `mixed_domain_external`, not on FineWeb-Edu
- segmentation quality on public web-education text may be suboptimal

### Option 2 — Train a new public-corpus 16k tokenizer later
Pros:
- better fit to the public corpus distribution
- likely improved tokenization efficiency relative to reusing the mixed/domain 8k artifact

Cons:
- requires a deliberate tokenizer-training step
- better deferred until the public-corpus line is larger than the current `50MB` slice

### Option 3 — Train a 32k tokenizer after larger public-corpus expansion
Pros:
- better longer-term fit if the public-corpus line becomes a major training backbone
- can align with later `100MB` / `500MB` bounded slices or larger approved public-corpus aggregation

Cons:
- highest delay and largest scope increase
- unnecessary for the shortest MVP smoke path

## 3. Recommendation
Recommended path:
- for MVP-5, reuse the existing mixed/domain tokenizer artifact at `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`
- do not train a new tokenizer in MVP-4
- treat the current public-corpus slice as a data-path and smoke-readiness validation step

This is the shortest path toward the next smoke milestone while avoiding a tokenizer-training detour.

## 4. Risks
Known risks:
- the existing tokenizer may be suboptimal on FineWeb-Edu text distribution
- token counts and segmentation behavior may differ from a later public-corpus-specific tokenizer
- any quality conclusions from MVP-5 should be interpreted as smoke-path validation, not final tokenizer quality validation

These risks are acceptable for MVP smoke because the immediate goal is data/model/loss path validation rather than optimized public-corpus pretraining quality.

## 5. Decision
Decision recorded for MVP short path:
- reuse `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json` for MVP-5 data/model/loss smoke
- postpone public-corpus tokenizer training to a later MVP-6 or follow-up corpus-scaling step
- preferred later follow-up: train a public `16k` tokenizer after additional bounded public slices such as `100MB` or `500MB`
- consider a `32k` tokenizer only after the public corpus becomes materially larger and more stable as a training backbone
