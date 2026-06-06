# Resume Project Narrative Draft

EduCode-1.5B is a from-scratch LLM training-systems project focused on reproducibility, execution guardrails, and measured systems evidence.

## Strong Claims

- Built a PyTorch training pipeline with tokenizer/data loading, model code, validation guardrails, Modal execution gates, artifact validation, and concise experiment documentation.
- Ran bounded A100 SDPA profiling at seq512 and seq1024, recording throughput, step time, memory, and no-OOM status for the profiled configurations.
- Maintained strict artifact hygiene: raw data, prepared data, result tarballs, and checkpoints are excluded from git while small imported summaries are tracked.

## Careful Wording

- This is a systems portfolio, not a finished foundation model.
- Short profiling runs are systems evidence, not quality-training proof.
- Experimental branches cover future directions such as KV cache inference, attention backends, RoPE, LoRA, quantization, Muon, MoE, data quality, and distributed training planning.

## Interview Expansion Points

- Explain why artifact validation and claims boundaries matter.
- Explain why seq1024 profiling used a bounded gate before longer training.
- Explain how branch-only prototypes are separated from evidence-backed mainline claims.
- Explain future tradeoffs among backend profiling, long-context memory, LoRA/QLoRA, and distributed training.
