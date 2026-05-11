# EduCode-1.5B Resume Project Report

## 1. Project Summary
EduCode-1.5B is a CS336-inspired small language model training system built from scratch, focusing on the core dense Transformer training pipeline before scaling to larger GPU experiments.

The current completed scope includes:
- Windows RTX 4060 Ti engineering fast track
- tiny dense decoder-only model
- toy-data training pipeline
- config validation
- logging
- checkpoint
- generation
- bounded 50-step toy training demo

This project does not yet claim:
- completed 1.5B training
- real large-scale dataset training
- formal LLM pretraining results

## 2. What Was Built
- Project skeleton
- JSON config schema
- CUDA environment checker
- Config loader / validator
- ByteTokenizer
- Toy corpus
- Sequence dataset x/y builder
- Tiny decoder-only Transformer
- RMSNorm
- Causal SDPA attention
- SwiGLU MLP
- Next-token cross entropy
- AdamW optimizer step
- Checkpoint save/load
- Autoregressive generation
- Run logging
- One-step smoke run
- 10-step minimal training loop
- 50-step bounded toy training run

## 3. Current Demo Result
- hardware: Windows RTX 4060 Ti 16GB
- device: `cuda`
- run_id: `20260511_044948_windows_cuda_bounded_50_step_toy`
- max_steps: `50`
- first_loss: `9.188724`
- final_loss: `4.837882`
- min_loss: `4.239685`
- max_loss: `9.188724`
- mean_loss: `6.944143`
- loss_drop: `4.350842`
- loss_all_finite: `True`
- grad_all_finite: `True`
- tokens_seen: `3200`
- approximate tokens/sec: `5007.161023`
- checkpoint reload match: `True`
- metrics rows: `50`
- generation preview: `helloa nordnad  n otd`

## 4. Technical Highlights
- Implemented a decoder-only dense Transformer training stack from scratch in PyTorch.
- Built modular components for config validation, toy data tokenization, sequence batching, model forward, loss computation, optimizer step, checkpointing, generation, and run logging.
- Validated the full training pipeline on RTX 4060 Ti with a bounded 50-step toy-data run.
- Implemented reproducible experiment artifacts: `run_config.json`, `run_metadata.json`, `metrics.jsonl`, `generation_samples.jsonl`, checkpoint manifest, and `summary.md`.
- Added safeguards to prevent accidental large-run execution and avoid committing generated checkpoints.

## 5. Architecture Overview
Pipeline:

`config → tokenizer → toy data → sequence dataset → tiny decoder-only Transformer → logits → loss → backward → optimizer step → checkpoint → generation → logging`

Current notes:
- the current implementation uses a tiny model
- the pipeline can later swap tokenizer, data source, model scale, and hardware backend

## 6. What This Project Demonstrates
- End-to-end LLM training pipeline understanding
- PyTorch model implementation
- CUDA smoke testing
- Training loop design
- Experiment reproducibility
- Checkpoint/reload correctness
- Logging discipline
- Engineering boundaries for scaling

## 7. Current Limitations
- toy data only
- ByteTokenizer temporary path
- config declares BPE/8192 but the current smoke path uses byte ids
- learned position embeddings, not RoPE
- PyTorch SDPA only, not FlashAttention-2
- tiny model only, not 1.5B
- no real dataset
- no validation set
- no meaningful generation quality
- no A100/B200 experiments yet

## 8. Next Engineering Steps
- BPE tokenizer integration
- RoPE integration
- real dataset pipeline
- validation loop
- learning-rate scheduler
- resume training test
- A100 100M profiling
- B200 1.5B pretraining experiment

## 9. Resume-Safe Description
Built EduCode-1.5B, a CS336-inspired modular LLM training system in PyTorch. Implemented the core dense Transformer training pipeline including config validation, tokenization, sequence batching, model forward, next-token loss, optimizer step, checkpoint save/load, generation, and structured experiment logging. Validated the pipeline on an RTX 4060 Ti with a bounded 50-step toy-data run, reducing loss from 9.19 to 4.84 while keeping all run artifacts reproducible and checkpoint-safe.
