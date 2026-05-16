# D14 Mixed/Domain BPE Tokenizer Retraining Plan

## 1. Purpose
Plan BPE tokenizer retraining on the `mixed_domain_external` corpus for later mixed-corpus smoke validation and bounded training steps.

## 2. Current Corpus
Current mixed-corpus state:
- mixed total docs = 57
- train docs = 52
- val docs = 5
- synthetic_domain docs = 45
- external_general_text docs = 12
- `source_category` preserved
- external text remains supplement only

This means the next tokenizer step can use a broader approved text mix than the prior domain-only path while still preserving project identity and provenance separation.

## 3. Previous Tokenizer Baselines
Tokenizer baselines to compare against:
- D4 expanded BPE observed vocab = 1846
- D9 domain BPE observed vocab = 3988
- D14 target vocab size = 8192
- expected observed vocab may still be below 8192 because the corpus remains small

Interpretation:
- a larger observed vocabulary than D9 would suggest broader mixed-corpus coverage
- an observed vocabulary below 8192 would still be expected if corpus variety remains limited
- tokenizer size alone is not evidence of model quality

## 4. Training Scope
D14.1 should:
- read `data/real_corpus/processed/mixed_domain_external.processed.jsonl`
- prefer `split == train`
- train a Hugging Face `tokenizers` BPE tokenizer
- target `vocab_size = 8192`
- use these special tokens:
  - `<pad>`
  - `<bos>`
  - `<eos>`
  - `<unk>`
- write the artifact to:
  - `tokenizers/educode_bpe_mixed_domain_8k/`

## 5. Artifact Requirements
The D14.1 artifact should include:
- `tokenizer.json`
- `tokenizer_config.json`
- `special_tokens_map.json`
- `README.md`
- `vocab.json` / `merges.txt` if available

The artifact should remain separate from earlier tokenizer directories so that the D9 domain tokenizer and earlier expanded tokenizer artifacts remain intact for comparison.

## 6. Validation Requirements
A D14.1 inspection script should check:
- observed vocab size
- special token ids
- exact round-trip behavior on representative inputs
- CS / ML / Python examples
- bilingual examples
- external general English example
- an A100 / training-system phrase

The purpose of this validation is to confirm artifact health and coverage behavior, not to claim downstream model performance.

## 7. Config Implication
D15 should create a mixed BPE smoke config with:
- `tokenizer.path = tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`
- `tokenizer.vocab_size = observed vocab`
- `model.vocab_size = observed vocab`
- `source_category` metadata remaining in the corpus artifacts

This keeps tokenizer and model vocabulary sizes aligned with the observed mixed-corpus tokenizer result instead of the nominal target.

## 8. Guardrails
Guardrails for D14 and D14.1:
- `external_general_text` remains supplement only
- do not claim model quality from tokenizer size
- do not train a model in D14
- do not enter the A100 path
- do not overwrite previous tokenizers
- keep the D9 domain tokenizer artifact intact

## 9. Success Criteria for D14.1
- tokenizer training completes
- observed vocab size reported
- special token ids reported
- round-trip tests pass
- artifact committed
- no model training

## 10. Next Step
D14.1: train a mixed/domain BPE tokenizer on the `mixed_domain_external` corpus.
