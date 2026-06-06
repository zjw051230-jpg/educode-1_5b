from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class CompressionPlan:
    strategy: str
    target_sparsity: float
    notes: str = ""

    def __post_init__(self) -> None:
        if self.strategy not in {"magnitude_pruning", "distillation_only", "quantization_audit"}:
            raise ValueError(f"unsupported compression strategy: {self.strategy}")
        if not 0.0 <= self.target_sparsity < 1.0:
            raise ValueError("target_sparsity must be in [0, 1)")


def summarize_compression_plan(plan: CompressionPlan) -> dict[str, object]:
    payload = asdict(plan)
    payload.update(
        {
            "model_mutated": False,
            "checkpoint_loaded": False,
            "requires_future_gpu_gate": plan.strategy != "distillation_only",
        }
    )
    return payload
