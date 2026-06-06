from __future__ import annotations

import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.moe_routing import load_balancing_loss, router_z_loss  # noqa: E402


class MoELossTests(unittest.TestCase):
    def test_load_balance_loss_is_finite(self) -> None:
        probs = torch.softmax(torch.randn(6, 4), dim=-1)
        indices = torch.tensor([[0, 1], [1, 2], [2, 3], [3, 0], [0, 2], [1, 3]])

        self.assertTrue(torch.isfinite(load_balancing_loss(probs, indices, num_experts=4)))

    def test_router_z_loss_is_finite(self) -> None:
        self.assertTrue(torch.isfinite(router_z_loss(torch.randn(6, 4))))


if __name__ == "__main__":
    unittest.main()
