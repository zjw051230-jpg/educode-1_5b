from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.plan_distributed_launch import check_fsdp_zero_feasibility  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local FSDP/ZeRO feasibility gates.")
    parser.add_argument("--strategy", default="fsdp", choices=["fsdp", "zero"])
    parser.add_argument("--zero-stage", type=int)
    parser.add_argument("--world-size", type=int, default=2)
    args = parser.parse_args()
    report = check_fsdp_zero_feasibility(args.strategy, args.zero_stage, args.world_size)
    report["modal_gpu_training_run"] = False
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
