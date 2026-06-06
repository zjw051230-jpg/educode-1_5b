from __future__ import annotations

import json
import math
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.compression import CompressionPlan, summarize_compression_plan
from educode.distillation import DistillationConfig, distillation_kl_loss


def main() -> int:
    config = DistillationConfig(temperature=2.0, alpha=0.7)
    loss = distillation_kl_loss(
        [[1.0, 0.0, -1.0], [0.2, 0.1, 0.0]],
        [[1.5, 0.1, -0.8], [0.3, 0.2, -0.1]],
        config,
    )
    plan = summarize_compression_plan(
        CompressionPlan(strategy="magnitude_pruning", target_sparsity=0.1, notes="future feasibility audit")
    )
    payload = {
        "validation_status": "passed" if math.isfinite(loss) else "failed",
        "kl_loss": loss,
        "temperature": config.temperature,
        "alpha": config.alpha,
        "compression_plan": plan,
        "checkpoint_loaded": False,
        "teacher_checkpoint_loaded": False,
        "modal_used": False,
        "gpu_used": False,
        "training_started": False,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["validation_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
