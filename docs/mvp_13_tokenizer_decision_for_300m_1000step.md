# MVP-13 Tokenizer Decision for 300M 1000-step Run

## 1. Purpose

MVP-13 decides how the next `300M` `1000-step` bounded run should use the newly trained public FineWeb-Edu tokenizer.

This is a planning and decision step only. It does not run model training, rent GPU time, download data, train a tokenizer, or modify core model code.

## 2. Inputs Reviewed

### 2.1 Prior A800 training-systems evidence

MVP-8 and MVP-9 validated the current bounded training loop on `A800-SXM4-40GB` with the `319329280`-parameter model and the mixed-domain `8k` tokenizer.

MVP-9 observed:

| field | value |
|---|---:|
| max_steps | `100` |
| tokenizer_vocab_size | `8192` |
| exact_parameter_count | `319329280` |
| metrics_rows | `100` |
| validation_rows | `5` |
| tokens_seen | `1638400` |
| checkpoint_reload_match | `true` |
| loss_all_finite | `true` |
| val_loss_all_finite | `true` |
| grad_all_finite | `true` |

Interpretation: the run is valid training-systems evidence, not a model-quality result.

### 2.2 MVP-10 caveats

MVP-10 recorded caveats that must remain visible before the next GPU run:

- the old configs declared `rope`, while the current core model path reported `learned_position_embedding`;
- `validation_metrics.jsonl` was not written as a standalone artifact;
- MVP-9 `checkpoint_path` pointed into the `10step_execute` directory;
- `scheduler_config_present_but_not_applied=true`;
- run naming still contained a `10step_smoke` phrase in the 100-step result path.

These caveats do not invalidate MVP-8 or MVP-9, but they require tighter logging and config traceability before the next reviewed GPU execution.

### 2.3 MVP-11.1 public corpus expansion

MVP-11.1 created the reviewed local FineWeb-Edu `500MB` corpus slice:

| field | value |
|---|---:|
| processed_count | `109117` |
| train_count | `103619` |
| val_count | `5498` |
| dropped_empty_count | `0` |
| dropped_duplicate_count | `13` |
| total_text_bytes | `524232621` |

Train split:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl
```

Validation split:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl
```

The raw, processed, and split corpus files remain local-only and ignored by Git.

### 2.4 MVP-12 public tokenizer

MVP-12 trained and validated the public FineWeb-Edu `16k` tokenizer:

| field | value |
|---|---:|
| tokenizer | `fineweb_edu_public_bpe_16k` |
| target_vocab_size | `16384` |
| observed_vocab_size | `16384` |
| train_records_seen | `103619` |
| round_trip_pass_count | `40` |
| round_trip_fail_count | `0` |
| unk_token_count_on_samples | `0` |
| sampled_public_token_count | `15302` |
| sampled_mixed_token_count | `21615` |
| token_count_ratio_public_vs_mixed | `0.707934` |

Tokenizer artifact:

```text
tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json
```

Special token IDs:

| token | id |
|---|---:|
| `<|endoftext|>` | `0` |
| `<|pad|>` | `1` |
| `<|unk|>` | `2` |

## 3. Decision

Decision: do not run the `300M` `1000-step` GPU experiment directly after tokenizer training.

Use the public FineWeb-Edu `16k` tokenizer as the intended tokenizer for the next public-corpus `300M` run, but gate GPU execution behind a local MVP-13.1 data/model/loss smoke first.

## 4. Why Not Direct 1000-step Execution

The public `16k` tokenizer is validated as a tokenizer artifact, but it has not yet exercised the model/loss path.

The tokenizer swap changes:

- tokenizer artifact path;
- special-token convention;
- configured vocabulary size from `8192` to `16384`;
- embedding and output-logit dimensions;
- token counts and batch packing behavior.

A short local smoke is cheaper and safer than discovering these issues during a paid GPU `1000-step` run.

## 5. A/B Decision

A mixed-domain `8k` vs public `16k` A/B smoke is optional, not required for the next route.

Recommended sequence:

1. run a local public `16k` data/model/loss smoke using the `500MB` train/val split;
2. if it passes, approve the public `16k` tokenizer for the next `300M` `1000-step` bounded GPU run;
3. only run a mixed-domain `8k` A/B smoke if the review goal is tokenizer continuity rather than preparing the next public-corpus run.

## 6. Next Gate

MVP-13.1 should validate:

- tokenizer load from `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json`;
- train and validation batch formation from the `500MB` split files;
- a small model can instantiate with `vocab_size=16384`;
- train and validation forward/loss are finite;
- no optimizer step, checkpoint, or training loop is run.

If MVP-13.1 passes, the next GPU planning step can promote the draft config:

```text
configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json
```

## 7. Scope Boundary

MVP-13 does not:

- run training;
- run the local smoke;
- use A100/A800;
- train or overwrite tokenizers;
- download new data;
- modify core model code;
- advance D20 or E-line corpus work;
- commit raw corpus files, processed/splits files, checkpoints, or result bundles.
