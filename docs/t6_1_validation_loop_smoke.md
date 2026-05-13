# T6.1 Validation Loop Smoke

## 1. Purpose
The purpose of T6.1 is to validate a bounded one-batch train-loss plus one-batch val-loss path using the current synthetic seed split files, linked BPE tokenizer artifact, and current tiny model configuration.

This step checks that the repository can compute both training-side and validation-side loss in one smoke script without entering real training behavior.

## 2. Files Added
- `scripts/inspect_validation_loop_smoke.py`
- `docs/t6_1_validation_loop_smoke.md`

## 3. What It Does
This smoke script:
- loads `configs/windows/bpe_8k_formal_placeholder.json`
- validates the config with `repo_root=PROJECT_ROOT`
- loads `tokenizers/educode_bpe_8k/tokenizer.json`
- reads:
  - `data/real_corpus/splits/synthetic_seed.train.jsonl`
  - `data/real_corpus/splits/synthetic_seed.val.jsonl`
- BPE-encodes the train split and val split separately
- constructs next-token x/y samples
- uses `sequence_length = min(context_length, 64)`
- uses `batch_size = min(config.training.batch_size, 4)`
- initializes `TinyDecoderOnlyTransformer`
- runs `model.eval()`
- computes one-batch `train_loss` and one-batch `val_loss` under `torch.no_grad()`
- checks that model parameters remain unchanged across the validation smoke

## 4. Observed Result
Observed result from the T6.1 run:
- train docs: `7`
- val docs: `1`
- train tokens: `903`
- val tokens: `399`
- input shape: `(4, 64)`
- logits shape: `(4, 64, 1174)`
- train_loss: `7.304811`
- val_loss: `7.261631`
- both finite: `True`
- parameters unchanged: `True`
- device: `cuda`

Interpretation:
- the split train/val files can both be encoded by the linked BPE tokenizer
- both loss paths are finite in one bounded smoke run
- validation does not update parameters in this implementation path

## 5. What It Does Not Do
This step does not:
- train a tokenizer
- train a model
- run backward
- run an optimizer step
- save a checkpoint
- run generation
- download data
- install packages
- execute `git push`

## 6. Current Limitations
Current limitations:
- this is a one-batch smoke, not a training loop
- it uses only the synthetic seed split files
- the validation split is very small
- no metrics JSONL is written yet
- no training-step scheduling or periodic validation cadence is exercised yet

## 7. Next Step
Recommended next step:
- T7 small real-data training plan
