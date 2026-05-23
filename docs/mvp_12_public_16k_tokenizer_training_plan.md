# MVP-12 Public 16k Tokenizer Training Plan

## 1. Purpose

MVP-12 will train a public-corpus BPE tokenizer on the reviewed FineWeb-Edu 500MB intake outputs.

The goal is to create a tokenizer that better fits the public English corpus path before longer 300M public-corpus training experiments.

## 2. Why Train Public 16k Tokenizer After 500MB

The 50MB FineWeb-Edu slice was enough to prove the fetch, intake, and training-systems path, but it is too small to justify a stronger public tokenizer artifact.

The 500MB slice gives MVP-12 a better bounded substrate:

- larger than the smoke-scale 50MB slice;
- still reviewable and locally manageable;
- aligned with the public English corpus path;
- ready for comparison against the current mixed-domain 8k tokenizer baseline.

A public 16k tokenizer should come before a longer 300M public-corpus training run so the later run is not tied to a tokenizer trained for a different corpus mixture.

## 3. Input Corpus

Primary training input:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl
```

Validation/statistics input:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl
```

Input record field:

```text
text
```

The corpus is local-only. MVP-12 may read it, but should not commit the raw, processed, or split corpus files.

## 4. Existing Tokenizer Baseline

Baseline tokenizer:

```text
tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json
```

Baseline role:

- preserve the tokenizer used by prior mixed-domain and FineWeb-Edu 50MB smoke paths;
- compare tokenization efficiency and corpus fit against the new public 16k tokenizer;
- avoid rewriting history for MVP-8/MVP-9 A800 results.

## 5. Target Tokenizer

Target tokenizer artifact:

```text
tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json
```

Expected companion files:

```text
tokenizers/fineweb_edu_public_bpe_16k/tokenizer_config.json
tokenizers/fineweb_edu_public_bpe_16k/README.md
```

Target properties:

- source corpus: FineWeb-Edu 500MB train split;
- vocabulary target: `16000` tokens;
- intended use: public-corpus tokenizer comparison and future bounded public-corpus training;
- existing tokenizer artifacts remain unchanged.

## 6. Special Tokens Policy

MVP-12 should preserve the project tokenizer conventions used by the existing BPE path unless a preflight review finds a mismatch.

Required special tokens:

- `<pad>`
- `<unk>`
- `<bos>`
- `<eos>`

The tokenizer config should record:

- tokenizer name;
- vocab size observed after training;
- source corpus path;
- train record count;
- validation record count;
- special token IDs;
- artifact path;
- creation timestamp.

## 7. Round-Trip Checks

MVP-12 should run bounded encode/decode checks before accepting the tokenizer artifact.

Minimum checks:

- encode/decode short English educational text;
- encode/decode text containing punctuation and numbers;
- encode/decode text sampled from the FineWeb-Edu validation split;
- verify token IDs are integers within vocabulary bounds;
- verify no empty token sequence for non-empty input;
- verify special tokens are present in the tokenizer vocabulary.

Round-trip checks do not need to prove perfect whitespace preservation, but they should catch broken artifacts, missing special tokens, and unusable encode/decode behavior.

## 8. Comparison Plan vs Mixed-Domain 8k

Compare `fineweb_edu_public_bpe_16k` against `educode_bpe_mixed_domain_8k` on the same bounded FineWeb-Edu validation sample.

Suggested comparison metrics:

- total characters evaluated;
- document count evaluated;
- total tokens under mixed-domain 8k;
- total tokens under public 16k;
- mean tokens per document;
- mean characters per token;
- longest tokenized document length;
- unknown token count if available;
- examples where token count differs materially.

The comparison should be documented before any model training uses the new tokenizer.

## 9. Validation Before Model Use

Before using the tokenizer in a model run, MVP-12 should add or run a bounded data/model/loss smoke that confirms:

- tokenizer artifact loads;
- public corpus batches can be tokenized;
- model config vocab size matches tokenizer vocab size;
- forward pass and loss computation work on a tiny bounded batch.

That smoke should be a separate validation step from tokenizer training.

## 10. What MVP-12 Will Not Do

MVP-12 will not:

- train a model;
- overwrite the existing mixed-domain 8k tokenizer;
- reinterpret prior A800 results;
- commit raw, processed, or split corpus data;
- enter A100 or A800 unless a later explicit execution step requests it.

## 11. Expected Next Step

Implement MVP-12 as a tokenizer-only milestone:

1. create the public 16k tokenizer training script or adapt the existing BPE training pattern;
2. train `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json` from the 500MB train split;
3. run round-trip checks;
4. run tokenizer comparison against `educode_bpe_mixed_domain_8k`;
5. document results without model training.
