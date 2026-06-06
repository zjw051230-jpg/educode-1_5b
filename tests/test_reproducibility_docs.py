import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class ReproducibilityDocsTests(unittest.TestCase):
    def test_environment_summary_script_writes_local_only_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "environment_summary.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts/capture_environment_summary.py"),
                    "--output",
                    str(output_path),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=True,
            )

            payload = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertIn("python_version", payload)
        self.assertIn("platform", payload)
        self.assertFalse(payload["modal_gpu_training_run"])
        self.assertIn("environment_summary_status", result.stdout)

    def test_model_card_template_contains_evidence_caveats(self):
        template = (REPO_ROOT / "docs/model_card_template.md").read_text(
            encoding="utf-8"
        )
        checklist = (REPO_ROOT / "docs/reproducibility_checklist.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("not a finished foundation model", template.lower())
        self.assertIn("short profiling runs are systems evidence", template.lower())
        self.assertIn("raw datasets", checklist.lower())
        self.assertIn("modal/gpu/training run: no", checklist.lower())


if __name__ == "__main__":
    unittest.main()
