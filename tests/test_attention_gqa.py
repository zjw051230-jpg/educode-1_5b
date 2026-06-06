from __future__ import annotations

import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.attention_backends import causal_attention  # noqa: E402
from educode.attention_utils import repeat_kv_for_gqa, validate_qkv_shapes  # noqa: E402


class AttentionGQATests(unittest.TestCase):
    def test_repeat_kv_for_gqa_shape(self) -> None:
        kv = torch.randn(2, 2, 5, 8)
        repeated = repeat_kv_for_gqa(kv, num_query_heads=4)

        self.assertEqual(tuple(repeated.shape), (2, 4, 5, 8))
        self.assertTrue(torch.equal(repeated[:, 0], kv[:, 0]))
        self.assertTrue(torch.equal(repeated[:, 1], kv[:, 0]))

    def test_gqa_attention_shapes(self) -> None:
        q = torch.randn(2, 4, 5, 8)
        k = torch.randn(2, 2, 5, 8)
        v = torch.randn(2, 2, 5, 8)
        out = causal_attention(q, k, v, backend="naive")

        self.assertEqual(tuple(out.shape), tuple(q.shape))

    def test_bad_gqa_shape_rejected(self) -> None:
        with self.assertRaises(ValueError):
            repeat_kv_for_gqa(torch.randn(2, 3, 5, 8), num_query_heads=4)
        with self.assertRaises(ValueError):
            validate_qkv_shapes(torch.randn(2, 4, 5, 8), torch.randn(2, 2, 4, 8), torch.randn(2, 2, 5, 8))


if __name__ == "__main__":
    unittest.main()
