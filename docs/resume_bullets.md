# Resume Bullets

## Short Version
- Built a CS336-inspired modular LLM training system in PyTorch, implementing config validation, tokenization, sequence batching, dense Transformer forward pass, next-token loss, optimizer step, checkpointing, generation, and experiment logging.
- Validated the full training pipeline on an RTX 4060 Ti with a bounded 50-step toy-data run, reducing loss from 9.19 to 4.84 and verifying checkpoint reload correctness.
- Designed the project for staged scaling from local CUDA smoke tests to A100/B200 experiments, with reproducible configs, JSONL metrics, and clear non-goals for MoE/alignment/RAG.

## More Engineering-Focused Version
- Built a modular PyTorch training codebase for a decoder-only dense Transformer, with separated components for config loading, validation, tokenization, batching, model forward, loss, checkpointing, generation, and structured run logging.
- Implemented reproducible experiment outputs including `run_config.json`, `run_metadata.json`, `metrics.jsonl`, `generation_samples.jsonl`, checkpoint manifest files, and markdown summaries.
- Added guardrails around bounded smoke and toy-training runs so generated artifacts stay Git-ignored and local engineering iterations do not accidentally turn into large runs.
- Validated the end-to-end pipeline on a Windows RTX 4060 Ti by completing one-step smoke, 10-step minimal loop, and bounded 50-step toy training milestones.
- Packaged the project with a single demo entry point and resume-safe documentation for reproducible presentation.

## More ML-Systems-Focused Version
- Implemented a CS336-inspired decoder-only Transformer stack in PyTorch with RMSNorm, causal SDPA attention, SwiGLU feed-forward blocks, and next-token cross-entropy training.
- Built the surrounding ML systems pipeline for toy-data experimentation: ByteTokenizer, x/y sequence dataset construction, AdamW training loop, checkpoint save/load, autoregressive generation, and structured metrics logging.
- Verified training-loop stability on CUDA with a bounded 50-step toy-data run on an RTX 4060 Ti, reducing loss from 9.19 to 4.84 while keeping losses and gradient norms finite.
- Implemented checkpoint reload sanity checks and experiment manifests to validate reproducibility and artifact discipline.
- Structured the repo for later scaling to real tokenizer integration, real datasets, A100 profiling, and eventual B200 1.5B experiments without overstating the current milestone.

## Honest Scope Notes
- toy-data run, not full pretraining
- tiny model, not final 1.5B
- engineering pipeline milestone
