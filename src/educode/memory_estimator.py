from __future__ import annotations

from src.educode.distributed_config import DistributedConfig


BYTES_PER_GIB = 1024**3


def _gib(bytes_value: float) -> float:
    return round(bytes_value / BYTES_PER_GIB, 6)


def estimate_training_memory_gib(
    parameter_count: int,
    batch_size: int,
    sequence_length: int,
    hidden_size: int,
    num_layers: int,
    dtype_bytes: int,
    distributed: DistributedConfig | None = None,
) -> dict:
    if distributed is None:
        distributed = DistributedConfig()
    for name, value in {
        "parameter_count": parameter_count,
        "batch_size": batch_size,
        "sequence_length": sequence_length,
        "hidden_size": hidden_size,
        "num_layers": num_layers,
        "dtype_bytes": dtype_bytes,
    }.items():
        if value <= 0:
            raise ValueError(f"{name} must be positive")

    shard_factor = distributed.world_size if distributed.strategy in {"fsdp", "zero"} else 1
    parameter_bytes = parameter_count * dtype_bytes / shard_factor
    gradient_bytes = parameter_count * dtype_bytes / shard_factor
    optimizer_multiplier = 3 if distributed.zero_stage == 3 else 6
    optimizer_bytes = parameter_count * dtype_bytes * optimizer_multiplier / shard_factor
    activation_bytes = batch_size * sequence_length * hidden_size * num_layers * dtype_bytes
    if distributed.sequence_parallel:
        activation_bytes /= max(distributed.tensor_parallel_size, 1)

    total = parameter_bytes + gradient_bytes + optimizer_bytes + activation_bytes
    return {
        "strategy": distributed.strategy,
        "world_size": distributed.world_size,
        "parameter_gib": _gib(parameter_bytes),
        "gradient_gib": _gib(gradient_bytes),
        "optimizer_state_gib": _gib(optimizer_bytes),
        "activation_gib": _gib(activation_bytes),
        "total_estimated_gib": _gib(total),
        "estimate_type": "rough_local_planning_only",
    }
