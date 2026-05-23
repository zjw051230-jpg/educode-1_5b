# MVP-13 300M 1000-step Bounded Run Plan

## 1. Purpose

This document drafts the next `300M` `1000-step` bounded GPU run on the reviewed FineWeb-Edu `500MB` public corpus with the MVP-12 public `16k` tokenizer.

This is not execution approval. It is a plan and config draft for later A100/A800 execution after required gates pass.

## 2. Planned Run Identity

| field | value |
|---|---|
| run_name | `fineweb_edu_500mb_300m_1000step_public16k_execute` |
| config | `configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json` |
| output_dir | `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute` |
| hardware target | `A100-80GB or A800-40GB` |
| runtime device | `cuda` |
| runtime dtype | `bf16_if_available_else_fp16` |
| training status | draft, not run |

## 3. Corpus and Tokenizer

Corpus:

| field | value |
|---|---|
| dataset_id | `HuggingFaceFW/fineweb-edu` |
| dataset_config | `sample-10BT` |
| source_slice | `500MB` |
| license | `odc-by` |
| train records | `103619` |
| validation records | `5498` |

Train split:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl
```

Validation split:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl
```

Tokenizer:

| field | value |
|---|---|
| tokenizer_source | `fineweb_edu_public_bpe_16k` |
| tokenizer_path | `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json` |
| vocab_size | `16384` |
| special tokens | `<|endoftext|>`, `<|pad|>`, `<|unk|>` |

## 4. Model Shape

The draft keeps the reviewed `300M` model class from MVP-8/MVP-9 while changing tokenizer vocabulary size to `16384`.

| field | value |
|---|---:|
| architecture | `dense_decoder_only` |
| model_size_label | `300m` |
| vocab_size | `16384` |
| context_length | `512` |
| num_layers | `18` |
| d_model | `1024` |
| num_heads | `16` |
| head_dim | `64` |
| d_ff | `4096` |
| ffn_type | `swiglu` |
| norm_type | `rmsnorm` |
| position_encoding | `learned_position_embedding` |
| tie_embeddings | `false` |

The config deliberately declares `learned_position_embedding` for this draft because MVP-10 found that the current core model path does not yet validate a RoPE implementation.

## 5. Training Bounds

| field | value |
|---|---:|
| max_steps | `1000` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| sequence_length | `512` |
| global_batch_tokens | `16384` |
| eval_interval | `100` |
| checkpoint_interval | `1000` |
| log_interval | `1` |
| mixed_precision | `bf16` |

This remains a bounded training-systems run. It is not a serious pretraining campaign and does not support model-quality claims.

## 6. Required Gates Before Execution

### Gate 1: MVP-13.1 public16k data/model/loss smoke

The local smoke must pass before this GPU run is approved. It should confirm:

- public tokenizer loads;
- `500MB` train and validation batches form;
- `vocab_size=16384` model/loss path works;
- losses are finite;
- no training loop or checkpoint is written.

### Gate 2: Logging cleanup

Before execution, the runner/report path must satisfy MVP-10 cleanup requirements:

- write standalone `validation_metrics.jsonl`;
- derive checkpoint paths from the current run output directory;
- ensure `run_id` includes the true `1000step` identity;
- do not report a scheduler as active unless it is actually applied;
- run post-run artifact validation against the actual output directory.

### Gate 3: Artifact policy

Do not commit:

- raw corpus files;
- processed/splits corpus files;
- checkpoints;
- result tarballs;
- large logs.

Commit only configs, reports, summaries, and small validation metadata.

## 7. Expected Post-run Review Criteria

A later execution review should check:

| check | expected |
|---|---|
| metrics rows | `1000` |
| validation rows | expected eval schedule for steps `100, 200, ..., 1000` |
| finite train losses | `true` |
| finite validation losses | `true` |
| finite gradients | `true` |
| checkpoint reload match | `true` |
| checkpoint path | inside `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute` |
| standalone validation metrics | present |
| config tokenizer vocab | `16384` |
| model vocab | `16384` |

## 8. Known Caveats to Preserve

Even if this run later succeeds, it should be described as:

- bounded training-systems validation;
- public tokenizer integration validation;
- longer short-run stability evidence;
- not model quality evidence;
- not final architecture validation;
- not proof that the future RoPE path is implemented.

## 9. Next Step

Immediate next step: MVP-13.1 local public `16k` data/model/loss smoke plan and execution.

If MVP-13.1 passes, a later MVP can approve the `300M` `1000-step` A100/A800 execution using the draft config from this step.

## 10. MVP-14.P Cleanup Gate Completed

MVP-14.P completed the pre-execution logging and path cleanup gate for the public16k `300M` `1000-step` draft.

Completed gate results:

- MVP-13.1 public16k data/model/loss smoke passed;
- `run_id` is now derived from the current config `run_name` instead of a hardcoded `10step` phrase;
- checkpoint paths are constrained to the current `output_dir/checkpoints`;
- standalone `validation_metrics.jsonl` writing is supported during evaluation;
- post-run artifact validation is available for summary, metrics, validation metrics, config, metadata, checkpoint path, and checkpoint reload status;
- public16k readiness passed with `blockers=0`.

The `1000-step` GPU run may proceed only after the readiness summary remains passing on the execution machine and the user explicitly approves the real A800/A100 execution.
