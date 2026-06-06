from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.config_loader import load_json_config  # noqa: E402
from educode.config_validator import validate_config  # noqa: E402
from educode.moe_layers import MoEConfig, SparseMoESkeleton, TopKRouter  # noqa: E402

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


class MoERoutingTests(unittest.TestCase):
    def test_top_k_router_shapes_and_normalized_weights(self) -> None:
        router = TopKRouter(d_model=16, num_experts=4, top_k=2)
        x = torch.randn(2, 5, 16)
        top_indices, top_weights = router(x)

        self.assertEqual(tuple(top_indices.shape), (2, 5, 2))
        self.assertEqual(tuple(top_weights.shape), (2, 5, 2))
        self.assertTrue(torch.allclose(top_weights.sum(dim=-1), torch.ones(2, 5), atol=1e-6))

    def test_moe_skeleton_returns_routing_metadata_only(self) -> None:
        skeleton = SparseMoESkeleton(MoEConfig(d_model=16, d_ff=64, num_experts=4, top_k=2))
        output = skeleton(torch.randn(2, 5, 16))

        self.assertEqual(set(output), {"top_indices", "top_weights"})

    def test_dense_config_with_moe_disabled_remains_valid(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)
        config["moe"] = {"enabled": False, "num_experts": 4, "top_k": 2}

        self.assertEqual(validate_config(config, repo_root=PROJECT_ROOT), [])

    def test_moe_enabled_training_config_is_rejected(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)
        config["moe"] = {"enabled": True, "num_experts": 4, "top_k": 2}
        errors = validate_config(config, repo_root=PROJECT_ROOT)

        self.assertTrue(any("moe.enabled=true" in error for error in errors))

    def test_bad_moe_config_is_rejected(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)
        bad_config = copy.deepcopy(config)
        bad_config["moe"] = {"enabled": False, "num_experts": 2, "top_k": 3}
        errors = validate_config(bad_config, repo_root=PROJECT_ROOT)

        self.assertTrue(any("moe.top_k" in error for error in errors))
        with self.assertRaises(ValueError):
            TopKRouter(d_model=16, num_experts=2, top_k=3)


if __name__ == "__main__":
    unittest.main()
