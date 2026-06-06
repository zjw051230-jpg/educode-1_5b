from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.distributed_config import DistributedConfig  # noqa: E402
from src.educode.memory_estimator import estimate_training_memory_gib  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate rough local training memory.")
    parser.add_argument("--strategy", default="single_gpu")
    parser.add_argument("--world-size", type=int, default=1)
    parser.add_argument("--parameters", type=int, default=300_000_000)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--sequence-length", type=int, default=1024)
    args = parser.parse_args()

    config = DistributedConfig(
        strategy=args.strategy,
        world_size=args.world_size,
        experimental_ack=args.strategy != "single_gpu",
    )
    estimate = estimate_training_memory_gib(
        parameter_count=args.parameters,
        batch_size=args.batch_size,
        sequence_length=args.sequence_length,
        hidden_size=1024,
        num_layers=24,
        dtype_bytes=2,
        distributed=config,
    )
    estimate["modal_gpu_training_run"] = False
    print(json.dumps(estimate, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
