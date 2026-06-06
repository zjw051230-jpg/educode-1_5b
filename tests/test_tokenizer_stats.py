import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.tokenizer_stats import TokenizerStatsConfig, analyze_tokenizer_stats  # noqa: E402


class TokenizerStatsTests(unittest.TestCase):
    def test_small_fixture_stats(self):
        report = analyze_tokenizer_stats(
            "hello <bos> world hello",
            TokenizerStatsConfig(special_tokens=("<bos>", "<eos>")),
        )

        self.assertEqual(report["token_count"], 4)
        self.assertEqual(report["frequency"]["hello"], 2)
        self.assertEqual(report["special_token_count"], 1)
        self.assertGreater(report["bytes_per_token"], 0)

    def test_empty_text_rejected(self):
        with self.assertRaises(ValueError):
            analyze_tokenizer_stats("", TokenizerStatsConfig())


if __name__ == "__main__":
    unittest.main()
