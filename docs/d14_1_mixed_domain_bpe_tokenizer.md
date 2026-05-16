# D14.1 Mixed/Domain BPE Tokenizer

## 1. Purpose
D14.1 trains a mixed/domain BPE tokenizer artifact on the approved `mixed_domain_external` corpus.

The goal of this step is to produce a tokenizer-only artifact for later mixed-corpus data/model/loss smoke work while keeping the project backbone unchanged and keeping `external_general_text` as a supplement only.

## 2. Corpus Used
Tokenizer training input:
- corpus path: `data/real_corpus/processed/mixed_domain_external.processed.jsonl`
- input docs: `57`
- train split used: `52`
- val split excluded from training: `5`
- synthetic docs in mixed corpus: `45`
- external docs in mixed corpus: `12`

Training scope in this step:
- train texts were taken from `split == train`
- no new intake was run
- no new external data was downloaded
- no model training was run

## 3. Source Category Counts
Observed source-category counts from the mixed corpus:
- input source counts: `{"synthetic_examples": 45, "external_general_text": 12}`
- train source counts: `{"synthetic_examples": 41, "external_general_text": 11}`

`source_category` remained preserved in the mixed corpus, and `external_general_text` remained supplement only.

## 4. Tokenizer Artifact
Created artifact directory:
- `tokenizers/educode_bpe_mixed_domain_8k/`

Artifact files created:
- `tokenizer.json`
- `tokenizer_config.json`
- `special_tokens_map.json`
- `README.md`
- `vocab.json`
- `merges.txt`

Artifact config summary:
- tokenizer name: `educode_bpe_mixed_domain_8k`
- library: `tokenizers`
- model type: `BPE`
- target vocab size: `8192`
- corpus path: `data/real_corpus/processed/mixed_domain_external.processed.jsonl`
- train split only: `true`

## 5. Observed Vocab Size
Observed tokenizer result:
- target vocab size: `8192`
- observed vocab size: `8192`

This means the tokenizer reached the configured target size on the current mixed corpus.
This is a tokenizer artifact result only and does not imply model quality.

## 6. Special Token IDs
Observed special token ids:
- `<pad>` = `0`
- `<bos>` = `1`
- `<eos>` = `2`
- `<unk>` = `3`

## 7. Round Trip Results
Inspection script:
- `scripts/inspect_mixed_domain_bpe_tokenizer.py`

Round-trip sample set included:
- `hello world`
- `你好，世界`
- `Python code: print('hello')`
- `Transformer models predict the next token.`
- `loss = F.cross_entropy(logits, targets)`
- `A100 2.15B seq512 optimizer profile`
- `Gradient clipping stabilizes training.`
- `JSONL data pipelines preserve document boundaries.`
- `Alice was beginning to get very tired of sitting by her sister on the bank.`
- `Emoji test 😊`

Observed result:
- all round-trip checks passed
- `all_round_trip_exact = True`
- `failed_input_count = 0`

## 8. Comparison with Previous Tokenizers
Tokenizer comparison:
- D4 expanded BPE observed vocab = `1846`
- D9 domain BPE observed vocab = `3988`
- D14.1 mixed/domain BPE observed vocab = `8192`

Interpretation:
- D14.1 produced a larger observed vocabulary than both the earlier expanded-only and domain-only tokenizer artifacts
- the mixed corpus broadened the tokenizer training input while keeping the project backbone constraint intact
- this comparison describes tokenizer artifact coverage only, not downstream model quality

## 9. What It Does Not Do
D14.1 does not:
- train a model
- run bounded model training
- modify model code
- replace the D9 domain tokenizer artifact
- change the rule that `external_general_text` is supplement only

## 10. Limitations
Current limitations:
- tokenizer quality is still limited by the small approved corpus size
- reaching the target vocab size does not prove strong segmentation quality on broader unseen data
- this step validates tokenizer artifact creation and inspection only
- the mixed corpus still includes only a small external supplement, not a large general-language backbone

## 11. Next Step
Recommended next step:
- D15 mixed/domain BPE data/model/loss smoke
