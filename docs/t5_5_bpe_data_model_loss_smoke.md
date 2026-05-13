# T5.5 BPE Data/Model/Loss Smoke

## 1. Purpose
The purpose of T5.5 is to validate the minimal processed-data → BPE tokenizer → model forward → loss path using the current synthetic seed corpus outputs and the linked `educode_bpe_8k` tokenizer artifact.

This step stays strictly at smoke level.
It does not perform backward, optimizer stepping, checkpoint saving, or generation.

## 2. Files Added
- `scripts/inspect_bpe_data_model_loss_smoke.py`
- `docs/t5_5_bpe_data_model_loss_smoke.md`

## 3. What It Does
This smoke script:
- loads `configs/windows/bpe_8k_formal_placeholder.json`
- validates the config with `repo_root=PROJECT_ROOT`
- loads `tokenizers/educode_bpe_8k/tokenizer.json`
- reads `data/real_corpus/processed/synthetic_seed.processed.jsonl`
- uses only `split == "train"` text
- BPE-encodes the train corpus text
- constructs next-token x/y samples
- uses `sequence_length = min(context_length, 64)`
- uses `batch_size = min(config.training.batch_size, 4)`
- initializes `TinyDecoderOnlyTransformer`
- runs `model.eval()` with `torch.no_grad()`
- computes forward logits and next-token cross-entropy loss

## 4. Observed Result
Observed result from the T5.5 run:
- train docs: `7`
- total token count: `903`
- sequence_length: `64`
- batch_size: `4`
- input_ids shape: `(4, 64)`
- logits shape: `(4, 64, 1174)`
- loss value: `7.221643`
- loss finite: `True`
- device: `cuda`

Interpretation:
- the processed synthetic train corpus can be encoded by the linked BPE tokenizer
- the token ids can enter the model successfully
- the model head shape matches the linked vocab size `1174`
- the loss is finite and near the expected random-init baseline for this vocabulary size

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
- this uses only the synthetic seed processed corpus
- it is only a smoke path, not a learning or convergence result
- the observed tokenizer vocabulary is still `1174`, not the original target `8192`
- the corpus remains too small to represent real-data training behavior
- no validation loop is exercised in this step

## 7. Next Step
Recommended next step:
- T6 validation loop plan
