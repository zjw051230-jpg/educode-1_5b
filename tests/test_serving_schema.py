from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.serving import FakeModelBackend, build_app, health_response, model_metadata_response  # noqa: E402
from educode.serving_schema import GenerateRequest, validate_generate_request  # noqa: E402


class ServingSchemaTests(unittest.TestCase):
    def test_schema_validation_accepts_valid_generate_request(self) -> None:
        request = GenerateRequest(prompt="def add(a, b):", max_new_tokens=8, temperature=0.7)

        self.assertEqual(validate_generate_request(request).prompt, "def add(a, b):")

    def test_schema_validation_rejects_empty_prompt(self) -> None:
        with self.assertRaises(ValueError):
            GenerateRequest(prompt="", max_new_tokens=8)

    def test_fake_generate_response_is_deterministic(self) -> None:
        backend = FakeModelBackend(model_name="educode-fake")
        request = GenerateRequest(prompt="hello", max_new_tokens=4)

        first = backend.generate(request)
        second = backend.generate(request)

        self.assertEqual(first.text, second.text)
        self.assertEqual(first.model_name, "educode-fake")
        self.assertFalse(first.checkpoint_loaded)

    def test_health_and_metadata_are_local_only(self) -> None:
        self.assertEqual(health_response()["status"], "ok")
        metadata = model_metadata_response(FakeModelBackend(model_name="educode-fake"))
        self.assertFalse(metadata["checkpoint_loaded"])

    def test_fastapi_app_builder_is_graceful(self) -> None:
        app_info = build_app(FakeModelBackend(model_name="educode-fake"))

        self.assertIn("fastapi_available", app_info)
        self.assertIn("app", app_info)


if __name__ == "__main__":
    unittest.main()
