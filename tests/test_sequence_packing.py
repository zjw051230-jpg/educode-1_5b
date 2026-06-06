import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.packing import (  # noqa: E402
    estimate_padding_waste,
    pack_document_lengths,
    token_utilization,
)


class SequencePackingTests(unittest.TestCase):
    def test_document_lengths_pack_without_crossing_context_limit(self):
        packs = pack_document_lengths([5, 4, 7, 3], context_length=10)

        self.assertEqual(packs, [[5, 4], [7, 3]])
        self.assertTrue(all(sum(pack) <= 10 for pack in packs))

    def test_token_utilization_and_padding_waste(self):
        packs = [[5, 4], [7, 3]]

        utilization = token_utilization(packs, context_length=10)
        waste = estimate_padding_waste([5, 4, 7, 3], context_length=10)

        self.assertEqual(utilization["used_tokens"], 19)
        self.assertEqual(utilization["capacity_tokens"], 20)
        self.assertAlmostEqual(utilization["utilization_ratio"], 0.95)
        self.assertEqual(waste["unpacked_padding_tokens"], 21)
        self.assertEqual(waste["packed_padding_tokens"], 1)

    def test_invalid_lengths_rejected(self):
        with self.assertRaises(ValueError):
            pack_document_lengths([11], context_length=10)
        with self.assertRaises(ValueError):
            pack_document_lengths([0], context_length=10)


if __name__ == "__main__":
    unittest.main()
