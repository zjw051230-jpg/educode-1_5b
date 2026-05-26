from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_PATH = PROJECT_ROOT / "scripts"
for path in (PROJECT_ROOT, SCRIPTS_PATH):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from check_a100_execution_readiness import build_sampling_metadata as build_readiness_sampling_metadata
from run_a100_300m_fineweb_edu_10step_training import build_sampling_metadata, build_split_sampling_settings


class SamplingPolicyConfigTests(unittest.TestCase):
    def test_missing_sampling_config_defaults_to_sequential_prefix(self) -> None:
        metadata = build_sampling_metadata({"run": {"seed": 336}})

        self.assertEqual(metadata["sampling_policy"], "sequential_prefix")
        self.assertIsNone(metadata["shuffle_seed"])
        self.assertEqual(metadata["shuffle_buffer_size"], 1)
        self.assertTrue(metadata["bounded_prefix_batches_only"])

    def test_shuffle_buffer_sampling_metadata_uses_explicit_seed_and_size(self) -> None:
        metadata = build_sampling_metadata(
            {
                "run": {"seed": 336},
                "sampling": {
                    "policy": "shuffle_buffer",
                    "shuffle_seed": 1337,
                    "shuffle_buffer_size": 1024,
                },
            }
        )

        self.assertEqual(metadata["sampling_policy"], "shuffle_buffer")
        self.assertEqual(metadata["shuffle_seed"], 1337)
        self.assertEqual(metadata["shuffle_buffer_size"], 1024)
        self.assertFalse(metadata["bounded_prefix_batches_only"])

    def test_shuffle_buffer_sampling_can_fallback_to_run_seed(self) -> None:
        metadata = build_sampling_metadata(
            {
                "run": {"seed": 336},
                "sampling": {
                    "policy": "shuffle_buffer",
                    "shuffle_buffer_size": 1024,
                },
            }
        )

        self.assertEqual(metadata["shuffle_seed"], 336)
        self.assertFalse(metadata["bounded_prefix_batches_only"])

    def test_shuffle_buffer_requires_buffer_larger_than_one(self) -> None:
        with self.assertRaisesRegex(ValueError, "shuffle_buffer_size must be greater than 1"):
            build_sampling_metadata(
                {
                    "run": {"seed": 336},
                    "sampling": {
                        "policy": "shuffle_buffer",
                        "shuffle_seed": 1337,
                        "shuffle_buffer_size": 1,
                    },
                }
            )

    def test_unsupported_sampling_policy_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported sampling policy"):
            build_sampling_metadata({"sampling": {"policy": "full_shuffle"}})

    def test_training_uses_shuffle_for_train_and_prefix_for_validation(self) -> None:
        config = {
            "run": {"seed": 336},
            "sampling": {
                "policy": "shuffle_buffer",
                "shuffle_seed": 1337,
                "shuffle_buffer_size": 1024,
            },
        }

        train_settings = build_split_sampling_settings(config, split_name="train")
        val_settings = build_split_sampling_settings(config, split_name="val")

        self.assertEqual(train_settings["sampling_policy"], "shuffle_buffer")
        self.assertEqual(train_settings["shuffle_seed"], 1337)
        self.assertEqual(train_settings["shuffle_buffer_size"], 1024)
        self.assertEqual(val_settings["sampling_policy"], "sequential_prefix")
        self.assertIsNone(val_settings["shuffle_seed"])
        self.assertEqual(val_settings["shuffle_buffer_size"], 1)

    def test_readiness_sampling_metadata_matches_training_parser(self) -> None:
        config = {
            "run": {"seed": 336},
            "sampling": {
                "policy": "shuffle_buffer",
                "shuffle_seed": 1337,
                "shuffle_buffer_size": 1024,
            },
        }

        self.assertEqual(build_readiness_sampling_metadata(config), build_sampling_metadata(config))


if __name__ == "__main__":
    unittest.main()
