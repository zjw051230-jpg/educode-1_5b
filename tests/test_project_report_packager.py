from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_PATH = PROJECT_ROOT / "scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

from build_project_report_package import (  # noqa: E402
    build_report_text,
    collect_report_sources,
    is_safe_report_source,
    write_project_report,
)


class ProjectReportPackagerTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> None:
        docs_dir = root / "docs"
        imported_dir = root / "experiments" / "a100" / "demo" / "results_imported_modal_streaming"
        raw_dir = root / "data" / "public_corpus" / "raw"
        checkpoint_dir = root / "experiments" / "a100" / "demo" / "checkpoints"
        docs_dir.mkdir(parents=True)
        imported_dir.mkdir(parents=True)
        raw_dir.mkdir(parents=True)
        checkpoint_dir.mkdir(parents=True)

        (docs_dir / "mvp_summary.md").write_text("# MVP Summary\n\nKey finding.\n", encoding="utf-8")
        (imported_dir / "summary.json").write_text(
            json.dumps({"run_name": "demo", "success": True, "max_steps": 50}),
            encoding="utf-8",
        )
        (root / "result.tar.gz").write_bytes(b"do-not-read")
        (checkpoint_dir / "checkpoint.pt").write_bytes(b"do-not-read")
        (raw_dir / "sample.txt").write_text("do not include", encoding="utf-8")

    def test_collect_report_sources_excludes_large_artifacts_and_raw_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_fixture(root)

            sources = collect_report_sources(root)
            source_paths = [source.path for source in sources]

            self.assertIn("docs/mvp_summary.md", source_paths)
            self.assertIn("experiments/a100/demo/results_imported_modal_streaming/summary.json", source_paths)
            self.assertNotIn("result.tar.gz", source_paths)
            self.assertNotIn("experiments/a100/demo/checkpoints/checkpoint.pt", source_paths)
            self.assertNotIn("data/public_corpus/raw/sample.txt", source_paths)

    def test_report_generation_is_deterministic_and_references_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_fixture(root)
            sources = collect_report_sources(root)

            first = build_report_text(sources)
            second = build_report_text(sources)

            self.assertEqual(first, second)
            self.assertIn("docs/mvp_summary.md", first)
            self.assertIn("experiments/a100/demo/results_imported_modal_streaming/summary.json", first)
            self.assertIn("excluded tarballs/checkpoints/raw data", first)

    def test_write_project_report_stays_under_safe_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_fixture(root)
            output_path = root / "docs" / "generated" / "project_report.md"

            report_path = write_project_report(root, output_path)

            self.assertEqual(report_path, output_path)
            self.assertTrue(output_path.exists())
            self.assertIn("Project Report Package", output_path.read_text(encoding="utf-8"))

    def test_safe_source_classifier_rejects_forbidden_paths(self) -> None:
        self.assertFalse(is_safe_report_source("model.safetensors"))
        self.assertFalse(is_safe_report_source("experiments/a100/run/checkpoints/model.pt"))
        self.assertFalse(is_safe_report_source("data/public_corpus/raw/file.txt"))
        self.assertTrue(is_safe_report_source("docs/analysis.md"))


if __name__ == "__main__":
    unittest.main()
