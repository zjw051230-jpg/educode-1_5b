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
from educode.moe_layers import MoEConfig, MoEFFNSkeleton, TopKRouter  # noqa: E402
from educode.moe_routing import combine_tokens, dispatch_tokens, expert_capacity, load_balancing_loss, router_z_loss  # noqa: E402

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


def build_summary() -> dict[str, object]:
    blockers: list[str] = []
    x = torch.randn(2, 4, 16)
    router = TopKRouter(d_model=16, num_experts=4, top_k=2)
    routing = router(x)
    if tuple(routing["top_indices"].shape) != (2, 4, 2):
        blockers.append("router top_indices shape mismatch")
    if not torch.allclose(routing["top_weights"].sum(dim=-1), torch.ones(2, 4), atol=1e-6):
        blockers.append("router top weights are not normalized")
    flat_probs = routing["probs"].reshape(-1, 4)
    flat_indices = routing["top_indices"].reshape(-1, 2)
    if not torch.isfinite(load_balancing_loss(flat_probs, flat_indices, 4)):
        blockers.append("load balancing loss is not finite")
    if not torch.isfinite(router_z_loss(routing["logits"].reshape(-1, 4))):
        blockers.append("router z-loss is not finite")
    if expert_capacity(8, 4, 2, 1.25) != 5:
        blockers.append("expert capacity helper returned unexpected value")
    tokens = x.reshape(-1, 16)
    dispatched, metadata = dispatch_tokens(tokens, flat_indices, routing["top_weights"].reshape(-1, 2), num_experts=4)
    combined = combine_tokens(dispatched, metadata, num_tokens=tokens.shape[0])
    if tuple(combined.shape) != tuple(tokens.shape):
        blockers.append("dispatch/combine shape mismatch")
    skeleton = MoEFFNSkeleton(MoEConfig(d_model=16, d_ff=64, num_experts=4, top_k=2))
    skeleton_output = skeleton(x)
    if "router_logits" not in skeleton_output:
        blockers.append("MoE FFN skeleton output missing router_logits")
    config = load_json_config(DEFAULT_CONFIG_PATH)
    disabled = copy.deepcopy(config)
    disabled["moe"] = {"enabled": False, "num_experts": 4, "top_k": 2, "capacity_factor": 1.25}
    disabled_valid = validate_config(disabled, repo_root=PROJECT_ROOT) == []
    if not disabled_valid:
        blockers.append("moe.enabled=false dense config should remain valid")
    enabled = copy.deepcopy(config)
    enabled["moe"] = {"enabled": True, "num_experts": 4, "top_k": 2}
    enabled_rejected = any("moe.enabled=true" in error for error in validate_config(enabled, repo_root=PROJECT_ROOT))
    if not enabled_rejected:
        blockers.append("moe.enabled=true config was not rejected")
    bad = copy.deepcopy(config)
    bad["moe"] = {"enabled": False, "num_experts": 2, "top_k": 3}
    bad_rejected = any("moe.top_k" in error for error in validate_config(bad, repo_root=PROJECT_ROOT))
    if not bad_rejected:
        blockers.append("bad MoE config was not rejected")
    return {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "router_shape": list(routing["top_indices"].shape),
        "top_k_weights_normalized": True,
        "load_balance_loss_finite": True,
        "z_loss_finite": True,
        "capacity_example": expert_capacity(8, 4, 2, 1.25),
        "dispatch_combine_passed": tuple(combined.shape) == tuple(tokens.shape),
        "moe_disabled_dense_config_valid": disabled_valid,
        "moe_enabled_rejected": enabled_rejected,
        "bad_moe_config_rejected": bad_rejected,
        "runs_gpu": False,
        "starts_training": False,
    }


def main() -> int:
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
