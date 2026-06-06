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
from educode.optimizers import (  # noqa: E402
    ExperimentalOptimizerUnavailable,
    create_optimizer,
    normalize_optimizer_name,
)

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


class OptimizerRegistryTests(unittest.TestCase):
    def test_adamw_registry_creates_optimizer_and_steps(self) -> None:
        parameter = torch.nn.Parameter(torch.tensor([1.0]))
        optimizer = create_optimizer([parameter], {"name": "adamw", "learning_rate": 0.1, "weight_decay": 0.0})
        loss = parameter.pow(2).sum()
        loss.backward()
        before = float(parameter.detach().item())
        optimizer.step()
        after = float(parameter.detach().item())

        self.assertIsInstance(optimizer, torch.optim.AdamW)
        self.assertNotEqual(before, after)

    def test_default_config_still_uses_adamw(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)

        self.assertEqual(config["optimizer"]["name"], "adamw")
        self.assertEqual(validate_config(config, repo_root=PROJECT_ROOT), [])

    def test_bad_optimizer_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            normalize_optimizer_name("not_an_optimizer")

        config = load_json_config(DEFAULT_CONFIG_PATH)
        bad_config = copy.deepcopy(config)
        bad_config["optimizer"]["name"] = "not_an_optimizer"
        errors = validate_config(bad_config, repo_root=PROJECT_ROOT)

        self.assertTrue(any("optimizer.name" in error for error in errors))

    def test_muon_experimental_is_guarded(self) -> None:
        with self.assertRaises(ExperimentalOptimizerUnavailable):
            create_optimizer([torch.nn.Parameter(torch.tensor([1.0]))], {"name": "muon_experimental"})

        with self.assertRaises(ExperimentalOptimizerUnavailable):
            create_optimizer(
                [torch.nn.Parameter(torch.tensor([1.0]))],
                {"name": "muon_experimental"},
                allow_experimental=True,
            )


if __name__ == "__main__":
    unittest.main()
