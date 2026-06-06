import sys
import unittest
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.lora import LoRAConfig, LoRALinear, adapter_state_dict  # noqa: E402
from src.educode.peft import find_target_linear_modules  # noqa: E402


class LoRAPEFTTests(unittest.TestCase):
    def test_disabled_path_equals_base_linear(self):
        torch.manual_seed(0)
        base = torch.nn.Linear(4, 3)
        wrapped = LoRALinear(base, LoRAConfig(rank=2, alpha=4.0, enabled=False))
        x = torch.randn(5, 4)

        self.assertTrue(torch.allclose(wrapped(x), base(x)))

    def test_enabled_adapter_shape_and_trainable_params(self):
        base = torch.nn.Linear(4, 3)
        wrapped = LoRALinear(base, LoRAConfig(rank=2, alpha=4.0, enabled=True))

        trainable = {name for name, p in wrapped.named_parameters() if p.requires_grad}

        self.assertEqual(wrapped(torch.randn(7, 4)).shape, (7, 3))
        self.assertEqual(trainable, {"lora_a", "lora_b"})

    def test_bad_lora_config_rejected(self):
        with self.assertRaises(ValueError):
            LoRAConfig(rank=0, alpha=4.0)
        with self.assertRaises(ValueError):
            LoRAConfig(rank=2, alpha=0.0)

    def test_target_selection_and_adapter_state_filter(self):
        model = torch.nn.Sequential(
            torch.nn.Linear(4, 4),
            torch.nn.ReLU(),
            torch.nn.Linear(4, 2),
        )

        targets = find_target_linear_modules(model)
        wrapped = LoRALinear(model[0], LoRAConfig(rank=1, alpha=1.0, enabled=True))
        state = adapter_state_dict({"block": wrapped})

        self.assertEqual(targets, ["0", "2"])
        self.assertEqual(set(state), {"block.lora_a", "block.lora_b"})


if __name__ == "__main__":
    unittest.main()
