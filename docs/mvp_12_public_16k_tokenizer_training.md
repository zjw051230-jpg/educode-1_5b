# MVP-12 Public FineWeb-Edu 16k Tokenizer Training

## 1. Purpose

MVP-12 trains a new public-corpus BPE tokenizer for the reviewed FineWeb-Edu 500MB corpus path.

The goal is to make a public English corpus tokenizer available before planning longer 300M experiments on the expanded FineWeb-Edu data substrate.

## 2. Input Corpus

Training input:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl
```

Validation input:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl
```

Input metadata:

| field | value |
|---|---|
| dataset_id | `HuggingFaceFW/fineweb-edu` |
| dataset_config | `sample-10BT` |
| source_slice | `500MB` |
| license | `odc-by` |
| text_field | `text` |
| train records | 103619 |
| validation records | 5498 |

The raw, processed, and split corpus files remain local-only and ignored by Git.

## 3. Why 16k

The prior mixed-domain tokenizer has an 8k vocabulary and was trained for a different corpus mixture. It was sufficient for MVP-8 and MVP-9 training-systems validation, but the post-A800 route now needs a tokenizer that better matches the public FineWeb-Edu path.

A 16k target is a bounded next step:

- larger than the mixed-domain 8k baseline;
- still modest relative to future larger-corpus tokenizer work;
- appropriate for a 500MB public-corpus slice;
- useful for tokenizer comparison before a 300M 1000-step bounded run.

## 4. Training Script

Script:

```text
scripts/train_fineweb_edu_public_bpe_16k.py
```

Config:

```text
configs/tokenizers/fineweb_edu_public_bpe_16k.json
```

Command:

```text
.venv/Scripts/python.exe scripts/train_fineweb_edu_public_bpe_16k.py --config configs/tokenizers/fineweb_edu_public_bpe_16k.json
```

The script trains a ByteLevel BPE tokenizer with Hugging Face `tokenizers`, using the train split only. It does not read the validation split during training.

## 5. Tokenizer Artifacts

New artifact directory:

```text
tokenizers/fineweb_edu_public_bpe_16k/
```

Created files:

- `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json`
- `tokenizers/fineweb_edu_public_bpe_16k/tokenizer_config.json`
- `tokenizers/fineweb_edu_public_bpe_16k/training_summary.json`
- `tokenizers/fineweb_edu_public_bpe_16k/validation_summary.json`
- `tokenizers/fineweb_edu_public_bpe_16k/README.md`

Existing mixed-domain tokenizer directory remains unchanged:

```text
tokenizers/educode_bpe_mixed_domain_8k/
```

## 6. Observed Vocab

Training result:

| metric | value |
|---|---:|
| target_vocab_size | 16384 |
| observed_vocab_size | 16384 |
| train_records_seen | 103619 |

The observed vocabulary size matches the configured target size.

## 7. Special Tokens

Configured special tokens:

| token | id |
|---|---:|
| `<|endoftext|>` | 0 |
| `<|pad|>` | 1 |
| `<|unk|>` | 2 |

Validation confirmed all configured special tokens exist and have non-empty IDs.

## 8. Round-trip Validation

Validation script:

```text
scripts/validate_fineweb_edu_public_bpe_16k.py
```

Command:

```text
.venv/Scripts/python.exe scripts/validate_fineweb_edu_public_bpe_16k.py --config configs/tokenizers/fineweb_edu_public_bpe_16k.json
```

Validation summary:

| metric | value |
|---|---:|
| train_samples_checked | 20 |
| val_samples_checked | 20 |
| round_trip_pass_count | 40 |
| round_trip_fail_count | 0 |
| unk_token_count_on_samples | 0 |
| sampled_char_count | 65335 |
| sampled_public_token_count | 15302 |
| chars_per_token | 4.269703 |
| average_tokens_per_char | 0.234208 |

Round-trip validation passed without whitespace-normalization exceptions.

## 9. Comparison vs Mixed-domain 8k

Baseline tokenizer:

```text
tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json
```

Comparison metrics on the same sampled FineWeb-Edu text:

| metric | public 16k | mixed-domain 8k |
|---|---:|---:|
| vocab size | 16384 | 8192 |
| sampled token count | 15302 | 21615 |

Token count ratio:

```text
token_count_ratio_public_vs_mixed = 0.707934
```

On the validation sample, the public 16k tokenizer produced about 70.8% as many tokens as the mixed-domain 8k tokenizer. This is directionally consistent with a larger tokenizer trained on the target public corpus, but it is still only a bounded sample comparison and not a model-quality claim.

## 10. What MVP-12 Does Not Do

MVP-12 does not:

- train a model;
- enter A100 or A800;
- overwrite the existing mixed-domain 8k tokenizer;
- modify existing tokenizer artifacts;
- commit raw, processed, or split corpus data;
- claim model-quality improvement.

## 11. Next Step

Next step: MVP-13 300M 1000-step bounded run plan using the 500MB FineWeb-Edu corpus and an explicit tokenizer decision.

MVP-13 should decide whether to use the new public 16k tokenizer directly or first run a short tokenizer comparison smoke against the existing mixed-domain 8k tokenizer.
