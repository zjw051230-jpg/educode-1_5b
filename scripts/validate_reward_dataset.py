from __future__ import annotations

import json
import sys
from pathlib import Path

import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.reward_model import (  # noqa: E402
    RewardHead,
    RewardPair,
    pairwise_ranking_loss,
    validate_reward_pair,
)


def main() -> int:
    pair = RewardPair(
        prompt="Summarize artifact hygiene.",
        chosen="Keep small summaries committed and leave checkpoints out of git.",
        rejected="Commit all tarballs and checkpoints.",
    )
    head = RewardHead(hidden_size=4)
    rewards = head(torch.randn(2, 4))
    loss = pairwise_ranking_loss(rewards[:1], rewards[1:])
    finite = bool(torch.isfinite(rewards).all() and torch.isfinite(loss))
    blockers = [] if finite else ["reward_synthetic_loss_non_finite"]
    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "pair_validation": validate_reward_pair(pair),
        "reward_shape": list(rewards.shape),
        "synthetic_pairwise_loss": float(loss.item()),
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
