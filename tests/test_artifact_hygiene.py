from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_PATH = PROJECT_ROOT / "scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

from check_artifact_hygiene import classify_paths  # noqa: E402


class ArtifactHygieneTests(unittest.TestCase):
    def reasons_for(self, paths: list[str], sizes: dict[str, int | None] | None = None) -> list[str]:
        return [finding.reason for finding in classify_paths(paths, sizes=sizes or {})]

    def test_tarballs_and_checkpoints_are_blocked(self) -> None:
        reasons = self.reasons_for(
            [
                "mvp30_a100_5gb_50step_seq1024_sdpa_profile_results.tar.gz",
                "experiments/a100/run/checkpoints/model.pt",
                "experiments/a100/run/final.safetensors",
            ]
        )

        self.assertIn("forbidden large artifact or checkpoint suffix", reasons)
        self.assertIn("checkpoint path must not be committed", reasons)

    def test_small_imported_json_markdown_files_are_allowed(self) -> None:
        findings = classify_paths(
            [
                "experiments/a100/sample/results_imported_modal_streaming/summary.json",
                "experiments/a100/sample/results_imported_modal_streaming/metrics.jsonl",
                "experiments/a100/sample/results_imported_modal_streaming/summary.md",
            ]
        )

        self.assertEqual(findings, [])

    def test_non_text_imported_result_file_is_blocked(self) -> None:
        reasons = self.reasons_for(
            ["experiments/a100/sample/results_imported_modal_streaming/checkpoint.pt"]
        )

        self.assertIn("imported results must stay small text artifacts", reasons)

    def test_raw_prepared_and_split_data_paths_are_blocked(self) -> None:
        reasons = self.reasons_for(
            [
                "data/real_corpus/raw/source/file.txt",
                "data/public_corpus/prepared_data/train.bin",
                "data/real_corpus/splits/train.jsonl",
            ]
        )

        self.assertIn("raw/prepared/split data path must not be committed", reasons)

    def test_large_experiment_file_is_blocked(self) -> None:
        path = "experiments/a100/run/results_imported_modal_streaming/large.json"
        reasons = self.reasons_for([path], sizes={path: 6 * 1024 * 1024})

        self.assertIn("large experiment artifact must not be committed", reasons)


if __name__ == "__main__":
    unittest.main()
