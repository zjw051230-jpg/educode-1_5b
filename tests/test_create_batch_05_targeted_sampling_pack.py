from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "create_batch_05_targeted_sampling_pack.py"
SUMMARY_PATH = (
    PROJECT_ROOT
    / "data"
    / "real_corpus"
    / "draft_queue"
    / "domain_synthetic_batch_05"
    / "batch_05_targeted_sampling_summary.json"
)
MANIFEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "real_corpus"
    / "draft_queue"
    / "domain_synthetic_batch_05"
    / "batch_05_targeted_sampling_manifest.jsonl"
)


class CreateBatch05TargetedSamplingPackTest(unittest.TestCase):
    def test_sampling_pack_produces_expected_shape(self) -> None:
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

        self.assertEqual(summary["sampled_total_files"], 120)
        self.assertEqual(len(manifest_rows), 120)
        self.assertEqual(summary["sampled_worker_counts"], {f"CC-{i}": 20 for i in range(1, 7)})
        self.assertEqual(summary["target_total_samples"], 120)
        self.assertGreater(summary["sampled_quality_state_counts"].get("quality_pass", 0), 0)
        self.assertGreater(summary["sampled_quality_state_counts"].get("needs_edit", 0), 0)

        rows_by_worker = {}
        for row in manifest_rows:
            rows_by_worker.setdefault(row["worker_id"], []).append(row)
            self.assertEqual(row["human_review_status"], "pending")
            self.assertIn("writing_form", row)
            self.assertIn("concrete_anchor", row)
            self.assertTrue(row["sample_reason"])
            self.assertTrue(row["suggested_review_focus"])

        self.assertEqual(len(rows_by_worker["CC-2"]), 20)
        self.assertEqual(len(rows_by_worker["CC-5"]), 20)
        self.assertEqual(len(rows_by_worker["CC-6"]), 20)

        self.assertTrue(
            any("repeated_internal_line" in row["risk_flags"] for row in rows_by_worker["CC-2"]),
            "expected CC-2 sampling to include repeated_internal_line cases",
        )
        self.assertTrue(
            any(
                any(flag in {"bilingual_pairing_missing", "thin_section_structure"} for flag in row["risk_flags"])
                for row in rows_by_worker["CC-5"]
            ),
            "expected CC-5 sampling to include bilingual/thin markdown cases",
        )
        self.assertTrue(
            any("trace_note_residue" in row["risk_flags"] for row in rows_by_worker["CC-6"]),
            "expected CC-6 sampling to include trace_note_residue cases",
        )
        self.assertTrue(
            any("thin_section_structure" in row["risk_flags"] for row in rows_by_worker["CC-6"]),
            "expected CC-6 sampling to include thin_section_structure cases",
        )


if __name__ == "__main__":
    unittest.main()
