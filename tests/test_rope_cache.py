from __future__ import annotations

import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.rope import apply_rotary_emb, build_rope_cache, rotate_half  # noqa: E402


class RoPECacheTests(unittest.TestCase):
    def test_rope_cache_shape(self) -> None:
        cache = build_rope_cache(seq_len=8, head_dim=16)

        self.assertEqual(tuple(cache.cos.shape), (8, 8))
        self.assertEqual(tuple(cache.sin.shape), (8, 8))

    def test_apply_rotary_emb_preserves_qk_shape(self) -> None:
        q = torch.randn(2, 4, 8, 16)
        k = torch.randn(2, 4, 8, 16)
        q_rot, k_rot = apply_rotary_emb(q, k, build_rope_cache(seq_len=8, head_dim=16))

        self.assertEqual(tuple(q_rot.shape), tuple(q.shape))
        self.assertEqual(tuple(k_rot.shape), tuple(k.shape))

    def test_rotate_half_and_bad_head_dim(self) -> None:
        self.assertEqual(tuple(rotate_half(torch.randn(2, 4)).shape), (2, 4))
        with self.assertRaises(ValueError):
            build_rope_cache(seq_len=8, head_dim=15)

    def test_bad_scaling_factor_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_rope_cache(seq_len=8, head_dim=16, scaling_factor=0)


if __name__ == "__main__":
    unittest.main()
