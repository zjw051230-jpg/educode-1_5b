# Quantization / QLoRA Feasibility

This branch adds local-only feasibility guards for future quantization and QLoRA work. It does not quantize a real model, run Modal, use GPU, or start training.

## Included

- `QuantizationConfig` for 4-bit NF4/FP4 and 8-bit int8 feasibility settings.
- Graceful `bitsandbytes` availability check.
- CPU fake quantization helper for tiny synthetic tensors.
- QLoRA readiness report with caveats.
- Local validator script.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\check_quantization_feasibility.py
```

## Caveats

- `bitsandbytes` may be unavailable locally and must not hard-fail the branch.
- Windows, CUDA, Modal image compatibility, paged optimizers, and adapter checkpointing need separate review.
- No real quantized training is performed here.

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Tarball/checkpoint/raw data touched: no.
- Future GPU/Modal validation requires explicit cost confirmation.
