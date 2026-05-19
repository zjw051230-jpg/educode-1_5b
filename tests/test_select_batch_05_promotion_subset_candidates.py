from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLING_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "create_batch_05_targeted_sampling_pack.py"
REVIEW_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "review_batch_05_targeted_samples.py"
SELECTOR_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "select_batch_05_promotion_subset_candidates.py"
SUMMARY_PATH = (
    PROJECT_ROOT
    / "data"
    / "real_corpus"
    / "draft_queue"
    / "domain_synthetic_batch_05"
    / "batch_05_promotion_subset_summary.json"
)
MANIFEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "real_corpus"
    / "draft_queue"
    / "domain_synthetic_batch_05"
    / "batch_05_promotion_subset_candidates.jsonl"
)


class SelectBatch05PromotionSubsetCandidatesTest(unittest.TestCase):
    def test_selector_outputs_only_strong_candidates(self) -> None:
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

        selector_result = subprocess.run(
            [sys.executable, str(SELECTOR_SCRIPT_PATH)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(selector_result.returncode, 0, selector_result.stderr or selector_result.stdout)

        summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
        manifest_rows = [
            json.loads(line)
            for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        self.assertEqual(summary["selected_count"], 92)
        self.assertEqual(summary["excluded_keep_as_candidate"], 17)
        self.assertEqual(summary["excluded_needs_rewrite"], 11)
        self.assertEqual(summary["excluded_reject"], 0)
        self.assertEqual(len(manifest_rows), 92)
        self.assertEqual(summary["selected_by_worker"], {"CC-1": 20, "CC-2": 11, "CC-3": 20, "CC-4": 20, "CC-5": 11, "CC-6": 10})
        self.assertEqual(summary["selected_file_type_counts"], {"markdown": 45, "python": 47})
        self.assertEqual(summary["source_batch_id"], "domain_synthetic_batch_05")
        self.assertFalse(summary["formal_promotion_done"])
        self.assertFalse(summary["intake_done"])
        self.assertFalse(summary["tokenizer_training_done"])
        self.assertFalse(summary["model_training_done"])

        candidate_ids = set()
        topic_ids = set()
        for row in manifest_rows:
            self.assertNotIn(row["candidate_id"], candidate_ids)
            candidate_ids.add(row["candidate_id"])
            topic_ids.add(row["topic_id"])
            self.assertEqual(row["promotion_decision_from_d19_3"], "strong_candidate_for_promotion")
            self.assertTrue(row["selected_for_promotion_subset"])
            self.assertFalse(row["approved_for_training"])
            self.assertEqual(row["formal_promotion_status"], "candidate_only_not_promoted")
            self.assertEqual(row["source_batch_id"], "domain_synthetic_batch_05")
            self.assertEqual(row["source_category"], "synthetic_examples")
            self.assertEqual(row["required_next_step"], "D20.2 formal promotion copy/review")
            self.assertTrue(row["worker_id"])
            self.assertTrue(row["topic_id"])
            self.assertTrue(row["selection_reason"])
            self.assertIn(row["file_type"], {"markdown", "python"})
            self.assertTrue((PROJECT_ROOT / row["file_path"]).exists())

        self.assertIn("B05-MLF-0066", topic_ids)
        self.assertNotIn("B05-PDS-0001", topic_ids)
        self.assertNotIn("B05-COD-0027", topic_ids)


if __name__ == "__main__":
    unittest.main()
