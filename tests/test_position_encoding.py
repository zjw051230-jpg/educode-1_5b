from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
SCRIPTS_ROOT = PROJECT_ROOT / "scripts"
for path in (SRC_ROOT, SCRIPTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from educode.config_loader import load_json_config  # noqa: E402
from educode.config_validator import validate_config  # noqa: E402
from educode.position_encoding import get_position_encoding_type, validate_position_encoding_config  # noqa: E402
from generate_passkey_fixture import make_passkey_example  # noqa: E402

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


class PositionEncodingTests(unittest.TestCase):
    def test_learned_default_config_remains_valid(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)

        self.assertEqual(get_position_encoding_type(config["model"]), "learned_position_embedding")
        self.assertEqual(validate_config(config, repo_root=PROJECT_ROOT), [])

    def test_rope_schema_valid_and_bad_scaling_rejected(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)
        rope_config = copy.deepcopy(config)
        rope_config["model"]["position_encoding"] = {"type": "rope", "rope_theta": 10000, "scaling_factor": 1.0}
        self.assertEqual(validate_config(rope_config, repo_root=PROJECT_ROOT), [])

        bad_config = copy.deepcopy(config)
        bad_config["model"]["position_encoding"] = {"type": "rope", "scaling_factor": -1}
        self.assertTrue(any("scaling_factor" in error for error in validate_config(bad_config, repo_root=PROJECT_ROOT)))

    def test_scaling_algorithm_placeholders_rejected(self) -> None:
        errors = validate_position_encoding_config(
            {"position_encoding": {"type": "rope", "scaling_type": "yarn", "scaling_factor": 1.0}}
        )

        self.assertTrue(any("placeholder" in error for error in errors))

    def test_passkey_fixture_generation(self) -> None:
        fixture = make_passkey_example(prefix_tokens=4, suffix_tokens=4, seed=123)

        self.assertIn(fixture["answer"], fixture["prompt"])
        self.assertEqual(fixture["task"], "passkey_retrieval_synthetic_fixture")


if __name__ == "__main__":
    unittest.main()
