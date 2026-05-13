# T8 A100 100M Scaling Plan

## 1. Purpose
The purpose of T8 is to plan the transition from the current local tiny/synthetic pipeline to an A100 100M-scale experiment line.

## 2. Current Baseline
Current baseline state:
- BPE tokenizer path validated
- observed vocab size = `1174`
- synthetic seed corpus processed
- train/val split exists
- validation loop works
- 50-step and 100-step small training completed
- checkpoint reload works
- logging works
- current limitation: tiny synthetic corpus overfits quickly

## 3. Why A100 / 100M Next
Why A100 / 100M is the next step:
- the local pipeline has already passed bounded training, validation, checkpoint, and logging checks
- we should not keep stacking more steps on the tiny synthetic corpus
- the next stage should validate a larger model configuration, GPU memory behavior, tokens/sec, checkpointing, and structured logging under datacenter-scale hardware assumptions
- an A100 100M-scale experiment is a practical intermediate layer before any 300M, B200, or 1.5B path

## 4. Target Experiment
Target experiment definition:
- hardware: A100 40GB or 80GB
- model size target: around 100M parameters
- architecture: dense decoder-only Transformer
- tokenizer: current BPE path initially, then retrain later on a larger permitted corpus
- context_length: `256` or `512`
- goal: scaling/profiling smoke, not final model quality

## 5. Model Config Proposal
Initial model config proposal:
- vocab_size: use the current tokenizer vocab for early smoke, or future `8k` / `16k` after a better corpus path exists
- num_layers: `12`
- d_model: `768`
- num_heads: `12`
- d_ff: `3072`
- context_length: `512`
- dropout: `0.0` or a small value
- attention_backend: `sdpa`

This is an initial proposal only.
T8.1 is the stage that should turn it into an actual config draft.

## 6. Data Requirement Before Real A100 Run
Data requirement before any real A100 run:
- the current synthetic corpus is not enough to support meaningful 100M training
- an A100 run should require an expanded permitted corpus first for any real training intent
- a config/profiling smoke can still come before the full data path is ready
- no one should present this as formal pretraining quality

## 7. Metrics to Track
Metrics to track in the A100 line:
- train_loss
- val_loss
- tokens/sec
- GPU memory allocated/reserved
- step time
- checkpoint size
- checkpoint reload
- generation sample
- OOM status

## 8. Run Ladder
Planned A100 ladder:
- T8.1 A100 100M config draft
- T8.2 A100 environment preflight checklist
- T8.3 100M forward/loss smoke
- T8.4 100M 10-step training smoke
- T8.5 100M profiling report
- T9 300M plan

## 9. Guardrails
Guardrails for this stage:
- not B200
- not 1.5B
- not production training
- not claiming model quality
- no large run before config, environment, and data checks pass

## 10. Next Step
Recommended next step:
- T8.1: create A100 100M config draft
