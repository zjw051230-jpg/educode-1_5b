from __future__ import annotations

import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.muon import MuonExperimental, newton_schulz_orthogonalize, split_muon_adamw_parameters  # noqa: E402


class MuonExperimentalTests(unittest.TestCase):
    def test_newton_schulz_output_is_finite(self) -> None:
        result = newton_schulz_orthogonalize(torch.randn(4, 4))

        self.assertEqual(tuple(result.shape), (4, 4))
        self.assertTrue(torch.isfinite(result).all())

    def test_muon_step_on_synthetic_2d_parameter(self) -> None:
        parameter = torch.nn.Parameter(torch.randn(4, 4))
        optimizer = MuonExperimental([parameter], lr=0.01)
        parameter.pow(2).sum().backward()
        before = parameter.detach().clone()
        optimizer.step()

        self.assertFalse(torch.equal(before, parameter.detach()))

    def test_parameter_grouping_separates_hidden_from_embedding_norm_bias_lm_head(self) -> None:
        named = [
            ("blocks.0.mlp.up_proj.weight", torch.nn.Parameter(torch.randn(4, 4))),
            ("token_embedding.weight", torch.nn.Parameter(torch.randn(8, 4))),
            ("final_norm.weight", torch.nn.Parameter(torch.randn(4))),
            ("lm_head.weight", torch.nn.Parameter(torch.randn(4, 8))),
            ("mlp.bias", torch.nn.Parameter(torch.randn(4))),
        ]
        groups = split_muon_adamw_parameters(named)

        self.assertEqual([name for name, _ in groups.muon], ["blocks.0.mlp.up_proj.weight"])
        self.assertEqual(len(groups.adamw), 4)


if __name__ == "__main__":
    unittest.main()
