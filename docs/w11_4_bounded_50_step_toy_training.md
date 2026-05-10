# W11.4 Bounded 50-Step Toy Training

## 1. Purpose
This step implements and runs bounded 50-step toy training.

## 2. Files Added
- `scripts/run_50_step_toy_training.py`

## 3. What It Does
This step:
- loads config
- validates config
- creates a run directory
- prepares the toy corpus
- tokenizes the corpus
- builds x/y batches
- initializes the tiny model
- runs exactly 50 steps
- logs metrics on every step
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
- do BPE / RoPE / FlashAttention-2
- do MoE / alignment / RAG / Web UI

## 5. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/run_50_step_toy_training.py
```

## 6. Observed Result
- run_id: `20260511_044948_windows_cuda_bounded_50_step_toy`
- run_dir: `D:/Projects/educode-1_5b/experiments/windows_cuda/20260511_044948_windows_cuda_bounded_50_step_toy`
- device: `cuda`
- max_steps: `50`
- first_loss: `9.188724`
- final_loss: `4.837882`
- min_loss: `4.239685`
- max_loss: `9.188724`
- mean_loss: `6.944143`
- loss_all_finite: `True`
- grad_all_finite: `True`
- final_grad_norm: `4.178667`
- tokens_seen: `3200`
- elapsed_seconds: `0.639085`
- approximate tokens/sec: `5007.161023`
- checkpoint exists: `True`
- checkpoint reload match: `True`
- generation preview: `helloa nordnad  n otd`
- metrics rows: `50`
- summary exists: `True`
- experiments/ remained ignored by Git

## 7. Learning Note
- the 10-step loop proved the smallest repeated training path could run safely
- the 50-step toy run further validates stability and logging completeness
- the toy corpus is far too small, so loss movement does not prove model capability
- generation quality is still not meaningful
- real training still needs a real tokenizer path, real data, validation, scheduler support, checkpoint resume, and more steps

## 8. Current Limitations
- toy data only
- ByteTokenizer temporary path
- config still declares BPE/8192
- learned position embedding, not RoPE
- PyTorch SDPA only
- tiny model only
- no validation set
- no meaningful generation quality
- still not a real language model training run

## 9. Next Step
Suggested W11.5:
- bounded 50-step toy training review
- inspect metrics, loss trend, checkpoint, generation, summary, and experiment index
- then decide whether to do a 100-step toy run or return to the Mac learning line for theory
