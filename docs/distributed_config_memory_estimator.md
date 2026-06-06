# Distributed Config / Memory Estimator

This branch adds local-only distributed training planning helpers. It does not run distributed training, `torchrun`, NCCL, Modal, GPU, or any training loop.

## Included

- Distributed config schema for `single_gpu`, `fsdp`, `zero`, tensor parallel, and pipeline parallel planning.
- Experimental acknowledgement gate for non-single-GPU strategies.
- Sequence parallel guard requiring tensor parallelism.
- Gradient accumulation and token accounting.
- Rough parameter, gradient, optimizer state, and activation memory estimator.

## Commands

```powershell
.\.venv\Scripts\python.exe scripts\validate_distributed_config.py
.\.venv\Scripts\python.exe scripts\estimate_training_memory.py
```

## Caveats

The memory estimator is deterministic and useful for planning, but it is not a replacement for measured GPU profiling. Real FSDP, ZeRO, tensor parallel, sequence parallel, Megatron, B200, or multi-GPU execution requires a separate cost gate.
