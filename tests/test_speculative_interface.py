from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.speculative import NgramProposer, speculative_decode_skeleton  # noqa: E402


class SpeculativeInterfaceTests(unittest.TestCase):
    def test_ngram_proposer_returns_requested_tokens(self) -> None:
        proposer = NgramProposer(ngram_size=2, fallback_token_id=0)
        draft = proposer.propose([1, 2, 3, 4], max_tokens=5)

        self.assertEqual(draft, [3, 4, 3, 4, 3])

    def test_speculative_skeleton_marks_verification_required(self) -> None:
        result = speculative_decode_skeleton([1, 2, 1, 2], NgramProposer(), max_draft_tokens=3)

        self.assertEqual(len(result["draft_tokens"]), 3)
        self.assertTrue(result["requires_target_model_verification"])


if __name__ == "__main__":
    unittest.main()
