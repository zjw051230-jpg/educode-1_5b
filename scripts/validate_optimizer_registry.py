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
from educode.muon import newton_schulz_orthogonalize, split_muon_adamw_parameters  # noqa: E402
from educode.optimizers import create_optimizer, normalize_optimizer_name  # noqa: E402

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


def build_summary() -> dict[str, object]:
    blockers: list[str] = []
    parameter = torch.nn.Parameter(torch.tensor([1.0]))
    adamw = create_optimizer([parameter], {"name": "adamw", "learning_rate": 0.1, "weight_decay": 0.0})
    loss = parameter.pow(2).sum()
    loss.backward()
    before = float(parameter.item())
    adamw.step()
    adamw_step_changed = float(parameter.item()) != before
    if not adamw_step_changed:
        blockers.append("AdamW synthetic step did not change parameter")

    matrix = torch.randn(4, 4)
    ns = newton_schulz_orthogonalize(matrix)
    if not bool(torch.isfinite(ns).all()):
        blockers.append("Newton-Schulz output is not finite")

    muon_ack_required = False
    try:
        create_optimizer([torch.nn.Parameter(torch.randn(4, 4))], {"name": "muon_experimental"})
    except ValueError:
        muon_ack_required = True
    if not muon_ack_required:
        blockers.append("Muon path did not require explicit ack")

    muon_param = torch.nn.Parameter(torch.randn(4, 4))
    muon = create_optimizer(
        [muon_param],
        {"name": "muon_experimental", "experimental_ack_required": True, "learning_rate": 0.01},
    )
    (muon_param.pow(2).sum()).backward()
    muon.step()

    named = [
        ("blocks.0.attention.q_proj.weight", torch.nn.Parameter(torch.randn(4, 4))),
        ("token_embedding.weight", torch.nn.Parameter(torch.randn(8, 4))),
        ("final_norm.weight", torch.nn.Parameter(torch.randn(4))),
        ("lm_head.weight", torch.nn.Parameter(torch.randn(4, 8))),
        ("mlp.bias", torch.nn.Parameter(torch.randn(4))),
    ]
    groups = split_muon_adamw_parameters(named)
    grouping_ok = len(groups.muon) == 1 and len(groups.adamw) == 4
    if not grouping_ok:
        blockers.append("Muon/AdamW parameter grouping failed")

    config = load_json_config(DEFAULT_CONFIG_PATH)
    bad_config = copy.deepcopy(config)
    bad_config["optimizer"]["name"] = "bad_optimizer"
    bad_rejected = any("optimizer.name" in error for error in validate_config(bad_config, repo_root=PROJECT_ROOT))
    if not bad_rejected:
        blockers.append("bad optimizer config was not rejected")

    muon_config = copy.deepcopy(config)
    muon_config["optimizer"]["name"] = "muon_experimental"
    muon_without_ack_rejected = any(
        "muon_experimental" in error for error in validate_config(muon_config, repo_root=PROJECT_ROOT)
    )
    if not muon_without_ack_rejected:
        blockers.append("Muon config without ack was not rejected")

    return {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "default_optimizer": config["optimizer"].get("name"),
        "adamw_registry_created": True,
        "adamw_step_changed_parameter": adamw_step_changed,
        "newton_schulz_finite": bool(torch.isfinite(ns).all()),
        "muon_ack_required": muon_ack_required,
        "muon_step_executed_on_synthetic_2d_parameter": True,
        "parameter_grouping_ok": grouping_ok,
        "bad_optimizer_rejected": bad_rejected,
        "runs_gpu": False,
        "starts_training": False,
    }


def main() -> int:
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
