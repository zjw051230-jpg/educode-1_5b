from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
SCRIPTS_ROOT = PROJECT_ROOT / "scripts"
for path in (SRC_ROOT, SCRIPTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from educode.config_loader import load_json_config  # noqa: E402
from educode.config_validator import validate_config  # noqa: E402
from educode.rope import apply_rotary_emb, build_rope_cache  # noqa: E402
from generate_passkey_fixture import make_passkey_example  # noqa: E402

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


def build_summary() -> dict[str, object]:
    blockers: list[str] = []
    q = torch.randn(2, 4, 8, 16)
    k = torch.randn(2, 4, 8, 16)
    cache = build_rope_cache(seq_len=8, head_dim=16)
    q_rot, k_rot = apply_rotary_emb(q, k, cache)
    if tuple(q_rot.shape) != tuple(q.shape) or tuple(k_rot.shape) != tuple(k.shape):
        blockers.append("apply_rotary_emb shape mismatch")
    bad_head_dim_rejected = False
    try:
        build_rope_cache(seq_len=8, head_dim=15)
    except ValueError:
        bad_head_dim_rejected = True
    if not bad_head_dim_rejected:
        blockers.append("odd head_dim was not rejected")
    bad_scaling_rejected = False
    try:
        build_rope_cache(seq_len=8, head_dim=16, scaling_factor=0)
    except ValueError:
        bad_scaling_rejected = True
    if not bad_scaling_rejected:
        blockers.append("bad scaling factor was not rejected")
    config = load_json_config(DEFAULT_CONFIG_PATH)
    if validate_config(config, repo_root=PROJECT_ROOT):
        blockers.append("learned default config should remain valid")
    rope_config = copy.deepcopy(config)
    rope_config["model"]["position_encoding"] = {"type": "rope", "rope_theta": 10000, "scaling_factor": 1.0}
    if validate_config(rope_config, repo_root=PROJECT_ROOT):
        blockers.append("explicit RoPE config should be schema-valid")
    bad_config = copy.deepcopy(config)
    bad_config["model"]["position_encoding"] = {"type": "rope", "scaling_factor": -1}
    bad_config_rejected = any("scaling_factor" in error for error in validate_config(bad_config, repo_root=PROJECT_ROOT))
    if not bad_config_rejected:
        blockers.append("bad RoPE scaling config was not rejected")
    fixture = make_passkey_example(prefix_tokens=4, suffix_tokens=4, seed=1)
    if "answer" not in fixture or fixture["answer"] not in fixture["prompt"]:
        blockers.append("passkey fixture did not include answer in prompt")
    return {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "learned_default_path_unchanged": True,
        "rope_cache_shape": [list(cache.cos.shape), list(cache.sin.shape)],
        "rotary_q_shape": list(q_rot.shape),
        "rotary_k_shape": list(k_rot.shape),
        "bad_head_dim_rejected": bad_head_dim_rejected,
        "bad_scaling_rejected": bad_scaling_rejected,
        "passkey_fixture_generated": True,
        "runs_gpu": False,
        "starts_training": False,
    }


def main() -> int:
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
