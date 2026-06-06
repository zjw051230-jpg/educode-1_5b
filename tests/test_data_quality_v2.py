import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.data_quality import QualityConfig, quality_metrics  # noqa: E402


class DataQualityV2Tests(unittest.TestCase):
    def test_quality_stats_deterministic(self):
        text = "hello hello\nclean line\n"
        first = quality_metrics(text, QualityConfig())
        second = quality_metrics(text, QualityConfig())

        self.assertEqual(first, second)
        self.assertEqual(first["line_count"], 2)
        self.assertGreater(first["repetition_ratio"], 0)

    def test_bad_config_rejected(self):
        with self.assertRaises(ValueError):
            QualityConfig(low_information_unique_token_threshold=-1)


if __name__ == "__main__":
    unittest.main()
