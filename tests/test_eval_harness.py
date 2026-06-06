from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.eval import evaluate_next_token_loss  # noqa: E402
from educode.tiny_model import TinyDecoderOnlyTransformer, TinyModelConfig  # noqa: E402


class EvalHarnessTests(unittest.TestCase):
    def test_eval_outputs_finite_loss_and_perplexity(self) -> None:
        config = TinyModelConfig(vocab_size=32, context_length=8, num_layers=1, d_model=16, num_heads=4, d_ff=64)
        model = TinyDecoderOnlyTransformer(config)
        result = evaluate_next_token_loss(
            model,
            torch.tensor([[1, 2, 3]], dtype=torch.long),
            torch.tensor([[2, 3, 4]], dtype=torch.long),
        )

        self.assertTrue(math.isfinite(result["loss"]))
        self.assertTrue(math.isfinite(result["perplexity"]))


if __name__ == "__main__":
    unittest.main()
