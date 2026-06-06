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
from educode.moe_layers import MoEConfig, SparseMoESkeleton, TopKRouter  # noqa: E402

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


def build_summary() -> dict[str, object]:
    blockers: list[str] = []
    torch.manual_seed(11)
    x = torch.randn(2, 5, 16)
    router = TopKRouter(d_model=16, num_experts=4, top_k=2)
    top_indices, top_weights = router(x)

    if tuple(top_indices.shape) != (2, 5, 2):
        blockers.append(f"unexpected top_indices shape: {tuple(top_indices.shape)}")
    if tuple(top_weights.shape) != (2, 5, 2):
        blockers.append(f"unexpected top_weights shape: {tuple(top_weights.shape)}")
    if not torch.allclose(top_weights.sum(dim=-1), torch.ones(2, 5), atol=1e-6):
        blockers.append("top-k router weights are not normalized")

    skeleton = SparseMoESkeleton(MoEConfig(d_model=16, d_ff=64, num_experts=4, top_k=2))
    skeleton_output = skeleton(x)
    if set(skeleton_output) != {"top_indices", "top_weights"}:
        blockers.append("MoE skeleton output keys are unexpected")

    dense_config = load_json_config(DEFAULT_CONFIG_PATH)
    disabled_config = copy.deepcopy(dense_config)
    disabled_config["moe"] = {"enabled": False, "num_experts": 4, "top_k": 2}
    disabled_errors = validate_config(disabled_config, repo_root=PROJECT_ROOT)
    if disabled_errors:
        blockers.append(f"moe.enabled=false dense config should remain valid: {disabled_errors}")

    enabled_config = copy.deepcopy(dense_config)
    enabled_config["moe"] = {"enabled": True, "num_experts": 4, "top_k": 2}
    enabled_errors = validate_config(enabled_config, repo_root=PROJECT_ROOT)
    bad_config_rejected = any("moe.enabled=true" in error for error in enabled_errors)
    if not bad_config_rejected:
        blockers.append("moe.enabled=true config was not rejected")

    invalid_shape_rejected = False
    try:
        TopKRouter(d_model=16, num_experts=2, top_k=3)
    except ValueError:
        invalid_shape_rejected = True
    if not invalid_shape_rejected:
        blockers.append("invalid top_k > num_experts router config was not rejected")

    return {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "router_output_shape": list(top_indices.shape),
        "router_weights_shape": list(top_weights.shape),
        "router_weights_normalized": bool(torch.allclose(top_weights.sum(dim=-1), torch.ones(2, 5), atol=1e-6)),
        "moe_disabled_dense_config_valid": not disabled_errors,
        "moe_enabled_config_rejected": bad_config_rejected,
        "bad_router_config_rejected": invalid_shape_rejected,
        "moe_default_enabled": False,
        "runs_gpu": False,
        "starts_training": False,
    }


def main() -> int:
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
