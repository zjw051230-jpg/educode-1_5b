from __future__ import annotations

import sys
import unittest
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.attention_backends import (
    attention_backend_availability,
    causal_attention,
    normalize_attention_backend,
)
from educode.tiny_model import TinyDecoderOnlyTransformer, TinyModelConfig


class AttentionBackendTests(unittest.TestCase):
    def test_sdpa_and_naive_causal_attention_shapes_are_stable(self) -> None:
        torch.manual_seed(123)
        q = torch.randn(2, 3, 5, 7)
        k = torch.randn(2, 3, 5, 7)
        v = torch.randn(2, 3, 5, 7)

        sdpa = causal_attention(q, k, v, backend="sdpa", dropout_p=0.0, training=False)
        naive = causal_attention(q, k, v, backend="naive", dropout_p=0.0, training=False)

        self.assertEqual(sdpa.shape, v.shape)
        self.assertEqual(naive.shape, v.shape)
        self.assertTrue(torch.isfinite(sdpa).all())
        self.assertTrue(torch.isfinite(naive).all())
        self.assertTrue(torch.allclose(sdpa, naive, atol=1e-5, rtol=1e-5))

    def test_tiny_model_default_sdpa_forward_is_unchanged_shape(self) -> None:
        config = TinyModelConfig(
            vocab_size=32,
            context_length=8,
            num_layers=1,
            d_model=16,
            num_heads=4,
            d_ff=32,
            dropout=0.0,
        )
        model = TinyDecoderOnlyTransformer(config)
        input_ids = torch.randint(0, config.vocab_size, (2, 6), dtype=torch.long)

        logits = model(input_ids)

        self.assertEqual(config.attention_backend, "sdpa")
        self.assertEqual(logits.shape, (2, 6, config.vocab_size))

    def test_tiny_model_naive_backend_forward_works_on_cpu(self) -> None:
        config = TinyModelConfig(
            vocab_size=32,
            context_length=8,
            num_layers=1,
            d_model=16,
            num_heads=4,
            d_ff=32,
            dropout=0.0,
            attention_backend="naive",
        )
        model = TinyDecoderOnlyTransformer(config)
        input_ids = torch.randint(0, config.vocab_size, (2, 6), dtype=torch.long)

        logits = model(input_ids)

        self.assertEqual(logits.shape, (2, 6, config.vocab_size))
        self.assertTrue(torch.isfinite(logits).all())

    def test_flash_attention_guard_does_not_import_crash(self) -> None:
        availability = attention_backend_availability("flash_attention_2")

        self.assertTrue(availability.supported_by_config)
        if not availability.available:
            q = torch.randn(1, 2, 4, 8)
            with self.assertRaisesRegex(RuntimeError, "flash_attn is not installed"):
                causal_attention(q, q, q, backend="flash_attention_2", dropout_p=0.0, training=False)

    def test_bad_backend_config_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "attention_backend must be one of"):
            normalize_attention_backend("bad_backend")
        with self.assertRaisesRegex(ValueError, "attention_backend must be one of"):
            TinyModelConfig(
                vocab_size=32,
                context_length=8,
                num_layers=1,
                d_model=16,
                num_heads=4,
                d_ff=32,
                dropout=0.0,
                attention_backend="bad_backend",
            )


if __name__ == "__main__":
    unittest.main()
