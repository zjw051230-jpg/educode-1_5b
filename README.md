# EduCode-1.5B

A CS336-inspired modular LLM training system, built from scratch and staged from local CUDA smoke tests toward larger-scale dense Transformer experiments.

## Current Status
- Resume MVP is complete.
- Formal training preparation has started.
- Tiny BPE tokenizer artifact created for tokenizer path validation.
- Tiny BPE tokenizer has passed dataset/model/loss integration smoke.
- Tokenizer configs have been split into byte smoke, toy BPE smoke, and formal BPE placeholder.
- Toy BPE tokenizer config path validation is now covered by a dedicated smoke config.
- Formal `educode_bpe_8k` tokenizer artifact has been created from the current synthetic seed corpus.
- The formal BPE config is linked to the observed tokenizer vocab size `1174`.
- BPE processed-data model/loss smoke has passed.
- One-batch train/val validation-loop smoke has passed.
- A bounded 50-step synthetic-seed small training run has completed with periodic validation, checkpoint reload, generation output, and structured logs.
- An A100 100M draft config has been created and passes read-only config inspection against the current validator.
- This A100 draft still uses the current observed tokenizer vocab size `1174` from the current `educode_bpe_8k` tokenizer artifact trained on the synthetic seed corpus.
- An A100 first-session command checklist has been prepared for the selected single `A100 80GB` provider path.
- A100 80GB single-GPU smoke path validated up to 2.15B-scale optimizer profiling.
- Current result is engineering/scaling validation, not full pretraining.
- After A100 scaling validation, the next bottleneck is permitted corpus scale and tokenizer quality.
- Since no existing local notes are available, the first approved source is a project-authored synthetic educational seed corpus.
- This is not external real-world training data.
- ByteTokenizer remains a legacy smoke/debug tokenizer path.
- Core pipeline validated: config, data, tokenizer, model, loss, optimizer step, checkpoint, generation, logging, and periodic validation.
- Not yet real pretraining, not yet 1.5B, not yet external real dataset.

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
| eval_interval | 10 |
| first_train_loss | 7.192344 |
| final_train_loss | 4.074500 |
| final_val_loss | 7.380465 |
| checkpoint reload match | True |
| tokens/sec | 6738.19 |
| generation preview | `def hello_world(): "deep learning uses"` |

## Architecture / Pipeline

`config → tokenizer → dataset → model → loss → optimizer → checkpoint → generation → logging`

Current implementation note:
- the current demo uses toy data and a tiny decoder-only model
- the same modular structure is intended to later support tokenizer, data, scale, and hardware upgrades

## Technical Highlights
- Built a modular decoder-only Transformer training pipeline in PyTorch.
- Implemented config loading and validation, byte-level tokenization, x/y sequence batching, model forward, next-token loss, optimizer step, checkpoint save/load, autoregressive generation, and run logging.
- Validated the end-to-end pipeline on an RTX 4060 Ti with one-step smoke, 10-step minimal loop, and bounded 50-step toy training milestones.
- Validated 100M/300M training smoke and 2.15B-scale optimizer profiling on a single A100 80GB.
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
- no B200 experiments yet

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
- T2.5 tokenizer config migration
- T3 small real dataset plan
- T4 real corpus intake structure
- T4.1 first corpus source decision
- T4.2S synthetic seed corpus source decision
- T4.3 synthetic seed corpus
- T5 real data intake cleaning script plan
- T5.1 synthetic seed intake cleaning script
- T5.2 BPE 8k tokenizer training plan
- T5.3 BPE 8k tokenizer artifact
- T5.4 BPE 8k config linkage validation
- T5.5 BPE data/model/loss smoke
- T6 validation loop plan
- T6.1 validation loop smoke
- T7 small real-data training plan
- T7.1 bounded 50-step small real-data training
- T7.2 50-step small training review
- T7.3 bounded 100-step small training plan
- T7.4 bounded 100-step small training run
- T7.5 100-step small training review
- T7.6 50-step vs 100-step comparison
- T8 A100 100M scaling plan
- T8.1 A100 100M config draft
- T8.2 A100 environment preflight checklist
- T8.3 A100 100M forward/loss smoke plan
- T8.4 A100 execution runbook
- T8.5 A100 access decision checklist
- T8.6 A100 provider selection record
- T8.7 A100 first-session command checklist
- T8.8 A100 first-session report template
- A1 A100 smoke milestone report
- D1 expand permitted corpus plan
- D2 expanded synthetic educational corpus plan
