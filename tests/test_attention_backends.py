from __future__ import annotations

import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.attention_backends import (  # noqa: E402
    backend_availability,
    causal_attention,
    flash_attention_2_availability,
    normalize_attention_backend,
)
from educode.tiny_model import TinyDecoderOnlyTransformer, TinyModelConfig  # noqa: E402


class AttentionBackendTests(unittest.TestCase):
    def test_sdpa_and_naive_outputs_match_for_small_cpu_tensor(self) -> None:
        torch.manual_seed(7)
        q = torch.randn(2, 3, 5, 4)
        k = torch.randn(2, 3, 5, 4)
        v = torch.randn(2, 3, 5, 4)

        sdpa = causal_attention(q, k, v, backend="sdpa")
        naive = causal_attention(q, k, v, backend="naive")

        self.assertTrue(torch.allclose(sdpa, naive, atol=1e-5, rtol=1e-5))

    def test_tiny_model_forward_supports_sdpa_and_naive(self) -> None:
        for backend in ("sdpa", "naive"):
            config = TinyModelConfig(
                vocab_size=32,
                context_length=8,
                num_layers=1,
                d_model=16,
                num_heads=4,
                d_ff=64,
                attention_backend=backend,
            )
            model = TinyDecoderOnlyTransformer(config)
            input_ids = torch.randint(0, 32, (2, 8), dtype=torch.long)
            logits = model(input_ids)

            self.assertEqual(tuple(logits.shape), (2, 8, 32))

    def test_flash_attention_unavailable_is_graceful(self) -> None:
        availability = flash_attention_2_availability()

        self.assertEqual(availability.backend, "flash_attention_2")
        self.assertIsInstance(availability.available, bool)
        self.assertTrue(availability.reason)

    def test_bad_backend_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            normalize_attention_backend("definitely_not_a_backend")
        with self.assertRaises(ValueError):
            TinyModelConfig(
                vocab_size=32,
                context_length=8,
                num_layers=1,
                d_model=16,
                num_heads=4,
                d_ff=64,
                attention_backend="definitely_not_a_backend",
            )

    def test_backend_availability_reports_supported_backends(self) -> None:
        self.assertTrue(backend_availability("sdpa").available)
        self.assertTrue(backend_availability("naive").available)
        self.assertEqual(backend_availability("flash_attention_2").backend, "flash_attention_2")


if __name__ == "__main__":
    unittest.main()
