# LoRA / PEFT v2

This branch extends the LoRA/PEFT skeleton without loading real checkpoints or training.

## Included

- `LoRAConfig` with rank, alpha, and dropout validation.
- `LoRALinear` wrapper.
- Disabled path equal to base linear output.
- Adapter-only trainable parameter report.
- Adapter-only state dict filter.
- Merge/unmerge guard with synthetic reversibility check.
- Target module selector for linear modules.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\validate_lora_peft_v2.py
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Real checkpoint load: no.
- Adapter training requires future GPU/Modal gate and checkpoint policy review.
