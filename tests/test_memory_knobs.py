import sys
import unittest
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.memory import (  # noqa: E402
    MemoryKnobsConfig,
    checkpoint_module_forward,
    validate_memory_knobs,
)


class MemoryKnobsTests(unittest.TestCase):
    def test_default_config_is_disabled(self):
        config = MemoryKnobsConfig()

        self.assertFalse(config.activation_checkpointing)
        self.assertEqual(validate_memory_knobs(config)["status"], "valid")

    def test_bad_config_rejected(self):
        with self.assertRaises(ValueError):
            MemoryKnobsConfig(checkpoint_segments=0)

    def test_checkpoint_wrapper_forward_backward_is_finite(self):
        torch.manual_seed(0)
        module = torch.nn.Sequential(torch.nn.Linear(4, 4), torch.nn.GELU())
        x = torch.randn(2, 4, requires_grad=True)
        config = MemoryKnobsConfig(activation_checkpointing=True)

        y = checkpoint_module_forward(module, x, config)
        loss = y.pow(2).mean()
        loss.backward()

        self.assertTrue(torch.isfinite(y).all())
        self.assertTrue(torch.isfinite(x.grad).all())


if __name__ == "__main__":
    unittest.main()
