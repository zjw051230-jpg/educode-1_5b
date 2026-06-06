import sys
import unittest
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.lora import (  # noqa: E402
    LoRAConfig,
    LoRALinear,
    adapter_state_dict,
    count_trainable_parameters,
)
from src.educode.peft import select_lora_targets  # noqa: E402


class LoRAPeftV2Tests(unittest.TestCase):
    def test_bad_rank_alpha_dropout_rejected(self):
        with self.assertRaises(ValueError):
            LoRAConfig(rank=0)
        with self.assertRaises(ValueError):
            LoRAConfig(rank=2, alpha=0)
        with self.assertRaises(ValueError):
            LoRAConfig(rank=2, dropout=1.5)

    def test_disabled_path_equals_base_linear(self):
        torch.manual_seed(0)
        base = torch.nn.Linear(4, 3)
        wrapped = LoRALinear(base, LoRAConfig(rank=2, alpha=4, enabled=False))
        x = torch.randn(5, 4)

        self.assertTrue(torch.allclose(wrapped(x), base(x)))

    def test_enabled_shape_trainable_and_adapter_state(self):
        wrapped = LoRALinear(
            torch.nn.Linear(4, 3),
            LoRAConfig(rank=2, alpha=4, enabled=True, dropout=0.0),
        )

        self.assertEqual(wrapped(torch.randn(7, 4)).shape, (7, 3))
        self.assertEqual(count_trainable_parameters(wrapped)["trainable_names"], ["lora_a", "lora_b"])
        self.assertEqual(set(adapter_state_dict(wrapped)), {"lora_a", "lora_b"})

    def test_merge_unmerge_reversible(self):
        torch.manual_seed(1)
        wrapped = LoRALinear(
            torch.nn.Linear(4, 3),
            LoRAConfig(rank=2, alpha=4, enabled=True, dropout=0.0),
        )
        x = torch.randn(2, 4)
        before = wrapped(x)
        wrapped.merge()
        merged = wrapped(x)
        wrapped.unmerge()
        after = wrapped(x)

        self.assertTrue(torch.allclose(before, merged, atol=1e-6))
        self.assertTrue(torch.allclose(before, after, atol=1e-6))

    def test_target_selector(self):
        model = torch.nn.Sequential(torch.nn.Linear(4, 4), torch.nn.ReLU(), torch.nn.Linear(4, 2))

        self.assertEqual(select_lora_targets(model), ["0", "2"])


if __name__ == "__main__":
    unittest.main()
