from __future__ import annotations

import json
import sys
from pathlib import Path

import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.memory import (  # noqa: E402
    MemoryKnobsConfig,
    checkpoint_module_forward,
    validate_memory_knobs,
)


def main() -> int:
    config = MemoryKnobsConfig(activation_checkpointing=True)
    module = torch.nn.Sequential(torch.nn.Linear(4, 4), torch.nn.ReLU())
    x = torch.randn(2, 4, requires_grad=True)
    y = checkpoint_module_forward(module, x, config)
    loss = y.pow(2).mean()
    loss.backward()

    finite = bool(torch.isfinite(y).all() and torch.isfinite(x.grad).all())
    blockers = [] if finite else ["checkpoint_forward_backward_non_finite"]
    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "config": validate_memory_knobs(config),
        "synthetic_forward_backward_finite": finite,
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
