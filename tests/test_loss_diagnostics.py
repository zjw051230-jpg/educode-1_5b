import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.diagnostics import (  # noqa: E402
    diagnose_metrics,
    detect_loss_spikes,
    read_metrics_jsonl,
    rolling_average,
)


class LossDiagnosticsTests(unittest.TestCase):
    def test_read_metrics_jsonl_rejects_non_finite_loss(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "metrics.jsonl"
            path.write_text(
                json.dumps({"step": 1, "train_loss": 3.0}) + "\n"
                + json.dumps({"step": 2, "train_loss": float("nan")}) + "\n",
                encoding="utf-8",
            )

            rows = read_metrics_jsonl(path)
            report = diagnose_metrics(rows)

        self.assertEqual(len(rows), 2)
        self.assertFalse(report.losses_all_finite)
        self.assertEqual(report.non_finite_steps, [2])

    def test_detect_loss_spikes_and_rolling_average(self):
        losses = [5.0, 4.8, 4.7, 9.8, 4.6]

        spikes = detect_loss_spikes(losses, threshold_ratio=1.5)
        smoothed = rolling_average(losses, window=3)

        self.assertEqual(spikes, [3])
        self.assertTrue(all(math.isfinite(value) for value in smoothed))
        self.assertAlmostEqual(smoothed[-1], (4.7 + 9.8 + 4.6) / 3)

    def test_existing_imported_metrics_parse_without_gpu(self):
        path = (
            REPO_ROOT
            / "experiments/a100/fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile/results_imported_modal_streaming/metrics.jsonl"
        )

        report = diagnose_metrics(read_metrics_jsonl(path))

        self.assertEqual(report.row_count, 50)
        self.assertTrue(report.losses_all_finite)
        self.assertGreater(report.final_train_loss, 0)
        self.assertGreater(report.mean_tokens_per_sec, 0)


if __name__ == "__main__":
    unittest.main()
