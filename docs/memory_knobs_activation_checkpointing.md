# Memory Knobs / Activation Checkpointing

This branch adds local-only memory knob scaffolding for future activation checkpointing experiments. It does not enable checkpointing by default and does not run training.

## Included

- `MemoryKnobsConfig` with validation.
- Default disabled activation checkpointing.
- Small checkpoint wrapper for module forward calls.
- Local CPU validator with synthetic forward/backward.

## Tradeoff

Activation checkpointing can reduce activation memory at the cost of recomputing part of the forward pass during backward. That tradeoff should be measured in a bounded profiling run before use in training.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\validate_memory_knobs.py
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Default enabled: no.
- Tarball/checkpoint/raw data touched: no.
