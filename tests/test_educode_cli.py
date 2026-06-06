import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "scripts" / "educode_cli.py"


class EduCodeCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_help_works_and_has_no_training_command(self):
        result = self.run_cli("--help")

        self.assertEqual(result.returncode, 0)
        self.assertIn("list-runs", result.stdout)
        self.assertNotIn("train", result.stdout)
        self.assertNotIn("modal", result.stdout.lower())

    def test_list_runs_reads_imported_dirs_not_tarballs(self):
        result = self.run_cli("list-runs")

        self.assertEqual(result.returncode, 0)
        self.assertIn("tarballs_read=false", result.stdout)
        self.assertIn("runs_found=", result.stdout)

    def test_invalid_command_rejected(self):
        result = self.run_cli("run-training")

        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
