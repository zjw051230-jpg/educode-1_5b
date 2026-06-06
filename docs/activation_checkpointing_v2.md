# Activation Checkpointing v2

This branch adds local-only activation checkpointing controls. It does not connect checkpointing into a real training loop.

## Included

- Config schema with granularities: `none`, `block`, `attention`, `mlp`.
- Default disabled behavior.
- Experimental acknowledgement requirement when enabled.
- Checkpoint wrapper helper.
- CPU synthetic forward/backward validator.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\validate_activation_checkpointing.py
```

## Compute vs Memory Caveat

Activation checkpointing can reduce stored activations but increases recomputation. The tradeoff must be measured in a bounded GPU profiling branch before use in training.

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Default enabled: no.
- Checkpoint/tarball/raw data touched: no.
