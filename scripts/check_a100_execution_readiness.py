from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_50mb_300m_10step_execute.json"
EXPECTED_PARAMETER_COUNT = 319329280
EXPECTED_MAX_STEPS = 10
EXPECTED_CHECKPOINT_INTERVAL = 10
TRAINING_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "run_a100_300m_fineweb_edu_10step_training.py"
DRY_RUN_SUMMARY_PATH = PROJECT_ROOT / "experiments" / "a100" / "fineweb_edu_50mb_300m_10step_smoke" / "dry_run_summary.json"
LOCAL_ARTIFACT_ROOT = PROJECT_ROOT / "data" / "public_corpus" / "fineweb_edu_sample10bt_50mb"
LOCAL_SPLITS_DIR = LOCAL_ARTIFACT_ROOT / "splits"
LOCAL_PROCESSED_DIR = LOCAL_ARTIFACT_ROOT / "processed"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_repo_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def repo_relative_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check A100 execution readiness for the FineWeb-Edu 300M 10-step smoke.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the A100 execution config JSON.")
    return parser.parse_args()


def require(condition: bool, message: str, blockers: list[str]) -> None:
    if not condition:
        blockers.append(message)


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    config = load_json(config_path)
    blockers: list[str] = []
    caveats: list[str] = []

    run_name = config["run"]["run_name"]
    output_dir = resolve_repo_path(config["run"]["output_dir"])
    train_path = resolve_repo_path(config["data"]["train_path"])
    val_path = resolve_repo_path(config["data"]["val_path"])
    tokenizer_path = resolve_repo_path(config["tokenizer"]["path"])
    tokenizer_vocab_size = int(config["tokenizer"]["vocab_size"])
    model_size_label = config["model"]["model_size_label"]
    sequence_length = int(config["training"]["sequence_length"])
    batch_size = int(config["training"]["batch_size"])
    gradient_accumulation_steps = int(config["training"]["gradient_accumulation_steps"])
    max_steps = int(config["training"]["max_steps"])
    eval_interval = int(config["training"]["eval_interval"])
    checkpoint_interval = int(config["training"]["checkpoint_interval"])
    precision = str(config["hardware"].get("precision"))
    training_no_training = config.get("training", {}).get("no_training")
    top_level_no_training = config.get("no_training")
    no_commit_checkpoints = config.get("checkpoint", {}).get("no_commit_checkpoints")

    require(training_no_training is False, "training.no_training must be false for execution config", blockers)
    require(max_steps == EXPECTED_MAX_STEPS, f"training.max_steps must equal {EXPECTED_MAX_STEPS}", blockers)
    require(
        checkpoint_interval == EXPECTED_CHECKPOINT_INTERVAL,
        f"training.checkpoint_interval must equal {EXPECTED_CHECKPOINT_INTERVAL}",
        blockers,
    )
    require(no_commit_checkpoints is True, "checkpoint.no_commit_checkpoints must be true", blockers)
    require(train_path.exists(), f"missing train_path: {train_path}", blockers)
    require(val_path.exists(), f"missing val_path: {val_path}", blockers)
    require(tokenizer_path.exists(), f"missing tokenizer_path: {tokenizer_path}", blockers)
    require(TRAINING_SCRIPT_PATH.exists(), f"missing training script: {TRAINING_SCRIPT_PATH}", blockers)
    require(DRY_RUN_SUMMARY_PATH.exists(), f"missing dry-run summary: {DRY_RUN_SUMMARY_PATH}", blockers)
    require(is_under(output_dir, PROJECT_ROOT / "experiments" / "a100"), "output_dir must stay under experiments/a100/", blockers)
    require(is_under(train_path, LOCAL_SPLITS_DIR), "train_path must stay under local splits artifact directory", blockers)
    require(is_under(val_path, LOCAL_SPLITS_DIR), "val_path must stay under local splits artifact directory", blockers)

    dry_run_summary: dict[str, Any] | None = None
    if DRY_RUN_SUMMARY_PATH.exists():
        dry_run_summary = load_json(DRY_RUN_SUMMARY_PATH)
        require(
            dry_run_summary.get("exact_parameter_count") == EXPECTED_PARAMETER_COUNT,
            f"dry-run exact_parameter_count must equal {EXPECTED_PARAMETER_COUNT}",
            blockers,
        )
        require(
            dry_run_summary.get("model_materialized_locally") is True,
            "dry-run model_materialized_locally must be true",
            blockers,
        )
        require(
            dry_run_summary.get("memory_limited_local_dry_run") is False,
            "dry-run memory_limited_local_dry_run must be false",
            blockers,
        )
        if dry_run_summary.get("core_model_feature_parity") is False:
            caveats.append(
                "core_model_feature_parity=false in dry-run summary; this is a training-systems smoke caveat, not a blocker."
            )

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "execution_readiness_summary.json"
    summary = {
        "status": "success" if not blockers else "failed",
        "config_path": repo_relative_path(config_path),
        "run_name": run_name,
        "train_path": repo_relative_path(train_path),
        "val_path": repo_relative_path(val_path),
        "tokenizer_path": repo_relative_path(tokenizer_path),
        "tokenizer_vocab_size": tokenizer_vocab_size,
        "model_size_label": model_size_label,
        "sequence_length": sequence_length,
        "batch_size": batch_size,
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "max_steps": max_steps,
        "eval_interval": eval_interval,
        "checkpoint_interval": checkpoint_interval,
        "precision": precision,
        "output_dir": repo_relative_path(output_dir),
        "training_script_path": repo_relative_path(TRAINING_SCRIPT_PATH),
        "dry_run_summary_path": repo_relative_path(DRY_RUN_SUMMARY_PATH),
        "training_no_training": training_no_training,
        "top_level_no_training": top_level_no_training,
        "no_commit_checkpoints": no_commit_checkpoints,
        "local_artifact_root": repo_relative_path(LOCAL_ARTIFACT_ROOT),
        "local_processed_dir": repo_relative_path(LOCAL_PROCESSED_DIR),
        "local_processed_dir_exists": LOCAL_PROCESSED_DIR.exists(),
        "local_processed_dir_is_local_artifact": is_under(LOCAL_PROCESSED_DIR, LOCAL_ARTIFACT_ROOT),
        "local_splits_dir": repo_relative_path(LOCAL_SPLITS_DIR),
        "local_splits_dir_exists": LOCAL_SPLITS_DIR.exists(),
        "local_splits_dir_is_local_artifact": is_under(LOCAL_SPLITS_DIR, LOCAL_ARTIFACT_ROOT),
        "train_path_is_local_artifact": is_under(train_path, LOCAL_ARTIFACT_ROOT),
        "val_path_is_local_artifact": is_under(val_path, LOCAL_ARTIFACT_ROOT),
        "dry_run_exact_parameter_count": dry_run_summary.get("exact_parameter_count") if dry_run_summary else None,
        "dry_run_model_materialized_locally": dry_run_summary.get("model_materialized_locally") if dry_run_summary else None,
        "dry_run_memory_limited_local_dry_run": dry_run_summary.get("memory_limited_local_dry_run") if dry_run_summary else None,
        "dry_run_core_model_feature_parity": dry_run_summary.get("core_model_feature_parity") if dry_run_summary else None,
        "blockers": blockers,
        "caveats": caveats,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "ready_for_a100_execution": not blockers,
        "no_training_ran_in_this_step": True,
        "no_a100_session_entered_in_this_step": True
    }
    write_json(summary_path, summary)

    print(f"status={summary['status']}")
    print(f"config_path={summary['config_path']}")
    print(f"run_name={summary['run_name']}")
    print(f"output_dir={summary['output_dir']}")
    print(f"training_no_training={summary['training_no_training']}")
    print(f"max_steps={summary['max_steps']}")
    print(f"checkpoint_interval={summary['checkpoint_interval']}")
    print(f"no_commit_checkpoints={summary['no_commit_checkpoints']}")
    print(f"ready_for_a100_execution={summary['ready_for_a100_execution']}")
    print(f"caveats={len(caveats)}")
    print(f"blockers={len(blockers)}")
    print(f"summary_path={repo_relative_path(summary_path)}")
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
