# EduCode-1.5B Project Plan

## 1. Project Theme
EduCode-1.5B is a small language model training system for CS / ML / Code learning scenarios. The project is intended to help the user understand the full engineering path from data and tokenizer design to dense Transformer training, evaluation, and scaling experiments.

## 2. Project Goal
The goal is to build a resume-worthy project based on the CS336 assignment style workflow, covering tokenizer, dense Transformer, training loop, checkpointing, generation, profiling, and the final path toward a 1.5B training experiment. The focus is on learning-by-building with clear engineering structure rather than pretending to reach frontier-scale SOTA results.

## 3. Hardware Roadmap
- **Windows RTX 4060 Ti 16GB**: engineering fast track, local inference, LoRA, and small-model smoke tests.
- **Mac M3 Max 36GB**: learning slow line for Apple Silicon / MPS understanding and small-model principle validation.
- **A100 40G/80G**: CUDA migration and 100M / 300M profiling experiments.
- **B200**: main training platform for the 1.5B model.
- **Optional multi-B200**: DDP / FSDP experiments after the single-device path is stable.

## 4. Model Roadmap
- **10M-40M**: Mac learning and validation models.
- **100M-300M**: A100 smoke tests and profiling models.
- **1.5B**: main B200 target model.
- **3B**: future stretch target, not part of the current stage.

## 5. 1.5B Model Draft Config
- decoder-only dense Transformer
- vocab size 32k
- context length 2048 to start
- RMSNorm
- RoPE
- SwiGLU
- causal attention
- bf16
- FlashAttention / SDPA
- AdamW baseline
- Muon optimizer ablation

## 6. Token Budget
- **5B tokens**: minimum deliverable training run.
- **10B tokens**: recommended formal version.
- **30B tokens**: more complete version.

This project does not claim SOTA ambition. The token budgets are meant for a course-style engineering project and a resume project, not for frontier model competition.

## 7. Technical Highlights
- byte-level BPE tokenizer
- LLaMA-style dense Transformer
- bf16 training
- checkpoint / resume
- generation
- validation loss
- Mac MPS profiling
- A100 CUDA profiling
- FlashAttention-2 / SDPA / naive attention comparison
- activation checkpointing
- AdamW vs Muon
- RoPE vs YaRN
- MFU / tokens/sec / memory profiling
- 100M / 300M / 1.5B scaling curve

## 8. Current Non-goals
The current phase does not include:
- MoE
- RLHF / DPO / alignment
- RAG
- Web UI
- service deployment
- multimodality
- large-scale distributed training
- direct 1.5B training on the 4060 Ti

## 9. Windows Line Role
The Windows line is responsible for:
- project skeleton
- documentation
- configuration
- local inference
- LoRA / PEFT small experiments
- small-model smoke tests

The Windows line is not responsible for formal 1.5B training.

## 10. Mac Line Role
The Mac line is responsible for:
- gradually learning tokenizer, model, and training internals
- understanding Apple Silicon / MPS behavior
- small-model training validation

## 11. Resume Bullet Draft
- Built EduCode-1.5B, a modular small-language-model training system for CS / ML / code learning, spanning tokenizer, dense Transformer, checkpointing, generation, and profiling workflows.
- Designed a multi-hardware training roadmap across Windows RTX 4060 Ti, Apple Silicon MPS, A100, and B200 to de-risk scaling from small-model validation to 1.5B training experiments.
- Structured experiment tracks for attention kernel comparison, optimizer ablations, memory profiling, and scaling-curve analysis across 100M, 300M, and 1.5B model sizes.

## 12. Next Engineering Step
W2 should verify PyTorch CUDA availability and add minimal environment validation scripts, while still avoiding the main training pipeline implementation.
