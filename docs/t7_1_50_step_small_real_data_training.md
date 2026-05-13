# T7.1 Bounded 50-Step Small Real-Data Training

## 1. Purpose
The purpose of T7.1 is to implement and run the first bounded small-training stage on the current synthetic-seed train/validation split files using the linked `educode_bpe_8k` tokenizer artifact and the existing tiny decoder-only model path.

This step is still intentionally narrow.
It does not introduce external data, larger hardware, longer training, or model-architecture changes.

## 2. Files Added
- `scripts/run_50_step_small_real_data_training.py`
- `docs/t7_1_50_step_small_real_data_training.md`

Ignored run artifacts were generated under:
- `experiments/windows_cuda/20260514_024451_windows_cuda_50_step_small_real_data_training/`

## 3. What It Does
This step:
- loads `configs/windows/bpe_8k_formal_placeholder.json`
- validates the config with `repo_root=PROJECT_ROOT`
- loads `tokenizers/educode_bpe_8k/tokenizer.json`
- reads:
  - `data/real_corpus/splits/synthetic_seed.train.jsonl`
  - `data/real_corpus/splits/synthetic_seed.val.jsonl`
- BPE-encodes the train and val text separately
- builds next-token x/y batches with `sequence_length = min(config, 64)`
- uses `batch_size = min(config.training.batch_size, 4)`
- initializes `TinyDecoderOnlyTransformer`
- runs exactly `50` optimizer steps with `AdamW`
- computes validation loss every `10` steps under `model.eval()` and `torch.no_grad()`
- writes `metrics.jsonl` on every training step, with `val_loss` populated on eval steps
- saves `checkpoint_final.pt`
- reloads the checkpoint and verifies parameter equality
- writes a final generation sample to `generation_samples.jsonl`
- writes `summary.md` and `checkpoints_manifest.json`

## 4. Test Command
Executed command:

```text
.venv/Scripts/python.exe scripts/run_50_step_small_real_data_training.py
```

## 5. Observed Result
Observed result from the T7.1 run:
- run_id: `20260514_024451_windows_cuda_50_step_small_real_data_training`
- run_dir: `D:/模型/educode-1_5b/experiments/windows_cuda/20260514_024451_windows_cuda_50_step_small_real_data_training`
- device: `cuda`
- max_steps: `50`
- eval_interval: `10`
- train docs: `7`
- val docs: `1`
- train tokens: `903`
- val tokens: `399`
- sequence_length: `64`
- batch_size: `4`
- first_train_loss: `7.192344`
- final_train_loss: `4.074500`
- final_val_loss: `7.380465`
- min_train_loss: `3.376844`
- max_train_loss: `7.192344`
- mean_train_loss: `4.072679`
- min_val_loss: `7.268392`
- max_val_loss: `7.696991`
- mean_val_loss: `7.415411`
- loss_all_finite: `True`
- grad_all_finite: `True`
- final_grad_norm: `2.583328`
- tokens_seen: `12800`
- elapsed_seconds: `1.899621`
- approximate tokens/sec: `6738.186196`
- checkpoint exists: `True`
- checkpoint reload match: `True`
- metrics rows: `50`
- validation rows: `5`
- summary exists: `True`
- generation preview starts with: `def hello_world(): "deep learning uses"`
- run artifacts remained Git-ignored

## 6. Learning Note
- the bounded train loop can now reuse the linked BPE tokenizer artifact and synthetic-seed split files without falling back to ByteTokenizer toy data
- train loss decreases substantially inside this tiny bounded run, which shows the local optimization path is functioning
- validation loss stays finite but noisy because the corpus and validation split are extremely small
- the generated text is only a pipeline sanity check and does not indicate real model quality

## 7. Current Limitations
- synthetic seed corpus only
- not external real-world data
- observed tokenizer vocab is `1174`, not the original target `8192`
- tiny model only
- validation split contains only one document
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
- review the bounded small-training artifacts before any longer run or any move beyond the synthetic-seed corpus
