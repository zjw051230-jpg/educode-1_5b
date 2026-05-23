# MVP-13.1 Public 16k Data/Model/Loss Smoke

## Purpose

MVP-13.1 verifies that the MVP-12 public FineWeb-Edu `16k` tokenizer can drive the local data/model/loss path before any `300M` `1000-step` A100/A800 execution.

This step validates compatibility only. It does not train a model.

## Input Corpus

The smoke used the reviewed local FineWeb-Edu `500MB` public corpus split from MVP-11.1.

| field | value |
|---|---:|
| train docs | `103619` |
| validation docs | `5498` |
| sequence length | `128` |
| batch size | `4` |

Train split:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl
```

Validation split:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl
```

The raw, processed, and split corpus files remain local-only and ignored by Git.

## Tokenizer

Tokenizer artifact:

```text
tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json
```

Observed tokenizer vocabulary size:

```text
16384
```

This matches the MVP-12 tokenizer validation result and the MVP-13.1 smoke config.

## Why This Smoke Was Needed

MVP-13 selected the public `16k` tokenizer as the intended tokenizer for the next public-corpus `300M` run, but deliberately did not send it directly into a `1000-step` GPU execution.

The tokenizer swap changes the vocabulary boundary from the prior mixed-domain `8192` path to `16384`. That changes embedding and output-logit dimensions, so a local model forward/loss smoke is the correct gate before paid GPU execution.

## Batch Shape

The smoke encoded FineWeb-Edu text with the public `16k` tokenizer and built next-token `input_ids` and `targets` tensors.

| tensor | shape |
|---|---|
| input_ids | `[4, 128]` |
| targets | `[4, 128]` |

## Model Forward

The smoke instantiated the project decoder-only Transformer path with a `300M`-class shape and `vocab_size=16384`.

Observed parameter count:

```text
336106496
```

The forward pass produced logits with the required shape:

```text
[4, 128, 16384]
```

This confirms that the public `16k` tokenizer can drive model forward/loss on the current local model path.

## Loss Check

The smoke computed next-token cross entropy without backward or optimizer execution.

| field | value |
|---|---:|
| loss_value | `9.8125` |
| loss_finite | `true` |
| device | `cuda` |
| model_dtype | `bfloat16` |

The loss value is a random-initialization compatibility check only. It is not a model-quality metric.

## Result Summary

Summary artifact:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/fineweb_edu_public16k_data_model_loss_smoke_summary.json
```

Required checks passed:

- tokenizer vocabulary size is `16384`;
- `input_ids_shape` is `[4, 128]`;
- `targets_shape` is `[4, 128]`;
- `logits_shape` is `[4, 128, 16384]`;
- loss is finite;
- no backward pass ran;
- no optimizer step ran;
- no checkpoint was written;
- no training loop ran.

## What MVP-13.1 Does Not Do

MVP-13.1 does not:

- train a model;
- run a training loop;
- run backward;
- run an optimizer step;
- save a checkpoint;
- train or overwrite a tokenizer;
- download data;
- enter A100/A800;
- modify core model code;
- advance D20/E-line corpus work;
- claim model quality.

## Next Step

Next step: MVP-14 A800 `300M` `1000-step` execution plan using the FineWeb-Edu `500MB` public corpus and the public `16k` tokenizer.

MVP-14 should still preserve MVP-10 logging cleanup requirements before execution approval.
