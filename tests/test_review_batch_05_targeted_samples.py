from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLING_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "create_batch_05_targeted_sampling_pack.py"
REVIEW_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "review_batch_05_targeted_samples.py"
SUMMARY_PATH = (
    PROJECT_ROOT
    / "data"
    / "real_corpus"
    / "draft_queue"
    / "domain_synthetic_batch_05"
    / "batch_05_targeted_sample_review_summary.json"
)
MANIFEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "real_corpus"
    / "draft_queue"
    / "domain_synthetic_batch_05"
    / "batch_05_targeted_sample_review_manifest.jsonl"
)


class ReviewBatch05TargetedSamplesTest(unittest.TestCase):
    def test_sampled_review_produces_expected_summary(self) -> None:
        sampling_result = subprocess.run(
            [sys.executable, str(SAMPLING_SCRIPT_PATH)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(sampling_result.returncode, 0, sampling_result.stderr or sampling_result.stdout)

        review_result = subprocess.run(
            [sys.executable, str(REVIEW_SCRIPT_PATH)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(review_result.returncode, 0, review_result.stderr or review_result.stdout)

        summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
        manifest_rows = [
            json.loads(line)
            for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        rows_by_topic = {row["topic_id"]: row for row in manifest_rows}

        self.assertEqual(summary["total_reviewed_samples"], 120)
        self.assertEqual(len(manifest_rows), 120)
        self.assertEqual(summary["reject_count"], 0)
        self.assertGreater(summary["keep_as_candidate_count"], 0)
        self.assertGreater(summary["needs_rewrite_count"], 0)
        self.assertIn(summary["promotion_readiness"], {"may_support_small_promotion_subset", "still_needs_another_repair_pass"})

        pds = rows_by_topic["B05-PDS-0001"]
        self.assertEqual(pds["promotion_decision"], "needs_rewrite")
        self.assertEqual(pds["template_repetition_risk"], "high")

        cod = rows_by_topic["B05-COD-0027"]
        self.assertEqual(cod["promotion_decision"], "needs_rewrite")
        self.assertEqual(cod["python_topic_fit"], "high")

        for row in manifest_rows:
            self.assertIn(row["topic_specificity"], {"high", "medium", "low"})
            self.assertIn(row["concrete_anchor_quality"], {"high", "medium", "low"})
            self.assertIn(row["template_repetition_risk"], {"high", "medium", "low"})
            self.assertIn(row["educational_value"], {"high", "medium", "low"})
            self.assertIn(row["python_topic_fit"], {"high", "medium", "low", "not_applicable"})
            self.assertIn(row["bilingual_quality"], {"high", "medium", "low", "not_applicable"})
            self.assertTrue(isinstance(row["metadata_ok"], bool))
            self.assertTrue(row["review_notes"])


if __name__ == "__main__":
    unittest.main()
