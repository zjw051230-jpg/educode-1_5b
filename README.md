# EduCode-1.5B

A CS336-inspired modular LLM training system, built from scratch and staged from local CUDA smoke tests toward larger-scale dense Transformer experiments.

## Current Status
- Resume MVP is complete.
- Formal training preparation has started.
- Tiny BPE tokenizer artifact created for tokenizer path validation.
- Tiny BPE tokenizer has passed dataset/model/loss integration smoke.
- BPE tokenizer config path validation is now planned/validated via a toy BPE smoke config.
- Legacy smoke config migration is still pending.
- Formal 8k tokenizer and real-data training are still pending.
- Next tokenizer target is BPE 8k for Windows small real-data training.
- ByteTokenizer remains a temporary smoke/debug tokenizer.
- Core pipeline validated: config, data, tokenizer, model, loss, optimizer step, checkpoint, generation, logging.
- Not yet real pretraining, not yet 1.5B, not yet real dataset.

## Quick Demo
Run either of these commands:

```text
python scripts/run_resume_demo.py
```

or

```text
python scripts/run_50_step_toy_training.py
```

## Current Result

| Metric | Value |
|---|---|
| max_steps | 50 |
| first_loss | 9.188724 |
| final_loss | 4.837882 |
| loss_drop | 4.350842 |
| checkpoint reload match | True |
| tokens/sec | 5007.16 |
| generation preview | `helloa nordnad  n otd` |

## Architecture / Pipeline

`config → tokenizer → dataset → model → loss → optimizer → checkpoint → generation → logging`

Current implementation note:
- the current demo uses toy data and a tiny decoder-only model
- the same modular structure is intended to later support tokenizer, data, scale, and hardware upgrades

## Technical Highlights
- Built a modular decoder-only Transformer training pipeline in PyTorch.
- Implemented config loading and validation, byte-level tokenization, x/y sequence batching, model forward, next-token loss, optimizer step, checkpoint save/load, autoregressive generation, and run logging.
- Validated the end-to-end pipeline on an RTX 4060 Ti with one-step smoke, 10-step minimal loop, and bounded 50-step toy training milestones.
- Produced reproducible run artifacts including `run_config.json`, `run_metadata.json`, `metrics.jsonl`, `generation_samples.jsonl`, checkpoint manifest files, and markdown summaries.
- Added guardrails so generated artifacts remain Git-ignored and bounded runs do not silently turn into larger experiments.

## Limitations
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

## Roadmap
- T1 formal training roadmap
- T2 BPE tokenizer plan
- BPE tokenizer integration
- RoPE integration
- real dataset pipeline
- validation loop
- learning-rate scheduler
- resume training test
- A100 100M profiling
- B200 1.5B pretraining experiment

## Resume Resources
- [Resume Bullets](docs/resume_bullets.md)
- [Resume Project Report](docs/resume_project_report.md)
- [Quickstart](docs/quickstart.md)
- [Reproducibility Checklist](docs/reproducibility_checklist.md)
- [Public Showcase Checklist](docs/public_showcase_checklist.md)

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
- W11.1 minimal training loop script
- W11.2 minimal training loop review
- W11.3 bounded 50-step toy training plan
- W11.4 bounded 50-step toy training
- W11.5 bounded 50-step toy training review
- R1 resume MVP pack
- T1 formal training roadmap
- T2 BPE tokenizer plan
- T2.1 tokenizer environment check
- T2.2 tiny BPE tokenizer artifact
- T2.3 BPE tokenizer integration smoke
- T2.4 tokenizer config schema update
