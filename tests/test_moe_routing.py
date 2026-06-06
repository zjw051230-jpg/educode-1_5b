from __future__ import annotations

import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.moe_layers import MoEConfig, MoEFFNSkeleton, TopKRouter  # noqa: E402
from educode.moe_routing import combine_tokens, dispatch_tokens, expert_capacity  # noqa: E402


class MoERoutingTests(unittest.TestCase):
    def test_top_k_router_shape_and_weight_normalization(self) -> None:
        routing = TopKRouter(d_model=16, num_experts=4, top_k=2)(torch.randn(2, 4, 16))

        self.assertEqual(tuple(routing["top_indices"].shape), (2, 4, 2))
        self.assertTrue(torch.allclose(routing["top_weights"].sum(dim=-1), torch.ones(2, 4), atol=1e-6))

    def test_capacity_helper(self) -> None:
        self.assertEqual(expert_capacity(num_tokens=8, num_experts=4, top_k=2, capacity_factor=1.25), 5)

    def test_dispatch_and_combine_synthetic_shape(self) -> None:
        tokens = torch.randn(4, 8)
        expert_indices = torch.tensor([[0, 1], [1, 2], [2, 3], [3, 0]])
        weights = torch.full((4, 2), 0.5)
        dispatched, metadata = dispatch_tokens(tokens, expert_indices, weights, num_experts=4, capacity_factor=1.0)
        combined = combine_tokens(dispatched, metadata, num_tokens=4)

        self.assertEqual(tuple(dispatched.shape), (4, 2, 8))
        self.assertEqual(tuple(combined.shape), tuple(tokens.shape))

    def test_moe_ffn_skeleton_outputs_router_metadata(self) -> None:
        output = MoEFFNSkeleton(MoEConfig(d_model=16, d_ff=64, num_experts=4, top_k=2))(torch.randn(2, 4, 16))

        self.assertIn("router_logits", output)
        self.assertIn("top_indices", output)


if __name__ == "__main__":
    unittest.main()
