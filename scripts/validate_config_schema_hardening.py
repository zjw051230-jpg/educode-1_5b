from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.config_loader import load_json_config  # noqa: E402
from educode.config_schema import infer_run_type, validate_hardened_config  # noqa: E402

CONFIGS_TO_KEEP_VALID = [
    "configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json",
    "configs/a100/fineweb_edu_5gb_300m_50step_public16k_sdpa_profile.json",
    "configs/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight.json",
    "configs/a100/fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile.json",
]


def bad_config_cases(base_config: dict[str, object]) -> dict[str, dict[str, object]]:
    cases: dict[str, dict[str, object]] = {}

    long_run = copy.deepcopy(base_config)
    long_run["training"]["max_steps"] = 10000
    long_run["run"]["run_type"] = "training_execution"
    cases["training_10000_step"] = long_run

    bad_backend = copy.deepcopy(base_config)
    bad_backend["profiling"]["attention_backend"] = "unknown_backend"
    cases["unknown_attention_backend"] = bad_backend

    bad_optimizer = copy.deepcopy(base_config)
    bad_optimizer["optimizer"]["name"] = "unknown_optimizer"
    cases["unknown_optimizer"] = bad_optimizer

    muon = copy.deepcopy(base_config)
    muon["optimizer"]["name"] = "muon_experimental"
    cases["muon_without_gate"] = muon

    bad_context = copy.deepcopy(base_config)
    bad_context["model"]["context_length"] = 8192
    cases["oversized_context"] = bad_context

    bad_checkpoint = copy.deepcopy(base_config)
    bad_checkpoint["checkpoint"]["save_dir"] = "../outside_repo/checkpoints"
    cases["checkpoint_escapes_repo"] = bad_checkpoint

    moe_enabled = copy.deepcopy(base_config)
    moe_enabled["moe"] = {"enabled": True}
    cases["moe_enabled"] = moe_enabled

    bad_profile = copy.deepcopy(base_config)
    bad_profile["run"]["run_type"] = "bounded_profile"
    bad_profile["training"]["max_steps"] = 3000
    cases["unbounded_profile"] = bad_profile

    return cases


def build_summary() -> dict[str, object]:
    blockers: list[str] = []
    valid_configs: list[dict[str, object]] = []
    for config_path_text in CONFIGS_TO_KEEP_VALID:
        config_path = PROJECT_ROOT / config_path_text
        config = load_json_config(config_path)
        errors = validate_hardened_config(config, repo_root=PROJECT_ROOT)
        valid_configs.append(
            {
                "config_path": config_path_text,
                "run_type": infer_run_type(config),
                "error_count": len(errors),
            }
        )
        if errors:
            blockers.append(f"{config_path_text} should remain valid: {errors}")

    base_config = load_json_config(PROJECT_ROOT / CONFIGS_TO_KEEP_VALID[0])
    rejected_bad_configs: dict[str, bool] = {}
    for name, bad_config in bad_config_cases(base_config).items():
        rejected_bad_configs[name] = bool(validate_hardened_config(bad_config, repo_root=PROJECT_ROOT))
        if not rejected_bad_configs[name]:
            blockers.append(f"bad config was not rejected: {name}")

    return {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "valid_config_count": len(valid_configs),
        "valid_configs": valid_configs,
        "bad_configs_rejected": rejected_bad_configs,
        "runs_modal": False,
        "runs_gpu": False,
        "starts_training": False,
    }


def main() -> int:
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
