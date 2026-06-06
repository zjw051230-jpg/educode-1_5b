from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.tokenizer_training import (  # noqa: E402
    TokenizerTrainingConfig,
    ToyByteTokenizer,
    validate_special_tokens,
    vocab_stats,
)


class TokenizerTrainingConfigTests(unittest.TestCase):
    def test_valid_config_is_accepted(self) -> None:
        config = TokenizerTrainingConfig(vocab_size=256, min_frequency=2, sample_limit=100)

        self.assertEqual(config.vocab_size, 256)
        self.assertEqual(config.algorithm, "byte_level_bpe")

    def test_bad_vocab_size_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TokenizerTrainingConfig(vocab_size=3)

    def test_special_tokens_must_be_unique_and_required(self) -> None:
        with self.assertRaises(ValueError):
            validate_special_tokens(["<|endoftext|>", "<|pad|>", "<|pad|>"])
        with self.assertRaises(ValueError):
            validate_special_tokens(["<|pad|>", "<|unk|>"])

    def test_toy_byte_tokenizer_round_trips_small_fixture(self) -> None:
        tokenizer = ToyByteTokenizer()
        text = "hello EduCode"

        token_ids = tokenizer.encode(text)
        decoded = tokenizer.decode(token_ids)

        self.assertEqual(decoded, text)
        self.assertTrue(all(isinstance(token_id, int) for token_id in token_ids))

    def test_vocab_stats_reports_special_and_byte_tokens(self) -> None:
        stats = vocab_stats(ToyByteTokenizer())

        self.assertGreaterEqual(stats["vocab_size"], 259)
        self.assertEqual(stats["special_token_count"], 3)
        self.assertEqual(stats["unk_token"], "<|unk|>")


if __name__ == "__main__":
    unittest.main()
