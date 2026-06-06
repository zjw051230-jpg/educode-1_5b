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
from educode.optimizers import create_optimizer, normalize_optimizer_name  # noqa: E402

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


class OptimizerRegistryTests(unittest.TestCase):
    def test_adamw_registry_creates_and_steps(self) -> None:
        parameter = torch.nn.Parameter(torch.tensor([1.0]))
        optimizer = create_optimizer([parameter], {"name": "adamw", "learning_rate": 0.1, "weight_decay": 0.0})
        parameter.pow(2).sum().backward()
        before = float(parameter.item())
        optimizer.step()

        self.assertIsInstance(optimizer, torch.optim.AdamW)
        self.assertNotEqual(float(parameter.item()), before)

    def test_default_config_still_uses_adamw(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)

        self.assertEqual(config["optimizer"]["name"], "adamw")
        self.assertEqual(validate_config(config, repo_root=PROJECT_ROOT), [])

    def test_bad_optimizer_config_rejected(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)
        bad = copy.deepcopy(config)
        bad["optimizer"]["name"] = "bad_optimizer"
        errors = validate_config(bad, repo_root=PROJECT_ROOT)

        self.assertTrue(any("optimizer.name" in error for error in errors))
        with self.assertRaises(ValueError):
            normalize_optimizer_name("bad_optimizer")

    def test_muon_requires_ack(self) -> None:
        with self.assertRaises(ValueError):
            create_optimizer([torch.nn.Parameter(torch.randn(4, 4))], {"name": "muon_experimental"})


if __name__ == "__main__":
    unittest.main()
