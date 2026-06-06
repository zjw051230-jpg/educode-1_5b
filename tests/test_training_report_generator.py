import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.build_training_report import (  # noqa: E402
    DEFAULT_ARTIFACT_DIRS,
    build_report,
    collect_runs,
    summarize_run,
)


class TrainingReportGeneratorTests(unittest.TestCase):
    def test_summarize_run_reads_summary_and_metric_rows(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact_dir = Path(tmpdir) / "run"
            artifact_dir.mkdir()
            (artifact_dir / "summary.json").write_text(
                json.dumps(
                    {
                        "run_name": "synthetic-run",
                        "success": True,
                        "max_steps": 2,
                        "sequence_length": 128,
                        "batch_size": 3,
                        "gradient_accumulation_steps": 4,
                        "final_train_loss": 1.5,
                        "final_val_loss": 2.25,
                        "approximate_tokens_per_sec": 1234.5,
                        "last_gpu_memory_allocated_gib": 1.25,
                        "last_gpu_memory_reserved_gib": 2.5,
                    }
                ),
                encoding="utf-8",
            )
            (artifact_dir / "metrics.jsonl").write_text(
                json.dumps({"step": 1, "tokens_per_sec": 100.0}) + "\n"
                + json.dumps({"step": 2, "tokens_per_sec": 200.0}) + "\n",
                encoding="utf-8",
            )
            (artifact_dir / "validation_metrics.jsonl").write_text(
                json.dumps({"step": 2, "val_loss": 2.25}) + "\n",
                encoding="utf-8",
            )

            run = summarize_run(artifact_dir)

        self.assertEqual(run.name, "synthetic-run")
        self.assertEqual(run.metrics_rows, 2)
        self.assertEqual(run.validation_rows, 1)
        self.assertEqual(run.mean_step_tokens_per_sec, 150.0)

    def test_build_report_includes_existing_imported_artifacts(self):
        runs = collect_runs(DEFAULT_ARTIFACT_DIRS)
        report = build_report(runs)

        self.assertGreaterEqual(len(runs), 4)
        self.assertIn("Training Report Summary", report)
        self.assertIn("seq512", report)
        self.assertIn("seq1024", report)
        self.assertIn("Quality Caveat", report)


if __name__ == "__main__":
    unittest.main()
