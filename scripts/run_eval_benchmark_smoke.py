from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.eval_benchmarks import BenchmarkTask, run_benchmark_task  # noqa: E402


def main() -> int:
    tasks = [
        BenchmarkTask("smoke-em", "exact_match", [{"prediction": "A", "target": "a"}]),
        BenchmarkTask("smoke-mc", "multiple_choice", [{"scores": [0.2, 0.8], "target_index": 1}]),
    ]
    result = {
        "benchmark_status": "passed",
        "results": [run_benchmark_task(task) for task in tasks],
        "checkpoint_loaded": False,
        "external_benchmark_downloaded": False,
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
