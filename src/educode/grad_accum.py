from __future__ import annotations


def _require_positive(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def training_tokens_accounting(
    micro_batch_size: int,
    grad_accum_steps: int,
    sequence_length: int,
    world_size: int,
    max_steps: int,
) -> dict:
    for name, value in {
        "micro_batch_size": micro_batch_size,
        "grad_accum_steps": grad_accum_steps,
        "sequence_length": sequence_length,
        "world_size": world_size,
        "max_steps": max_steps,
    }.items():
        _require_positive(name, value)

    global_batch_size = micro_batch_size * grad_accum_steps * world_size
    tokens_per_optimizer_step = global_batch_size * sequence_length
    return {
        "micro_batch_size": micro_batch_size,
        "grad_accum_steps": grad_accum_steps,
        "world_size": world_size,
        "sequence_length": sequence_length,
        "global_batch_size": global_batch_size,
        "tokens_per_optimizer_step": tokens_per_optimizer_step,
        "tokens_seen": tokens_per_optimizer_step * max_steps,
    }
