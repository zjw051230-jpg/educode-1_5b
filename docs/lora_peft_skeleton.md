# LoRA / PEFT Skeleton

This branch adds a small LoRA/PEFT skeleton for future adapter training work. It does not train, load a large model, run Modal, or use GPU.

## Included

- `LoRAConfig` with rank/alpha validation.
- `LoRALinear` wrapper for `torch.nn.Linear`.
- Disabled-by-default path that returns the base linear output.
- Adapter-only trainable parameters when enabled and `freeze_base = true`.
- Adapter state dict filtering.
- Target linear module discovery helper.
- Merge/unmerge guard skeleton for future inference/export workflows.

## Current Guardrails

- Default adapter state: disabled.
- Bad rank or alpha: rejected.
- Synthetic CPU forward only.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data touched: no.

## Future Work

- Wire target module names into the training config.
- Add checkpoint format rules for adapter-only saves.
- Add explicit cost-gated Modal training mode only after local review.
