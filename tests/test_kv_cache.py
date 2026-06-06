from __future__ import annotations

import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.inference import decode_one, prefill  # noqa: E402
from educode.kv_cache import KVCache  # noqa: E402
from educode.paged_cache import PagedBlockTable  # noqa: E402
from educode.tiny_model import TinyDecoderOnlyTransformer, TinyModelConfig  # noqa: E402


class KVCacheTests(unittest.TestCase):
    def test_kv_cache_append_read_reset(self) -> None:
        cache = KVCache(num_layers=1)
        key = torch.zeros(1, 2, 1, 4)
        cache.append(0, key, key)
        cache.append(0, key, key)
        stored_key, stored_value = cache.read(0)

        self.assertEqual(cache.sequence_length(), 2)
        self.assertEqual(tuple(stored_key.shape), (1, 2, 2, 4))
        self.assertEqual(tuple(stored_value.shape), (1, 2, 2, 4))
        cache.reset()
        self.assertEqual(cache.sequence_length(), 0)

    def test_prefill_decode_shapes(self) -> None:
        config = TinyModelConfig(vocab_size=32, context_length=8, num_layers=1, d_model=16, num_heads=4, d_ff=64)
        model = TinyDecoderOnlyTransformer(config)
        input_ids = torch.tensor([[1, 2, 3]], dtype=torch.long)
        prefill_logits, _ = prefill(model, input_ids, KVCache(num_layers=1))
        decode_logits, _ = decode_one(model, input_ids[:, -1:], KVCache(num_layers=1))

        self.assertEqual(tuple(prefill_logits.shape), (1, 3, 32))
        self.assertEqual(tuple(decode_logits.shape), (1, 1, 32))

    def test_paged_block_table(self) -> None:
        table = PagedBlockTable(block_size=4)
        blocks = table.allocate(sequence_id=1, token_count=9)

        self.assertEqual(len(blocks), 3)
        self.assertEqual(table.lookup(1), blocks)
        table.release(1)
        self.assertEqual(table.lookup(1), [])


if __name__ == "__main__":
    unittest.main()
