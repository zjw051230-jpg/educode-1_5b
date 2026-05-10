# EduCode-1.5B

EduCode-1.5B is a small language model training system for CS / ML / Code learning scenarios.

## Current Stage
- Windows engineering fast track has completed the one-step smoke milestone through W10.13
- CUDA, tiny model forward, loss, backward, optimizer step, checkpoint save/load, generation, and run logging have been validated in a bounded smoke path
- The next stage is W11 minimal training loop plan
- The project has not entered long training yet
- The project has not entered A100/B200 main training yet
- BPE, RoPE, FlashAttention-2, MoE, and alignment are not implemented yet

## Hardware Roadmap
- Windows RTX 4060 Ti: engineering fast track
- Mac M3 Max: learning line
- A100: CUDA migration and profiling line
- B200: main 1.5B training line

## Current Scope
This repository currently focuses on:
- project skeleton
- documentation
- configuration placeholders
- experiment organization

## Current Non-goals
This stage does not include:
- MoE
- alignment / RLHF / DPO
- RAG
- Web UI
- service deployment
- multimodality

## Immediate Goal
Build a clean project structure and planning documents before implementing tokenizer, model, or training components.

## Current Milestones
- W1 project skeleton
- W2 CUDA environment check
- W3 config schema draft
- W4 smoke test plan
- W5 run logging format
- W6 config validation checklist
- W7 minimal run manifest templates
- W8 experiment index
- W9 Windows 10M smoke preflight checklist
- W10 Windows 10M smoke implementation plan
- W10.1 config loader only
- W10.2 config validator only
- W10.3 run setup only
- W10.4 toy data + ByteTokenizer only
- W10.5 sequence dataset x/y only
- W10.6 tiny model forward only
- W10.7 loss only
- W10.8 backward + optimizer step only
- W10.9 checkpoint save/load only
- W10.10 generation only
- W10.11 logging integration only
- W10.12 one-step smoke run
- W10.13 one-step smoke review
- W11 minimal training loop plan
