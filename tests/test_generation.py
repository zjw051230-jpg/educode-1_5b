from __future__ import annotations

import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.generation import generate_token_ids  # noqa: E402
from educode.tiny_model import TinyDecoderOnlyTransformer, TinyModelConfig  # noqa: E402


class ToyTokenizer:
    def encode(self, prompt: str) -> list[int]:
        return [min(ord(char), 31) for char in prompt] or [1]

    def decode(self, token_ids: list[int]) -> str:
        return " ".join(str(token_id) for token_id in token_ids)


class GenerationTests(unittest.TestCase):
    def setUp(self) -> None:
        torch.manual_seed(9)
        config = TinyModelConfig(vocab_size=32, context_length=16, num_layers=1, d_model=16, num_heads=4, d_ff=64)
        self.model = TinyDecoderOnlyTransformer(config)
        self.tokenizer = ToyTokenizer()

    def test_greedy_generation_is_deterministic(self) -> None:
        first = generate_token_ids(self.model, self.tokenizer, "abc", 4, torch.device("cpu"), strategy="greedy")
        second = generate_token_ids(self.model, self.tokenizer, "abc", 4, torch.device("cpu"), strategy="greedy")

        self.assertEqual(first, second)

    def test_sampling_seed_is_deterministic(self) -> None:
        first = generate_token_ids(self.model, self.tokenizer, "abc", 4, torch.device("cpu"), seed=123, top_k=4)
        second = generate_token_ids(self.model, self.tokenizer, "abc", 4, torch.device("cpu"), seed=123, top_k=4)

        self.assertEqual(first, second)

    def test_eos_stops_generation(self) -> None:
        token_ids = generate_token_ids(
            self.model,
            self.tokenizer,
            "abc",
            4,
            torch.device("cpu"),
            strategy="greedy",
            eos_token_id=0,
        )

        self.assertLessEqual(len(token_ids), len(self.tokenizer.encode("abc")) + 4)


if __name__ == "__main__":
    unittest.main()
