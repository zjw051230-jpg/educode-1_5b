import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.document_boundaries import build_document_boundaries  # noqa: E402
from src.educode.packing import (  # noqa: E402
    PackingConfig,
    build_loss_mask,
    estimate_padding_waste,
    pack_documents,
)


class SequencePackingV2Tests(unittest.TestCase):
    def test_synthetic_docs_packed_and_boundaries_preserved(self):
        docs = [[1, 2, 3], [4, 5], [6, 7, 8]]
        packs = pack_documents(docs, PackingConfig(context_length=6))

        self.assertEqual(len(packs), 2)
        self.assertEqual(build_document_boundaries(packs[0].documents), [(0, 3), (3, 5)])

    def test_padding_waste_and_loss_mask(self):
        docs = [[1, 2, 3], [4, 5]]
        packs = pack_documents(docs, PackingConfig(context_length=6))
        waste = estimate_padding_waste(docs, PackingConfig(context_length=6))
        mask = build_loss_mask(packs[0], context_length=6)

        self.assertEqual(waste["packed_padding_tokens"], 1)
        self.assertEqual(mask, [1, 1, 1, 1, 1, 0])

    def test_invalid_config_rejected(self):
        with self.assertRaises(ValueError):
            PackingConfig(context_length=0)
        with self.assertRaises(ValueError):
            pack_documents([[1, 2, 3, 4]], PackingConfig(context_length=3))


if __name__ == "__main__":
    unittest.main()
