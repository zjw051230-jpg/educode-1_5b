from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_PATH = PROJECT_ROOT / "scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

from build_experiment_matrix import (  # noqa: E402
    COMPLETED_SOURCES,
    PLANNED_CANDIDATES,
    build_matrix,
    completed_row,
)


class ExperimentPlannerTests(unittest.TestCase):
    def test_completed_sources_are_small_json_summaries(self) -> None:
        for source in COMPLETED_SOURCES:
            self.assertEqual(source.summary_path.suffix, ".json")
            self.assertNotIn(".tar.gz", source.summary_path.as_posix())

    def test_completed_row_extracts_core_systems_fields(self) -> None:
        row = completed_row(
            COMPLETED_SOURCES[1],
            {
                "analysis_status": "passed",
                "blocker_count": 0,
                "context_length": 512,
                "batch_size": 8,
                "max_steps": 50,
                "attention_backend": "sdpa",
                "summary_tokens_per_sec": 44100.0,
                "average_step_time_seconds": 0.37,
                "peak_reserved_memory_gib": 8.4,
            },
        )

        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["context_length"], 512)
        self.assertEqual(row["attention_backend"], "sdpa")

    def test_planned_candidates_mark_gpu_gates(self) -> None:
        gpu_candidates = [candidate for candidate in PLANNED_CANDIDATES if candidate["requires_gpu"]]

        self.assertGreaterEqual(len(gpu_candidates), 1)
        self.assertTrue(all("cost_gate" in candidate for candidate in PLANNED_CANDIDATES))

    def test_build_matrix_from_current_artifacts_passes(self) -> None:
        matrix = build_matrix(PROJECT_ROOT)

        self.assertEqual(matrix["matrix_status"], "passed")
        self.assertEqual(matrix["blocker_count"], 0)
        self.assertGreaterEqual(matrix["completed_count"], 4)
        self.assertFalse(matrix["reads_tarballs"])
        self.assertFalse(matrix["runs_gpu"])


if __name__ == "__main__":
    unittest.main()
