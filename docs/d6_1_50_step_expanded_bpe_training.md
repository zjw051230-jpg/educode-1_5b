# D6.1 Bounded 50-Step Expanded BPE Training

## 1. Purpose
The purpose of D6.1 is to implement and run the first bounded small-training stage on the expanded synthetic corpus train/validation split files using the linked `educode_bpe_expanded_8k` tokenizer artifact and the existing tiny decoder-only model path.

This step remains intentionally narrow.
It does not introduce external data, larger hardware, longer training, generation claims, or model-architecture changes.

## 2. Files Added
- `scripts/run_50_step_expanded_bpe_training.py`
- `docs/d6_1_50_step_expanded_bpe_training.md`

Ignored run artifacts were generated under:
- `experiments/windows_cuda/20260515_014657_windows_cuda_50_step_expanded_bpe_training/`

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
- runs exactly `50` optimizer steps with `AdamW`
- computes validation loss every `10` steps under `model.eval()` and `torch.no_grad()`
- writes `metrics.jsonl` on every training step, with `val_loss` populated on eval steps
- saves `checkpoint_final.pt`
- reloads the checkpoint and verifies parameter equality
- writes `summary.md`, `run_metadata.json`, and `run_config.json`

## 4. Test Command
Executed command:

```text
.venv/Scripts/python.exe scripts/run_50_step_expanded_bpe_training.py
```

## 5. Observed Result
Observed result from the D6.1 run:
- run_id: `20260515_014657_windows_cuda_50_step_expanded_bpe_training`
- run_dir: `D:/模型/educode-1_5b/experiments/windows_cuda/20260515_014657_windows_cuda_50_step_expanded_bpe_training`
- device: `cuda`
- max_steps: `50`
- eval_interval: `10`
- train docs: `13`
- val docs: `2`
- train tokens: `2142`
- val tokens: `503`
- sequence_length: `128`
- batch_size: `4`
- first_train_loss: `7.633180`
- final_train_loss: `4.182922`
- final_val_loss: `7.184383`
- loss_all_finite: `True`
- val_loss_all_finite: `True`
- grad_all_finite: `True`
- final_grad_norm: `1.340357`
- tokens_seen: `25600`
- elapsed_seconds: `1.486907`
- approximate tokens/sec: `17216.945349`
- checkpoint exists: `True`
- checkpoint reload match: `True`
- metrics rows: `50`
- validation rows: `5`
- summary exists: `True`
- run artifacts remained Git-ignored

## 6. Learning Note
- the expanded synthetic train/val split, expanded BPE tokenizer, tiny model, optimizer step, checkpoint, and structured logging now connect inside one bounded local training run
- train loss decreases substantially inside this tiny bounded run, which shows the local optimization path is functioning on the expanded-corpus path
- validation loss stays finite but noisy because the corpus and validation split are still extremely small
- no generation sample is produced in this step, and no model quality claim should be made from these metrics

## 7. Current Limitations
- expanded synthetic corpus only
- not external real-world data
- observed tokenizer vocab is `1846`, not the original target `8192`
- tiny model only
- validation split contains only two documents
- learned position embeddings are still used in the current tiny model path
- no scheduler, resume-training test, long-run stability test, or larger-scale hardware path is exercised here

## 8. What It Does Not Do
This step does not:
- use external data
- do long training
- do A100/B200
- do 1.5B
- change model architecture
- install packages
- perform `git push`
- commit run artifacts from `experiments/`

## 9. Next Step
Recommended next step:
- review the bounded expanded-BPE training artifacts before any longer run or any move beyond the current synthetic corpus
