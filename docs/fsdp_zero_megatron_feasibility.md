# FSDP / ZeRO / Megatron Feasibility

This branch records local feasibility planning for distributed training strategies. It does not implement or execute distributed training.

## Scope

- FSDP feasibility notes.
- DeepSpeed ZeRO stage guard.
- Megatron-style tensor parallel and sequence parallel compatibility guard.
- Future GPU, multi-GPU, B200, and Modal cost gates.

## Non-Scope

- No `torchrun` execution.
- No `deepspeed` execution.
- No NCCL workload.
- No multi-GPU training.
- No checkpoint or raw data handling.

## Gate

Any real distributed execution requires explicit user cost confirmation and a bounded run plan.
