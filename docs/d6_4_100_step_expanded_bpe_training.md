# D6.4 Bounded 100-Step Expanded BPE Training

## 1. Purpose
The purpose of D6.4 is to implement and run the next bounded local training stage on the expanded synthetic corpus train/validation split files using the linked `educode_bpe_expanded_8k` tokenizer artifact and the existing tiny decoder-only model path.

This step remains intentionally narrow.
It does not introduce external data, larger hardware, tokenizer retraining, or model-architecture changes.

## 2. Files Added
- `scripts/run_100_step_expanded_bpe_training.py`
- `docs/d6_4_100_step_expanded_bpe_training.md`

Ignored run artifacts were generated under:
- `experiments/windows_cuda/20260515_023640_windows_cuda_100_step_expanded_bpe_training/`

## 3. What It Does
This step:
- loads `configs/windows/bpe_expanded_8k_smoke.json`
- validates the config with `repo_root=PROJECT_ROOT`
- loads `tokenizers/educode_bpe_expanded_8k/tokenizer.json`
- reads:
  - `data/real_corpus/splits/synthetic_expanded.train.jsonl`
  - `data/real_corpus/splits/synthetic_expanded.val.jsonl`
- BPE-encodes the train and val text separately
- builds next-token x/y batches with `sequence_length = min(config context_length, config training sequence_length)`
- uses `batch_size = min(config.training.batch_size, 4)`
- initializes `TinyDecoderOnlyTransformer`
- runs exactly `100` optimizer steps with `AdamW`
- computes validation loss every `10` steps under `model.eval()` and `torch.no_grad()`
- writes `metrics.jsonl` on every training step, with `val_loss` populated on eval steps
- saves `checkpoint_final.pt`
- reloads the checkpoint and verifies parameter equality
- writes `summary.md`, `run_metadata.json`, and `run_config.json`
- does not make any generation-quality claim

## 4. Test Command
Executed command:

```text
.venv/Scripts/python.exe scripts/run_100_step_expanded_bpe_training.py
```

## 5. Observed Result
Observed result from the D6.4 run:
- run_id: `20260515_023640_windows_cuda_100_step_expanded_bpe_training`
- run_dir: `D:/模型/educode-1_5b/experiments/windows_cuda/20260515_023640_windows_cuda_100_step_expanded_bpe_training`
- device: `cuda`
- max_steps: `100`
- train docs: `13`
- val docs: `2`
- tokenizer vocab size: `1846`
- first_train_loss: `7.689178`
- final_train_loss: `3.109032`
- final_val_loss: `7.552639`
- loss_all_finite: `True`
- val_loss_all_finite: `True`
- checkpoint reload match: `True`
- metrics rows: `100`
- validation rows: `10`
- run artifacts remained Git-ignored

## 6. Learning Note
- the expanded synthetic train/val split, expanded BPE tokenizer, tiny model, optimizer step, checkpoint, and structured logging remain connected across a longer bounded local training run
- train loss decreased substantially across the `100`-step run, which confirms the local optimization path continued to function under the longer bounded budget
- validation loss stayed finite at every scheduled evaluation point, but the validation split is still too small for any model-quality interpretation
- this remains expanded synthetic corpus validation work, not formal large-scale pretraining

## 7. Current Limitations
- expanded synthetic corpus only
- not external real-world data
- observed tokenizer vocab is `1846`, not the original target `8192`
- tiny model only
- validation split contains only two documents
- learned position embeddings are still used in the current tiny model path
- this is still not formal large-scale pretraining or a meaningful model-quality result

## 8. What It Does Not Do
This step does not:
- use external data
- copy external corpora
- retrain the tokenizer
- do A100/B200
- do 1.5B
- change model architecture
- install packages
- perform `git push`
- commit run artifacts from `experiments/`

## 9. Next Step
Recommended next step:
- review the bounded 100-step expanded-BPE training artifacts before any longer run or any move beyond the current synthetic corpus
