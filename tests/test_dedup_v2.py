import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.dedup import detect_exact_duplicates, detect_near_duplicates, shingle_jaccard  # noqa: E402


class DedupV2Tests(unittest.TestCase):
    def test_exact_duplicate_detected(self):
        texts = ["alpha beta", "gamma", "alpha beta"]

        self.assertEqual(detect_exact_duplicates(texts), [(0, 2)])

    def test_near_duplicate_detected(self):
        a = "machine learning systems need careful validation"
        b = "machine learning systems need careful validation notes"

        self.assertGreater(shingle_jaccard(a, b, k=3), 0.5)
        self.assertEqual(detect_near_duplicates([a, b], threshold=0.5, k=3), [(0, 1)])


if __name__ == "__main__":
    unittest.main()
