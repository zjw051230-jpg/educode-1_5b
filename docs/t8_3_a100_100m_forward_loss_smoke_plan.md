# T8.3 A100 100M Forward/Loss Smoke Plan

## 1. Purpose
The purpose of T8.3 is to plan a future 100M-scale forward/loss smoke step on A100 hardware without actually running it in this milestone.

This step is planning only.
It does not enter an A100 machine, does not run the smoke, and does not execute training.

## 2. Preconditions
Preconditions for the future A100 forward/loss smoke step:
- an A100 machine is available
- the T8.2 environment checklist has passed
- the repo is synced to the required commit
- `torch.cuda.is_available()` is `True`
- `configs/a100/educode_100m_a100_draft.json` validation has passed

## 3. Smoke Scope
This future smoke step should do only the following:
- load the config
- load the tokenizer
- initialize the 100M-scale dense model
- create one synthetic or processed batch
- run one forward pass
- compute next-token loss
- check that the loss is finite
- record memory and step-time information

This future smoke step should not do the following:
- backward
- optimizer step
- checkpoint save/load
- generation
- long training

## 4. Expected Script Later
Expected future script name:
- `scripts/inspect_a100_100m_forward_loss_smoke.py`

That future script should report:
- device
- GPU name
- config path
- parameter count
- `input_ids` shape
- `logits` shape
- loss value
- whether loss is finite
- CUDA memory allocated/reserved
- elapsed time

## 5. Success Criteria
Success criteria for the future smoke step:
- config validates
- model initializes on A100
- forward pass succeeds
- logits shape is correct
- loss is finite
- no OOM occurs
- memory statistics are recorded

## 6. Failure Handling
Failure handling order:
- if OOM occurs, reduce `batch_size` first
- then reduce `context_length`
- then reduce model size
- if CUDA is unavailable, stop
- if config validation fails, fix the config before retrying

## 7. Guardrails
Guardrails for this stage:
- not a training run
- not 100M pretraining
- not 1.5B
- not B200
- no model quality claim

## 8. Next Step
Recommended next step:
- T8.4 implement the A100 100M forward/loss smoke script, only when an actual A100 environment is available.
