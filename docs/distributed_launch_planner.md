# Distributed Launch Planner

The distributed launch planner generates protected command strings only. It is useful for reviewing command shape before a real multi-GPU branch exists.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\plan_distributed_launch.py --strategy fsdp --gpus-per-node 2
```

## Guarantees

- Generated commands are strings only.
- Invalid strategies are rejected.
- Invalid ZeRO stages are rejected.
- Sequence parallel requires tensor parallel size greater than 1.
- No command is executed.
- Modal/GPU/training run: no.
