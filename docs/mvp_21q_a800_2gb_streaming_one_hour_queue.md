# MVP-21.Q A800 2GB Streaming One-Hour Queue

## Purpose

Prepare a fuller 2GB FineWeb-Edu public16k A800/A100 execution queue so the next GPU session can start with the already validated 2GB 1000-step run and continue to longer bounded runs only after each prior run passes.

This is local preparation only. It does not enter A800/A100, run model training, train a tokenizer/model, create checkpoints, or commit raw/processed/split corpus artifacts.

## Queue Order

| order | config | max_steps | eval_interval | checkpoint_interval | gate |
|---:|---|---:|---:|---:|---|
| 1 | `configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json` | `1000` | `100` | `1000` | primary run |
| 2 | `configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json` | `3000` | `300` | `3000` | only after 1000-step success |
| 3 | `configs/a100/fineweb_edu_2gb_300m_5000step_public16k_execute.json` | `5000` | `500` | `5000` | only after 3000-step success and remaining rental time |

All configs keep `data_loading_mode=streaming`, `batch_size=8`, `gradient_accumulation_steps=4`, `sequence_length=512`, public16k vocab size `16384`, and exact parameter count `336106496`.

## Local Validation Evidence

| config | memory inspection | dry-run | readiness |
|---|---|---|---|
| 1000-step | passed; streaming batch tensor memory `0.062` MiB; host RAM safe | passed; `exact_parameter_count=336106496` | passed; blockers `0`, caveats `0` |
| 3000-step | passed; streaming batch tensor memory `0.062` MiB; host RAM safe | passed; `exact_parameter_count=336106496` | passed; blockers `0`, caveats `0` |
| 5000-step | passed; streaming batch tensor memory `0.062` MiB; host RAM safe | passed; `exact_parameter_count=336106496` | passed; blockers `0`, caveats `0` |

The 5000-step memory inspection estimates the old full precompute path at `645.137594` GiB of Python memory, while the streaming path keeps the steady-state batch tensor estimate at `0.062` MiB. This is why streaming remains mandatory for the queue.

## Data Logistics

GPU hosts should receive the prepared package before training:

```text
C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz
```

Remote train/val paths after extraction:

```text
data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.train.jsonl
data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.val.jsonl
```

The GPU host must not fetch Hugging Face data for this 2GB queue.

## Stop Conditions

Stop before launching the next queued command if any prior run has non-finite train loss, non-finite validation loss, non-finite gradients, checkpoint reload mismatch, post-run artifact validation failure, CUDA OOM, missing split files, or readiness blockers.

## Claim Boundary

This queue can provide bounded training-systems evidence for data logistics, streaming stability, loss finiteness, and artifact validation. It is not model-quality evidence.
