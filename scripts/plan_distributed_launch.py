from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


VALID_STRATEGIES = {"fsdp", "zero", "megatron"}


@dataclass(frozen=True)
class LaunchPlan:
    strategy: str
    nodes: int
    gpus_per_node: int
    config_path: str
    zero_stage: int | None = None
    tensor_parallel_size: int = 1
    sequence_parallel: bool = False

    def __post_init__(self) -> None:
        if self.strategy not in VALID_STRATEGIES:
            raise ValueError("invalid distributed launch strategy")
        if self.nodes <= 0 or self.gpus_per_node <= 0:
            raise ValueError("nodes and gpus_per_node must be positive")
        if self.strategy == "zero" and self.zero_stage not in {1, 2, 3}:
            raise ValueError("zero launch requires zero_stage 1, 2, or 3")
        if self.sequence_parallel and self.tensor_parallel_size <= 1:
            raise ValueError("sequence parallel requires tensor_parallel_size > 1")

    @property
    def world_size(self) -> int:
        return self.nodes * self.gpus_per_node


def build_launch_command(plan: LaunchPlan) -> str:
    base = (
        f"torchrun --nnodes {plan.nodes} --nproc_per_node {plan.gpus_per_node} "
        "scripts/run_distributed_training.py"
    )
    if plan.strategy == "fsdp":
        return f"{base} --strategy fsdp --config {plan.config_path}"
    if plan.strategy == "zero":
        return f"{base} --strategy zero --zero-stage {plan.zero_stage} --config {plan.config_path}"
    return (
        f"{base} --strategy megatron --tensor-parallel-size {plan.tensor_parallel_size} "
        f"{'--sequence-parallel ' if plan.sequence_parallel else ''}--config {plan.config_path}"
    ).strip()


def check_fsdp_zero_feasibility(
    strategy: str, zero_stage: int | None = None, world_size: int = 1
) -> dict:
    if strategy not in {"fsdp", "zero"}:
        raise ValueError("strategy must be fsdp or zero")
    if world_size <= 1:
        return {
            "status": "not_applicable_single_process",
            "strategy": strategy,
            "command_executed": False,
            "future_gpu_modal_gate_required": True,
        }
    if strategy == "zero" and zero_stage not in {1, 2, 3}:
        raise ValueError("zero_stage must be 1, 2, or 3")
    return {
        "status": "feasible_with_gate",
        "strategy": strategy,
        "zero_stage": zero_stage,
        "world_size": world_size,
        "command_executed": False,
        "future_gpu_modal_gate_required": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a protected distributed launch command string.")
    parser.add_argument("--strategy", default="fsdp", choices=sorted(VALID_STRATEGIES))
    parser.add_argument("--nodes", type=int, default=1)
    parser.add_argument("--gpus-per-node", type=int, default=2)
    parser.add_argument("--config-path", default="configs/a100/example_distributed.json")
    parser.add_argument("--zero-stage", type=int)
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--sequence-parallel", action="store_true")
    args = parser.parse_args()
    plan = LaunchPlan(
        strategy=args.strategy,
        nodes=args.nodes,
        gpus_per_node=args.gpus_per_node,
        config_path=args.config_path,
        zero_stage=args.zero_stage,
        tensor_parallel_size=args.tensor_parallel_size,
        sequence_parallel=args.sequence_parallel,
    )
    result = {
        "planning_status": "generated",
        "plan": asdict(plan),
        "world_size": plan.world_size,
        "command": build_launch_command(plan),
        "command_executed": False,
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
