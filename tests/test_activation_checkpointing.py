import sys
import unittest
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.activation_checkpointing import (  # noqa: E402
    ActivationCheckpointConfig,
    checkpoint_forward,
    validate_activation_checkpoint_config,
)


class ActivationCheckpointingTests(unittest.TestCase):
    def test_default_disabled(self):
        config = ActivationCheckpointConfig()

        self.assertEqual(config.granularity, "none")
        self.assertFalse(config.enabled)
        self.assertEqual(validate_activation_checkpoint_config(config)["status"], "valid")

    def test_unknown_granularity_rejected(self):
        with self.assertRaises(ValueError):
            ActivationCheckpointConfig(granularity="layernorm")

    def test_enabled_requires_experimental_ack(self):
        with self.assertRaises(ValueError):
            ActivationCheckpointConfig(enabled=True, granularity="block")

    def test_block_wrapper_synthetic_forward_backward_finite(self):
        module = torch.nn.Sequential(torch.nn.Linear(4, 4), torch.nn.SiLU())
        x = torch.randn(3, 4, requires_grad=True)
        config = ActivationCheckpointConfig(
            enabled=True,
            granularity="block",
            experimental_ack=True,
        )

        y = checkpoint_forward(module, x, config)
        loss = y.square().mean()
        loss.backward()

        self.assertTrue(torch.isfinite(y).all())
        self.assertTrue(torch.isfinite(x.grad).all())


if __name__ == "__main__":
    unittest.main()
