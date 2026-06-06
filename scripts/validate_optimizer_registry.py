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
from educode.optimizers import (  # noqa: E402
    DEFAULT_OPTIMIZER,
    ExperimentalOptimizerUnavailable,
    create_optimizer,
    normalize_optimizer_name,
)

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


def adamw_synthetic_step_changes_parameter() -> bool:
    parameter = torch.nn.Parameter(torch.tensor([1.0]))
    optimizer = create_optimizer([parameter], {"name": "adamw", "learning_rate": 0.1, "weight_decay": 0.0})
    loss = parameter.pow(2).sum()
    loss.backward()
    before = float(parameter.detach().item())
    optimizer.step()
    after = float(parameter.detach().item())
    return after != before


def build_summary() -> dict[str, object]:
    blockers: list[str] = []
    config = load_json_config(DEFAULT_CONFIG_PATH)
    config_errors = validate_config(config, repo_root=PROJECT_ROOT)
    if config_errors:
        blockers.append(f"default config validation failed: {config_errors}")

    default_optimizer_name = str(config.get("optimizer", {}).get("name", DEFAULT_OPTIMIZER)).strip().lower()
    if default_optimizer_name != "adamw":
        blockers.append(f"default config optimizer expected adamw, got {default_optimizer_name!r}")

    adamw_step_changed = adamw_synthetic_step_changes_parameter()
    if not adamw_step_changed:
        blockers.append("AdamW synthetic step did not change parameter")

    bad_optimizer_rejected = False
    try:
        normalize_optimizer_name("not_an_optimizer")
    except ValueError:
        bad_optimizer_rejected = True
    if not bad_optimizer_rejected:
        blockers.append("bad optimizer name was not rejected")

    bad_config = copy.deepcopy(config)
    bad_config["optimizer"]["name"] = "not_an_optimizer"
    bad_config_errors = validate_config(bad_config, repo_root=PROJECT_ROOT)
    if not any("optimizer.name" in error for error in bad_config_errors):
        blockers.append("config validator did not reject bad optimizer.name")

    muon_guarded = False
    try:
        create_optimizer([torch.nn.Parameter(torch.tensor([1.0]))], {"name": "muon_experimental"})
    except ExperimentalOptimizerUnavailable:
        muon_guarded = True
    if not muon_guarded:
        blockers.append("muon_experimental was not guarded")

    return {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "default_optimizer": default_optimizer_name,
        "adamw_registry_created": True,
        "adamw_synthetic_step_changed_parameter": adamw_step_changed,
        "bad_optimizer_rejected": bad_optimizer_rejected,
        "config_validator_rejects_bad_optimizer": any("optimizer.name" in error for error in bad_config_errors),
        "muon_experimental_guarded": muon_guarded,
        "runs_gpu": False,
        "starts_training": False,
    }


def main() -> int:
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
