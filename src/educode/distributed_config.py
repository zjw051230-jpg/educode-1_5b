from __future__ import annotations

from dataclasses import asdict, dataclass


EXPERIMENTAL_STRATEGIES = {"fsdp", "zero", "tensor_parallel", "pipeline_parallel"}


@dataclass(frozen=True)
class DistributedConfig:
    strategy: str = "single_gpu"
    world_size: int = 1
    tensor_parallel_size: int = 1
    pipeline_parallel_size: int = 1
    zero_stage: int | None = None
    sequence_parallel: bool = False
    experimental_ack: bool = False

    def __post_init__(self) -> None:
        if self.world_size <= 0:
            raise ValueError("world_size must be positive")
        if self.tensor_parallel_size <= 0 or self.pipeline_parallel_size <= 0:
            raise ValueError("parallel sizes must be positive")
        if self.strategy == "single_gpu" and self.world_size != 1:
            raise ValueError("single_gpu strategy requires world_size=1")
        if self.strategy not in {"single_gpu", "fsdp", "zero", "tensor_parallel", "pipeline_parallel"}:
            raise ValueError(f"unknown distributed strategy: {self.strategy}")
        if self.strategy in EXPERIMENTAL_STRATEGIES and not self.experimental_ack:
            raise ValueError("experimental distributed strategies require experimental_ack=True")
        if self.world_size % self.tensor_parallel_size != 0:
            raise ValueError("world_size must be divisible by tensor_parallel_size")
        if self.world_size % self.pipeline_parallel_size != 0:
            raise ValueError("world_size must be divisible by pipeline_parallel_size")
        if self.sequence_parallel and self.tensor_parallel_size <= 1:
            raise ValueError("sequence_parallel requires tensor_parallel_size > 1")
        if self.zero_stage is not None and self.zero_stage not in {1, 2, 3}:
            raise ValueError("zero_stage must be 1, 2, or 3")

    def validate(self) -> dict:
        return {
            "status": "valid",
            "strategy": self.strategy,
            "world_size": self.world_size,
            "tensor_parallel_size": self.tensor_parallel_size,
            "pipeline_parallel_size": self.pipeline_parallel_size,
            "zero_stage": self.zero_stage,
            "sequence_parallel": self.sequence_parallel,
            "experimental_ack": self.experimental_ack,
        }

    def to_dict(self) -> dict:
        return asdict(self)
