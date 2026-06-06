# EduCode-1.5B Model Card Template

## Status

EduCode-1.5B is not a finished foundation model. This repository is evidence for building and validating a reproducible training pipeline, not a claim of production model quality.

## Intended Use

- Training systems portfolio evidence.
- Local and Modal execution guardrail review.
- Small-scale profiling comparison across context length, batch size, and attention backend choices.

## Out Of Scope

- Production deployment.
- Safety-critical use.
- Claims of broad benchmark quality.
- Claims that short profiling runs prove model quality.

## Evidence Summary

- FineWeb-Edu 5GB 3000-step training improved relative to the 1000-step run.
- Validation guardrails recorded `validation_unique_doc_count = 15` and `validation_prefix_only_risk = false` for the key 5GB run.
- Short profiling runs are systems evidence for throughput, step time, and memory.
- seq512 SDPA and seq1024 SDPA profiles completed on A100-40GB without OOM in the recorded bounded runs.

## Limitations

- Short 10-step and 50-step runs are sanity/profiling evidence only.
- MFU is currently unavailable/null in the imported profiling artifacts.
- No naive attention or FlashAttention comparison should be claimed until those branches are implemented and run.
- Raw datasets, prepared data, tarballs, and checkpoints are intentionally not committed.

## Reproducibility Fields

- Repository commit:
- Config path:
- Tokenizer path:
- Dataset slice:
- Modal mode, if any:
- GPU type, if any:
- Runtime dtype:
- Batch size:
- Gradient accumulation:
- Context length:
- Max steps:
- Artifact validation status:
