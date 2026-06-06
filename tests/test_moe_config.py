from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.config_loader import load_json_config  # noqa: E402
from educode.config_validator import validate_config  # noqa: E402

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


class MoEConfigTests(unittest.TestCase):
    def test_moe_disabled_keeps_dense_config_valid(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)
        config["moe"] = {"enabled": False, "num_experts": 4, "top_k": 2, "capacity_factor": 1.25}

        self.assertEqual(validate_config(config, repo_root=PROJECT_ROOT), [])

    def test_moe_enabled_rejected(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)
        config["moe"] = {"enabled": True, "num_experts": 4, "top_k": 2}
        errors = validate_config(config, repo_root=PROJECT_ROOT)

        self.assertTrue(any("moe.enabled=true" in error for error in errors))

    def test_bad_moe_config_rejected(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)
        bad = copy.deepcopy(config)
        bad["moe"] = {"enabled": False, "num_experts": 2, "top_k": 3}
        errors = validate_config(bad, repo_root=PROJECT_ROOT)

        self.assertTrue(any("moe.top_k" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
