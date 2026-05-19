from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "validate_draft_corpus_batch_05.py"
SUMMARY_PATH = (
    PROJECT_ROOT
    / "data"
    / "real_corpus"
    / "draft_queue"
    / "domain_synthetic_batch_05"
    / "batch_05_validation_summary.json"
)


class ValidateDraftCorpusBatch05Test(unittest.TestCase):
    def test_validator_produces_expected_batch_05_counts(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

        summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))

        self.assertEqual(summary["total_topic_files"], 600)
        self.assertEqual(summary["markdown_topic_files"], 365)
        self.assertEqual(summary["python_topic_files"], 235)
        self.assertEqual(summary["worker_manifest_count"], 6)
        self.assertEqual(summary["batch_summary_count"], 6)
        self.assertEqual(summary["anti_template_self_check_count"], 6)
        self.assertEqual(summary["progress_checkpoint_count"], 24)
        self.assertEqual(summary["missing_files"], 0)
        self.assertEqual(summary["metadata_errors"], 0)
        self.assertEqual(summary["scope_errors"], 0)
        self.assertEqual(summary["credential_style_secret_hit_count"], 0)
        self.assertIn(summary["validation_status"], {"passed", "passed_with_notes"})


if __name__ == "__main__":
    unittest.main()
