from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.instruction_data import (  # noqa: E402
    InstructionValidationResult,
    chat_to_prompt_completion,
    estimate_token_count,
    load_jsonl_samples,
    validate_instruction_sample,
)


class InstructionDataTests(unittest.TestCase):
    def valid_sample(self) -> dict[str, object]:
        return {
            "id": "sample-001",
            "messages": [
                {"role": "system", "content": "You are a concise coding tutor."},
                {"role": "user", "content": "Explain a Python list comprehension."},
                {"role": "assistant", "content": "It builds a list by applying an expression over an iterable."},
            ],
        }

    def test_valid_chat_sample_is_accepted(self) -> None:
        result = validate_instruction_sample(self.valid_sample(), max_estimated_tokens=64)

        self.assertIsInstance(result, InstructionValidationResult)
        self.assertTrue(result.accepted)
        self.assertEqual(result.issue_count, 0)

    def test_missing_assistant_turn_is_rejected(self) -> None:
        sample = {
            "id": "missing-assistant",
            "messages": [{"role": "user", "content": "What is recursion?"}],
        }

        result = validate_instruction_sample(sample)

        self.assertFalse(result.accepted)
        self.assertIn("at least one assistant turn is required", result.issues)

    def test_overlong_sample_is_flagged(self) -> None:
        sample = self.valid_sample()
        sample["messages"] = [{"role": "user", "content": "token " * 100}, {"role": "assistant", "content": "ok"}]

        result = validate_instruction_sample(sample, max_estimated_tokens=10)

        self.assertFalse(result.accepted)
        self.assertIn("estimated token count exceeds limit", result.issues)

    def test_chat_to_prompt_completion_preserves_roles(self) -> None:
        pair = chat_to_prompt_completion(self.valid_sample())

        self.assertIn("system: You are a concise coding tutor.", pair["prompt"])
        self.assertIn("user: Explain a Python list comprehension.", pair["prompt"])
        self.assertEqual(pair["completion"], "It builds a list by applying an expression over an iterable.")

    def test_jsonl_loader_rejects_bad_samples(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "samples.jsonl"
            path.write_text(
                json.dumps(self.valid_sample()) + "\n"
                + json.dumps({"id": "bad", "messages": [{"role": "user", "content": "hello"}]}) + "\n",
                encoding="utf-8",
            )

            loaded = load_jsonl_samples(path, max_estimated_tokens=64)

            self.assertEqual(loaded["sample_count"], 2)
            self.assertEqual(loaded["accepted_count"], 1)
            self.assertEqual(loaded["rejected_count"], 1)

    def test_token_estimator_is_deterministic(self) -> None:
        text = "alpha beta beta"

        self.assertEqual(estimate_token_count(text), estimate_token_count(text))
        self.assertGreaterEqual(estimate_token_count(text), 3)


if __name__ == "__main__":
    unittest.main()
