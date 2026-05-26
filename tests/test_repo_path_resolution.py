from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_PATH = PROJECT_ROOT / "scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

from run_a100_300m_fineweb_edu_10step_training import (  # noqa: E402
    PROJECT_ROOT as TRAINING_PROJECT_ROOT,
    repo_relative_path,
    resolve_repo_path,
)

CONFIG_RELATIVE_PATH = "configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json"


class RepoPathResolutionTests(unittest.TestCase):
    def test_relative_config_path_is_reported_as_repo_relative(self) -> None:
        self.assertEqual(repo_relative_path(Path(CONFIG_RELATIVE_PATH)), CONFIG_RELATIVE_PATH)

    def test_absolute_config_path_is_reported_as_repo_relative(self) -> None:
        absolute_config_path = TRAINING_PROJECT_ROOT / CONFIG_RELATIVE_PATH

        self.assertEqual(repo_relative_path(absolute_config_path), CONFIG_RELATIVE_PATH)

    def test_resolve_repo_path_accepts_relative_and_absolute_paths(self) -> None:
        absolute_config_path = TRAINING_PROJECT_ROOT / CONFIG_RELATIVE_PATH

        self.assertEqual(resolve_repo_path(CONFIG_RELATIVE_PATH).resolve(), absolute_config_path.resolve())
        self.assertEqual(resolve_repo_path(str(absolute_config_path)).resolve(), absolute_config_path.resolve())


if __name__ == "__main__":
    unittest.main()
