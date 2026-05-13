# T7.4 Bounded 100-Step Small Real-Data Training

## 1. Purpose
The purpose of T7.4 is to implement and run a strictly bounded 100-step small-training stage using the existing synthetic-seed split files, linked BPE tokenizer artifact, and current tiny dense model path.

This step stays local and bounded.
It does not use external real-world data, does not change the model, and does not claim model quality.

## 2. Files Added
- `scripts/run_100_step_small_real_data_training.py`
- `docs/t7_4_100_step_small_real_data_training.md`

Ignored run artifacts were generated under:
- `experiments/windows_cuda/20260514_030554_windows_cuda_100_step_small_real_data_training/`

## 3. What It Does
This step:
- loads `configs/windows/bpe_8k_formal_placeholder.json`
- validates the config with `repo_root=PROJECT_ROOT`
- loads `tokenizers/educode_bpe_8k/tokenizer.json`
- reads:
  - `data/real_corpus/splits/synthetic_seed.train.jsonl`
  - `data/real_corpus/splits/synthetic_seed.val.jsonl`
- BPE-encodes the train and val text separately
- builds next-token x/y batches
- uses the same tiny dense model path as T7.1
- runs exactly `100` optimizer steps
- evaluates validation loss every `10` steps
- writes `metrics.jsonl`
- saves `checkpoint_final.pt`
- reloads the checkpoint and checks parameter equality
- writes `generation_samples.jsonl`
- writes `summary.md`

## 4. Test Command
Executed command:

```text
D:/模型/educode-1_5b/.venv/Scripts/python.exe scripts/run_100_step_small_real_data_training.py
```

## 5. Observed Result
Observed run result:
- run_id: `20260514_030554_windows_cuda_100_step_small_real_data_training`
- device: `cuda`
- max_steps: `100`
- eval_interval: `10`
- first_train_loss: `7.206174`
- final_train_loss: `3.113705`
- final_val_loss: `8.295060`
- min_train_loss: `2.924466`
- max_train_loss: `7.206174`
- mean_train_loss: `3.734624`
- checkpoint reload match: `True`
- metrics rows: `100`
- validation rows: `10`
- generation preview:

```text
def hello_world():
- stay explicitly separate from real-world external corpora
- tokenizer, cleaning, tokenizer, cleaning, cleaning, tokenizer, tokenizer, cleaning, and small data
```

## 6. Interpretation
Interpretation:
- train loss remained finite and decreased across the bounded run
- validation loss remained finite across all scheduled evaluation points
- the checkpoint reload sanity check passed
- generation output exists and confirms the post-training generation path completed
- this remains a synthetic-seed bounded experiment, not a large-scale real-corpus training result

## 7. Current Limitations
Current limitations:
- synthetic seed corpus only
- not large-scale real data
- validation split still contains only one document
- observed tokenizer vocab is `1174`
- not A100/B200
- not 1.5B
- no claim should be made about model quality or generalization

## 8. Next Step
Recommended next step:
- T7.5 100-step small training review
