from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "review_draft_corpus_quality_batch_05.py"
SUMMARY_PATH = (
    PROJECT_ROOT
    / "data"
    / "real_corpus"
    / "draft_queue"
    / "domain_synthetic_batch_05"
    / "batch_05_quality_review_summary.json"
)
MANIFEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "real_corpus"
    / "draft_queue"
    / "domain_synthetic_batch_05"
    / "batch_05_quality_review_manifest.jsonl"
)


class ReviewDraftCorpusQualityBatch05Test(unittest.TestCase):
    def test_quality_review_produces_expected_batch_05_summary(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

        summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
        manifest_rows = [
            json.loads(line)
            for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        rows_by_topic = {row["topic_id"]: row for row in manifest_rows}

        self.assertEqual(summary["total_records"], 600)
        self.assertEqual(summary["file_type_counts"], {"markdown": 365, "python": 235})
        self.assertEqual(summary["quality_gate_status"], "passed_with_notes")
        self.assertEqual(summary["reject_count"], 0)
        self.assertGreater(summary["needs_edit_count"], 0)
        self.assertGreater(summary["flag_counts"].get("repeated_internal_line", 0), 0)
        self.assertEqual(len(manifest_rows), 600)

        self.assertEqual(rows_by_topic["B05-PDS-0001"]["quality_state"], "needs_edit")
        self.assertIn("repeated_internal_line", rows_by_topic["B05-PDS-0001"]["quality_flags"])
        self.assertEqual(rows_by_topic["B05-COD-0027"]["quality_state"], "needs_edit")
        self.assertIn("trace_note_residue", rows_by_topic["B05-COD-0027"]["quality_flags"])


if __name__ == "__main__":
    unittest.main()
