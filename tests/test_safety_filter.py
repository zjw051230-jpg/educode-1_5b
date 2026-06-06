from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.safety_filter import (  # noqa: E402
    SafetyFilter,
    SafetyPattern,
    build_filter_report,
    validate_patterns,
)


class SafetyFilterTests(unittest.TestCase):
    def test_synthetic_unsafe_pattern_is_detected(self) -> None:
        safety_filter = SafetyFilter([SafetyPattern(name="secret", pattern=r"api[_-]?key", severity="high")])

        result = safety_filter.check_text("Never paste an api_key into logs.")

        self.assertFalse(result.safe)
        self.assertEqual(result.matches[0].pattern_name, "secret")

    def test_safe_text_passes(self) -> None:
        safety_filter = SafetyFilter([SafetyPattern(name="secret", pattern=r"api[_-]?key", severity="high")])

        result = safety_filter.check_text("This is a normal tokenizer note.")

        self.assertTrue(result.safe)
        self.assertEqual(result.matches, [])

    def test_bad_pattern_config_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            SafetyPattern(name="", pattern="x", severity="low")
        with self.assertRaises(ValueError):
            SafetyPattern(name="bad", pattern="[", severity="low")

    def test_filter_report_counts_safe_and_unsafe_items(self) -> None:
        safety_filter = SafetyFilter([SafetyPattern(name="secret", pattern=r"api[_-]?key", severity="high")])

        report = build_filter_report(safety_filter, ["safe sample", "contains api-key"])

        self.assertEqual(report["text_count"], 2)
        self.assertEqual(report["unsafe_count"], 1)
        self.assertEqual(report["safe_count"], 1)

    def test_validate_patterns_rejects_empty_list(self) -> None:
        with self.assertRaises(ValueError):
            validate_patterns([])


if __name__ == "__main__":
    unittest.main()
