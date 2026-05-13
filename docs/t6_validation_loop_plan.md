# T6 Validation Loop Plan

## 1. Purpose
The purpose of T6 is to define the future validation loop needed before formal training work expands beyond the current smoke-only path.

This step stays at the planning level only.
It does not implement the validation loop, does not run training, and does not modify the model.

## 2. Current Baseline
Current baseline state:
- synthetic seed corpus has been created
- intake and cleaning have been completed
- processed docs = `8`
- train docs = `7`
- val docs = `1`
- `educode_bpe_8k` artifact has been created
- observed vocab size = `1174`
- BPE data/model/loss smoke has passed
- last smoke loss = `7.221643`

## 3. Why Validation Loop Is Needed
A formal validation loop is needed because:
- train loss alone is not enough
- validation loss is needed to check leakage and overfitting
- later small real-data training must record both `train_loss` and `val_loss`

Without a validation loop, the project can only confirm that the forward/loss path works.
It cannot meaningfully compare whether the model is fitting the training data while failing to generalize to held-out samples.

## 4. Planned Validation Flow
Planned validation flow:
- load config
- load tokenizer
- load processed train/val JSONL
- build train samples
- build val samples
- run train loss on batch
- run val loss under `torch.no_grad()`
- use `model.eval()` for validation
- perform no optimizer step during validation
- log metrics

## 5. Metrics
The future validation loop should record:
- `step`
- `train_loss`
- `val_loss`
- `tokens_seen`
- `elapsed_seconds`
- split sizes
- config hash or config path
- git commit

## 6. Success Criteria
Success criteria for the future validation loop:
- train loss is finite
- val loss is finite
- no CUDA OOM occurs
- validation does not update parameters
- metrics are written to JSONL
- a summary artifact is generated

## 7. Boundary
T6 does not:
- implement code
- run training
- download data
- train a tokenizer
- modify the model

## 8. Next Step
Recommended next step:
- T6.1 validation loop smoke script

That follow-up should stay bounded:
- one-batch train loss
- one-batch val loss
- no backward
- no optimizer step
