import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.data_quality import (  # noqa: E402
    detect_near_duplicates,
    shingle_jaccard,
    text_quality_metrics,
)


class DataQualityTests(unittest.TestCase):
    def test_text_quality_metrics_count_lengths_and_repetition(self):
        metrics = text_quality_metrics("hello hello\nshort\n")

        self.assertEqual(metrics["line_count"], 2)
        self.assertEqual(metrics["token_count"], 3)
        self.assertEqual(metrics["max_line_length"], 11)
        self.assertGreater(metrics["repetition_ratio"], 0)

    def test_shingle_jaccard_and_near_duplicate_detection(self):
        a = "machine learning systems need careful validation"
        b = "machine learning systems need careful validation notes"
        c = "completely different topic"

        self.assertGreater(shingle_jaccard(a, b, k=3), 0.5)
        duplicates = detect_near_duplicates([a, b, c], threshold=0.5, k=3)

        self.assertEqual(duplicates, [(0, 1)])

    def test_empty_text_rejected_for_quality_metrics(self):
        with self.assertRaises(ValueError):
            text_quality_metrics("")


if __name__ == "__main__":
    unittest.main()
