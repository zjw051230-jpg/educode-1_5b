# T7 Small Real-Data Training Plan

## 1. Purpose
The purpose of T7 is to define the first bounded small real-data training stage that follows the current synthetic-seed-only tokenizer, data, model, loss, and validation smoke path.

This step stays at the planning level only.
It does not implement a training script, does not train the model, and does not modify the model architecture.

## 2. Current Baseline
Current baseline state:
- synthetic seed corpus created
- processed docs = `8`
- train docs = `7`
- val docs = `1`
- BPE tokenizer artifact observed vocab = `1174`
- BPE data/model/loss smoke passed
- validation loop smoke passed
- train_loss smoke = `7.304811`
- val_loss smoke = `7.261631`

## 3. Training Scope
The first bounded training round should use:
- local Windows GPU
- synthetic seed corpus only
- BPE tokenizer with vocab size `1174`
- tiny dense decoder-only model
- `max_steps = 50` or `100`
- both `train_loss` and `val_loss`
- final checkpoint
- final generation sample
- structured logging

## 4. Success Criteria
Success criteria for the bounded training stage:
- train loss is finite
- val loss is finite
- no OOM occurs
- checkpoint reload works
- `metrics.jsonl` contains both train and val loss
- `summary.md` is generated
- no claim is made about real model quality

## 5. Guardrails
Guardrails for this stage:
- synthetic corpus only
- not large-scale pretraining
- not 1.5B
- not A100/B200
- no external data
- no production tokenizer claim

## 6. Planned Script
A future T7.1 implementation step can add:
- `scripts/run_small_real_data_training.py`

That future script should:
- load config
- load tokenizer
- load train/val splits
- train for bounded steps
- evaluate val loss every N steps
- save checkpoint
- write summary

## 7. What T7 Does Not Do
T7 does not:
- implement the script
- train the model
- download data
- modify the model

## 8. Next Step
Recommended next step:
- T7.1: bounded small real-data training script
