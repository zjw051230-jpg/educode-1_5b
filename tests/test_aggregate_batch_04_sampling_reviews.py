from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "aggregate_batch_04_sampling_reviews.py"
AGGREGATE_JSON_PATH = (
    PROJECT_ROOT
    / "data"
    / "real_corpus"
    / "draft_queue"
    / "domain_synthetic_batch_04"
    / "reviews"
    / "batch_04_sampling_review_aggregate.json"
)


class AggregateBatch04SamplingReviewsTest(unittest.TestCase):
    def test_aggregate_script_produces_expected_batch_04_decision(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

        aggregate = json.loads(AGGREGATE_JSON_PATH.read_text(encoding="utf-8"))

        self.assertEqual(aggregate["reviewed_samples"], 240)
        self.assertEqual(aggregate["decision_counts"]["strong_candidate_for_promotion"], 0)
        self.assertEqual(aggregate["decision_counts"]["keep_as_candidate"], 24)
        self.assertEqual(aggregate["decision_counts"]["needs_rewrite"], 216)
        self.assertEqual(aggregate["decision_counts"]["reject"], 0)
        self.assertEqual(aggregate["promotion_readiness"], "not_ready_for_promotion")


if __name__ == "__main__":
    unittest.main()
