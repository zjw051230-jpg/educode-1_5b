from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = PROJECT_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from check_flashattention_feasibility import (  # noqa: E402
    build_summary,
    default_future_config,
    flash_attn_installed,
    validate_future_flashattention_config,
)


class FlashAttentionFeasibilityTests(unittest.TestCase):
    def test_missing_flash_attn_is_not_a_checker_failure(self) -> None:
        summary = build_summary()

        self.assertEqual(summary["feasibility_status"], "passed")
        self.assertEqual(summary["blocker_count"], 0)
        self.assertIsInstance(summary["flash_attn_installed"], bool)

    def test_default_future_config_is_disabled_and_valid(self) -> None:
        config = default_future_config()
        blockers = validate_future_flashattention_config(config, flash_available=flash_attn_installed())

        self.assertEqual(blockers, [])
        self.assertFalse(config["flash_attention"]["enabled"])
        self.assertEqual(config["profiling"]["attention_backend"], "flash_attention_2")

    def test_bad_backend_config_is_rejected(self) -> None:
        blockers = validate_future_flashattention_config(
            {
                "profiling": {"attention_backend": "bad_backend"},
                "flash_attention": {"enabled": False, "dtype": "bfloat16"},
            },
            flash_available=False,
        )

        self.assertIn("profiling.attention_backend must be sdpa or flash_attention_2", blockers)

    def test_enabled_flashattention_requires_backend_and_package(self) -> None:
        blockers = validate_future_flashattention_config(
            {
                "profiling": {"attention_backend": "sdpa"},
                "flash_attention": {"enabled": True, "dtype": "bfloat16"},
            },
            flash_available=False,
        )

        self.assertIn("flash_attention.enabled requires profiling.attention_backend=flash_attention_2", blockers)
        self.assertIn("flash_attention.enabled requires flash_attn to be installed", blockers)

    def test_bad_dtype_is_rejected(self) -> None:
        blockers = validate_future_flashattention_config(
            {
                "profiling": {"attention_backend": "flash_attention_2"},
                "flash_attention": {"enabled": False, "dtype": "float32"},
            },
            flash_available=True,
        )

        self.assertIn("flash_attention.dtype must be float16 or bfloat16", blockers)


if __name__ == "__main__":
    unittest.main()
