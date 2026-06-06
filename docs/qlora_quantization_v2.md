# QLoRA / Quantization v2

This branch extends quantization feasibility checks without loading a real 4-bit model.

## Included

- NF4, FP4, and int8 config validation.
- bitsandbytes availability guard.
- local CUDA availability guard.
- fake quantize/dequantize helpers for synthetic tensors.
- QLoRA requires quantization plus explicit experimental acknowledgement.

## Commands

```powershell
.\.venv\Scripts\python.exe scripts\check_quantization_feasibility_v2.py
.\.venv\Scripts\python.exe scripts\validate_qlora_config.py
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Real 4-bit model load: no.
- Future LoRA/QLoRA training requires explicit GPU/Modal cost confirmation.
