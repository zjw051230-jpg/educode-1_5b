from __future__ import annotations

import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.sampling import filter_top_k, filter_top_p, greedy_token, sample_token, validate_sampling_args  # noqa: E402


class SamplingTests(unittest.TestCase):
    def test_greedy_is_deterministic(self) -> None:
        self.assertEqual(int(greedy_token(torch.tensor([0.1, 3.0, 2.0])).item()), 1)

    def test_top_k_and_top_p_sampling_returns_valid_token(self) -> None:
        logits = torch.tensor([0.1, 0.2, 5.0, 0.3])
        token = sample_token(logits, top_k=2, top_p=0.95, generator=torch.Generator().manual_seed(1))

        self.assertIn(int(token.item()), range(4))
        self.assertTrue(torch.isfinite(filter_top_k(logits, 2)).any())
        self.assertTrue(torch.isfinite(filter_top_p(logits, 0.95)).any())

    def test_bad_sampling_config_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_sampling_args(temperature=0)
        with self.assertRaises(ValueError):
            validate_sampling_args(top_k=0)
        with self.assertRaises(ValueError):
            validate_sampling_args(top_p=1.5)


if __name__ == "__main__":
    unittest.main()
