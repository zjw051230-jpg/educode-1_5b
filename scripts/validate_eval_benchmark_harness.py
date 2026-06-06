from __future__ import annotations

import json
import sys
from pathlib import Path

import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.eval_benchmarks import BenchmarkTask, run_benchmark_task  # noqa: E402
from src.educode.eval_metrics import perplexity_from_logits  # noqa: E402


def main() -> int:
    blockers = []
    exact = run_benchmark_task(BenchmarkTask("exact", "exact_match", [{"prediction": "ok", "target": "OK"}]))
    mc = run_benchmark_task(BenchmarkTask("mc", "multiple_choice", [{"scores": [0.0, 1.0], "target_index": 1}]))
    ppl = perplexity_from_logits(torch.tensor([[[1.0, 0.0]]]), torch.tensor([[0]]))
    if exact["score"] != 1.0:
        blockers.append("exact_match_failed")
    if mc["score"] != 1.0:
        blockers.append("multiple_choice_failed")
    if not torch.isfinite(torch.tensor(ppl)):
        blockers.append("perplexity_non_finite")
    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "perplexity": ppl,
        "checkpoint_loaded": False,
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
