from __future__ import annotations

import copy
import json
import sys
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


def build_summary() -> dict[str, object]:
    blockers: list[str] = []
    cache = build_rope_cache(seq_len=8, head_dim=16, dtype=torch.float32)
    x = torch.randn(2, 4, 8, 16)
    y = apply_rope(x, cache)

    if tuple(y.shape) != tuple(x.shape):
        blockers.append(f"RoPE output shape mismatch: {tuple(y.shape)} != {tuple(x.shape)}")
    if y.dtype != x.dtype:
        blockers.append(f"RoPE output dtype mismatch: {y.dtype} != {x.dtype}")

    config = load_json_config(DEFAULT_CONFIG_PATH)
    config_errors = validate_config(config, repo_root=PROJECT_ROOT)
    if config_errors:
        blockers.append(f"default learned-position config validation failed: {config_errors}")

    rope_config = copy.deepcopy(config)
    rope_config["model"]["position_encoding"] = "rope"
    rope_config["model"]["rope_theta"] = 10000
    rope_errors = validate_config(rope_config, repo_root=PROJECT_ROOT)
    if rope_errors:
        blockers.append(f"rope declaration should be schema-valid for prepared path: {rope_errors}")

    bad_config = copy.deepcopy(config)
    bad_config["model"]["position_encoding"] = "bad_position_backend"
    bad_errors = validate_config(bad_config, repo_root=PROJECT_ROOT)
    bad_config_rejected = any("model.position_encoding" in error for error in bad_errors)
    if not bad_config_rejected:
        blockers.append("bad position_encoding config was not rejected")

    bad_rope_shape_rejected = False
    try:
        build_rope_cache(seq_len=8, head_dim=15)
    except ValueError:
        bad_rope_shape_rejected = True
    if not bad_rope_shape_rejected:
        blockers.append("odd head_dim RoPE cache was not rejected")

    return {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "default_position_encoding": config["model"].get("position_encoding"),
        "rope_helper_output_shape": list(y.shape),
        "rope_helper_dtype": str(y.dtype),
        "rope_config_schema_valid": not rope_errors,
        "bad_position_config_rejected": bad_config_rejected,
        "bad_rope_shape_rejected": bad_rope_shape_rejected,
        "wired_into_training_path": False,
        "runs_gpu": False,
        "starts_training": False,
    }


def main() -> int:
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
