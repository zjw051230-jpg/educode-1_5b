import sys
import unittest
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


class RewardModelTests(unittest.TestCase):
    def test_reward_head_output_shape(self):
        head = RewardHead(hidden_size=6)
        hidden = torch.randn(4, 6)

        rewards = head(hidden)

        self.assertEqual(rewards.shape, (4,))

    def test_pairwise_ranking_loss_is_finite(self):
        chosen = torch.tensor([2.0, 1.0])
        rejected = torch.tensor([0.5, -0.25])

        loss = pairwise_ranking_loss(chosen, rejected)

        self.assertEqual(loss.shape, ())
        self.assertTrue(torch.isfinite(loss))

    def test_reward_pair_validation(self):
        pair = RewardPair(prompt="p", chosen="better", rejected="worse")

        self.assertEqual(validate_reward_pair(pair)["status"], "valid")
        with self.assertRaises(ValueError):
            RewardPair(prompt="p", chosen="same", rejected="same")


if __name__ == "__main__":
    unittest.main()
