from __future__ import annotations

import json
import sys
from pathlib import Path

import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.dpo import dpo_loss  # noqa: E402
from src.educode.preference import PreferencePair, validate_preference_pair  # noqa: E402


def main() -> int:
    pairs = [
        PreferencePair(
            prompt="Explain why profiling loss is not quality evidence.",
            chosen="It is a short sanity signal and should be framed as systems evidence.",
            rejected="It proves the model is production ready.",
        )
    ]
    validations = [validate_preference_pair(pair) for pair in pairs]
    loss = dpo_loss(
        torch.tensor([-1.0]),
        torch.tensor([-2.0]),
        torch.tensor([-1.2]),
        torch.tensor([-1.8]),
        beta=0.1,
    )
    blockers = [] if torch.isfinite(loss) else ["dpo_loss_non_finite"]
    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "preference_pair_count": len(pairs),
        "pair_validations": validations,
        "synthetic_dpo_loss": float(loss.item()),
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
