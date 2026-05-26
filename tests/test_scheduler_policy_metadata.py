from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_PATH = PROJECT_ROOT / "scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

from run_a100_300m_fineweb_edu_10step_training import build_scheduler_metadata, get_scheduler_policy


class SchedulerPolicyMetadataTests(unittest.TestCase):
    def test_missing_scheduler_defaults_to_constant_policy(self) -> None:
        self.assertEqual(get_scheduler_policy({}), "constant")

    def test_scheduler_without_policy_defaults_to_constant_policy(self) -> None:
        config = {"scheduler": {"enabled": False, "name": None}}

        self.assertEqual(get_scheduler_policy(config), "constant")

    def test_scheduler_constant_policy_is_explicit(self) -> None:
        config = {"scheduler": {"enabled": False, "policy": "constant"}}

        self.assertEqual(get_scheduler_policy(config), "constant")

    def test_constant_policy_is_not_reported_as_accidental_caveat(self) -> None:
        config = {
            "optimizer": {"learning_rate": 0.0003},
            "scheduler": {"enabled": False, "policy": "constant"},
        }

        metadata = build_scheduler_metadata(config)

        self.assertTrue(metadata["scheduler_config_present"])
        self.assertEqual(metadata["scheduler_policy"], "constant")
        self.assertFalse(metadata["scheduler_applied"])
        self.assertFalse(metadata["scheduler_config_present_but_not_applied"])
        self.assertEqual(metadata["learning_rate_mode"], "constant")
        self.assertEqual(metadata["base_learning_rate"], 0.0003)
        self.assertEqual(metadata["final_learning_rate"], 0.0003)

    def test_unsupported_scheduler_policy_raises_clear_error(self) -> None:
        config = {"scheduler": {"enabled": True, "policy": "warmup_cosine"}}

        with self.assertRaises(NotImplementedError):
            get_scheduler_policy(config)


if __name__ == "__main__":
    unittest.main()
