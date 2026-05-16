# EduCode Mixed Domain BPE 8k

This directory stores the `educode_bpe_mixed_domain_8k` tokenizer artifact trained on the approved `mixed_domain_external` corpus.
It is a tokenizer-only artifact for later smoke validation work.
It does not replace the D9 domain tokenizer artifact and does not imply model-quality claims.
The `external_general_text` portion remains supplement only.

Observed vocab size: 8192
Target vocab size: 8192
Corpus path: `data/real_corpus/processed/mixed_domain_external.processed.jsonl`
Train split used: `train` only
Train docs used: 52
Train source_category counts: `{"external_general_text": 11, "synthetic_examples": 41}`
