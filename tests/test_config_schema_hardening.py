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
from educode.config_schema import infer_run_type, validate_hardened_config  # noqa: E402

BASE_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"
SEQ512_PROFILE_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile.json"
SEQ1024_PREFLIGHT_PATH = (
    PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight.json"
)
SEQ1024_PROFILE_PATH = (
    PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile.json"
)


class ConfigSchemaHardeningTests(unittest.TestCase):
    def test_existing_a100_configs_remain_valid(self) -> None:
        for path in (BASE_CONFIG_PATH, SEQ512_PROFILE_PATH, SEQ1024_PREFLIGHT_PATH, SEQ1024_PROFILE_PATH):
            config = load_json_config(path)
            self.assertEqual(validate_hardened_config(config, repo_root=PROJECT_ROOT), [])

    def test_run_type_inference(self) -> None:
        self.assertEqual(infer_run_type(load_json_config(BASE_CONFIG_PATH)), "training_execution")
        self.assertEqual(infer_run_type(load_json_config(SEQ512_PROFILE_PATH)), "bounded_profile")
        self.assertEqual(infer_run_type(load_json_config(SEQ1024_PREFLIGHT_PATH)), "memory_preflight")

    def test_bad_configs_are_rejected(self) -> None:
        config = load_json_config(BASE_CONFIG_PATH)
        cases = []

        long_run = copy.deepcopy(config)
        long_run["training"]["max_steps"] = 10000
        long_run["run"]["run_type"] = "training_execution"
        cases.append((long_run, "max_steps"))

        bad_backend = copy.deepcopy(config)
        bad_backend["profiling"]["attention_backend"] = "unknown_backend"
        cases.append((bad_backend, "attention_backend"))

        bad_optimizer = copy.deepcopy(config)
        bad_optimizer["optimizer"]["name"] = "unknown_optimizer"
        cases.append((bad_optimizer, "optimizer.name"))

        bad_context = copy.deepcopy(config)
        bad_context["model"]["context_length"] = 8192
        cases.append((bad_context, "context_length"))

        bad_checkpoint = copy.deepcopy(config)
        bad_checkpoint["checkpoint"]["save_dir"] = "../outside_repo/checkpoints"
        cases.append((bad_checkpoint, "checkpoint.save_dir"))

        moe_enabled = copy.deepcopy(config)
        moe_enabled["moe"] = {"enabled": True}
        cases.append((moe_enabled, "moe.enabled"))

        for bad_config, expected_fragment in cases:
            errors = validate_hardened_config(bad_config, repo_root=PROJECT_ROOT)
            self.assertTrue(any(expected_fragment in error for error in errors), errors)

    def test_bounded_profile_rejects_unbounded_step_count(self) -> None:
        config = load_json_config(BASE_CONFIG_PATH)
        config["run"]["run_type"] = "bounded_profile"
        config["training"]["max_steps"] = 3000
        errors = validate_hardened_config(config, repo_root=PROJECT_ROOT)

        self.assertTrue(any("bounded_profile max_steps" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
