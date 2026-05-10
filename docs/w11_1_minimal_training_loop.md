# W11.1 Minimal Training Loop Script

## 1. Purpose
This step implements and runs a strictly bounded minimal training loop.

## 2. Files Added
- `scripts/run_minimal_training_loop.py`

## 3. What It Does
This step:
- loads config
- validates config
- creates a run directory
- prepares toy data
- tokenizes the corpus
- builds batches
- initializes the tiny model
- runs `max_steps <= 10`
- logs metrics
- saves a final checkpoint
- reloads the checkpoint for a sanity check
- runs final generation
- writes a summary

## 4. What It Does Not Do
This step does not:
- use real data
- download data
- download models
- do long training
- do A100/B200
- do 1.5B
- do validation loop
- do scheduler
- do gradient accumulation
- do mixed precision
- do distributed training
- do BPE / RoPE / FlashAttention-2 / MoE / alignment / RAG / Web UI

## 5. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/run_minimal_training_loop.py
```

## 6. Observed Result
- run_id: `20260511_041027_windows_cuda_minimal_training_loop`
- run_dir: `D:/Projects/educode-1_5b/experiments/windows_cuda/20260511_041027_windows_cuda_minimal_training_loop`
- device: `cuda`
- max_steps: `10`
- first_loss: `9.139446`
- final_loss: `8.856288`
- loss_all_finite: `True`
- grad_all_finite: `True`
- checkpoint exists: `True`
- checkpoint reload match: `True`
- generation preview: `hello�a`
- metrics exists: `True`
- summary exists: `True`
- experiments/ remained ignored by Git

## 7. Learning Note
- one-step smoke only proves the path can run once
- minimal training loop proves the same path can repeat safely for a small number of steps
- loss may be unstable because the toy corpus is tiny, the model starts random, and the run is extremely short
- this result must not be interpreted as the model already being trained well
- real training still needs real data, tokenizer integration, validation, scheduler support, checkpoint resume, and longer runs

## 8. Current Limitations
- toy data only
- ByteTokenizer temporary path
- config still declares BPE/8192
- learned positional embedding, not RoPE
- SDPA only, not FlashAttention-2
- tiny model only, not 1.5B
- no validation set
- no meaningful generation quality

## 9. Next Step
Suggested W11.2:
- minimal training loop review
- inspect metrics, artifacts, docs, and experiment index
- then decide whether to move to 50-step/100-step toy training or back to the Mac learning line
