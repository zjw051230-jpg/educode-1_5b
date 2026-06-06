from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.config_loader import load_json_config  # noqa: E402
from educode.config_validator import validate_config  # noqa: E402
from educode.position_encoding import apply_rope, build_rope_cache, normalize_position_encoding  # noqa: E402

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


class PositionEncodingTests(unittest.TestCase):
    def test_rope_cache_and_apply_preserve_shape_and_dtype(self) -> None:
        cache = build_rope_cache(seq_len=8, head_dim=16, dtype=torch.float32)
        x = torch.randn(2, 4, 8, 16)
        y = apply_rope(x, cache)

        self.assertEqual(tuple(y.shape), tuple(x.shape))
        self.assertEqual(y.dtype, x.dtype)

    def test_rope_rejects_odd_head_dim(self) -> None:
        with self.assertRaises(ValueError):
            build_rope_cache(seq_len=8, head_dim=15)

    def test_position_encoding_normalization_and_bad_value(self) -> None:
        self.assertEqual(normalize_position_encoding("learned"), "learned")
        self.assertEqual(normalize_position_encoding("rope"), "rope")
        with self.assertRaises(ValueError):
            normalize_position_encoding("bad_position_backend")

    def test_current_default_config_remains_valid(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)

        self.assertEqual(validate_config(config, repo_root=PROJECT_ROOT), [])

    def test_rope_config_schema_and_bad_config_rejection(self) -> None:
        config = load_json_config(DEFAULT_CONFIG_PATH)
        rope_config = copy.deepcopy(config)
        rope_config["model"]["position_encoding"] = "rope"
        rope_config["model"]["rope_theta"] = 10000

        self.assertEqual(validate_config(rope_config, repo_root=PROJECT_ROOT), [])

        bad_config = copy.deepcopy(config)
        bad_config["model"]["position_encoding"] = "bad_position_backend"
        errors = validate_config(bad_config, repo_root=PROJECT_ROOT)
        self.assertTrue(any("model.position_encoding" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
