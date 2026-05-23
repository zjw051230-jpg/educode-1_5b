# MVP-13.1 Public 16k Data/Model/Loss Smoke Plan

## 1. Purpose

MVP-13.1 should verify that the MVP-12 public FineWeb-Edu `16k` tokenizer can drive the local data/model/loss path before any A100/A800 `300M` `1000-step` run.

This smoke is deliberately smaller than the GPU run and should not perform training.

## 2. Config

Draft config:

```text
configs/windows/fineweb_edu_500mb_public16k_data_model_loss_smoke.json
```

Key fields:

| field | value |
|---|---|
| run_name | `fineweb_edu_500mb_public16k_data_model_loss_smoke` |
| train_path | `data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl` |
| val_path | `data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl` |
| tokenizer_path | `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json` |
| tokenizer_source | `fineweb_edu_public_bpe_16k` |
| vocab_size | `16384` |
| sequence_length | `128` |
| batch_size | `4` |
| seed | `336` |
| no_training | `true` |

## 3. Required Smoke Behavior

The smoke should check only:

1. load config;
2. load tokenizer;
3. confirm tokenizer vocab size is `16384`;
4. confirm special token IDs match MVP-12;
5. read a small bounded train sample;
6. read a small bounded validation sample;
7. tokenize and form one train batch with `sequence_length=128`, `batch_size=4`;
8. tokenize and form one validation batch with `sequence_length=128`, `batch_size=4`;
9. instantiate a small local model with `vocab_size=16384`;
10. run train forward/loss once;
11. run validation forward/loss once;
12. assert both losses are finite;
13. write a small summary JSON only.

## 4. What It Must Not Do

The smoke must not:

- train a model;
- run optimizer steps;
- write checkpoints;
- run generation;
- enter A100/A800;
- download data;
- train or overwrite tokenizers;
- modify core model code;
- commit raw, processed, or split corpus files.

## 5. Suggested Output Summary

Suggested local summary path:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/fineweb_edu_500mb_public16k_data_model_loss_smoke_summary.json
```

Suggested summary fields:

```json
{
  "status": "success",
  "config_path": "configs/windows/fineweb_edu_500mb_public16k_data_model_loss_smoke.json",
  "tokenizer_path": "tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json",
  "vocab_size": 16384,
  "sequence_length": 128,
  "batch_size": 4,
  "train_batch_shape": [4, 128],
  "val_batch_shape": [4, 128],
  "train_loss_finite": true,
  "val_loss_finite": true,
  "optimizer_step_run": false,
  "checkpoint_written": false
}
```

## 6. Success Criteria

MVP-13.1 succeeds only if:

- config validation passes;
- tokenizer load passes;
- train and validation batch formation pass;
- model forward/loss runs with `vocab_size=16384`;
- train and validation losses are finite;
- the smoke does not write checkpoints or perform optimizer steps.

## 7. Follow-up Decision

If MVP-13.1 passes, the project can promote the public `16k` tokenizer into the next `300M` `1000-step` A100/A800 bounded execution plan.

If it fails, do not run the GPU experiment. Investigate whether the failure is in tokenizer loading, special-token handling, batch formation, model vocabulary sizing, or loss computation.
