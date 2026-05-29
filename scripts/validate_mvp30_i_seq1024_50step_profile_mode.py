from __future__ import annotations

import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPO_ROOT / "scripts" / "modal_a100_streaming_runner.py"
CHECKER_PATH = REPO_ROOT / "scripts" / "check_a100_execution_readiness.py"
ARTIFACT_VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_a800_public16k_run_artifacts.py"
CONFIG_PATH = REPO_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile.json"
MODE_NAME = "profile_5gb_50step_seq1024_sdpa"
EXPECTED_CONFIG_PATH = "configs/a100/fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile.json"
EXPECTED_PACKAGE_PATH = "/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz"
EXPECTED_RESULT_PACKAGE = "/vol/results/mvp30_a100_5gb_50step_seq1024_sdpa_profile_results.tar.gz"
EXPECTED_FLAGS = ("record_tokens_per_sec", "record_memory", "record_mfu")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def resolve_repo_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


def literal_value(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Tuple):
        return tuple(literal_value(element) for element in node.elts)
    if isinstance(node, ast.Name):
        return {"name_ref": node.id}
    raise ValueError(f"unsupported AST literal: {ast.dump(node)}")


def find_mode_spec(path: Path, mode_name: str) -> dict[str, Any] | None:
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "MODE_SPECS" for target in node.targets):
            continue
        if not isinstance(node.value, ast.Dict):
            continue
        for key_node, value_node in zip(node.value.keys, node.value.values):
            if not isinstance(key_node, ast.Constant) or key_node.value != mode_name:
                continue
            if not isinstance(value_node, ast.Call):
                raise ValueError(f"{mode_name} registry entry is not a ModeSpec call")
            return {keyword.arg: literal_value(keyword.value) for keyword in value_node.keywords if keyword.arg}
    return None


def summary_path_for_config(config: dict[str, Any]) -> Path:
    return resolve_repo_path(str(config["run"]["output_dir"])) / "execution_readiness_summary.json"


def snapshot_paths(paths: list[Path]) -> dict[Path, bytes | None]:
    return {path: path.read_bytes() if path.exists() else None for path in paths}


def restore_snapshots(snapshots: dict[Path, bytes | None]) -> None:
    for path, payload in snapshots.items():
        if payload is None:
            if path.exists():
                path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)


def run_checker(config_path: Path) -> tuple[int, str, dict[str, Any] | None]:
    completed = subprocess.run(
        [sys.executable, str(CHECKER_PATH), "--config", str(config_path)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    summary_path: Path | None = None
    for line in completed.stdout.splitlines():
        if line.startswith("summary_path="):
            summary_path = resolve_repo_path(line.split("=", 1)[1].strip())
            break
    summary = load_json(summary_path) if summary_path and summary_path.exists() else None
    return completed.returncode, completed.stdout + completed.stderr, summary


def run_artifact_validator(output_dir: Path) -> tuple[int, str, dict[str, Any] | None]:
    completed = subprocess.run(
        [sys.executable, str(ARTIFACT_VALIDATOR_PATH), "--output-dir", str(output_dir)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    summary_path = output_dir / "post_run_artifact_validation_summary.json"
    summary = load_json(summary_path) if summary_path.exists() else None
    return completed.returncode, completed.stdout + completed.stderr, summary


def make_bad_config(path: Path) -> None:
    config = load_json(CONFIG_PATH)
    config["training"]["max_steps"] = 3000
    config["training"]["save_interval"] = 3000
    config["training"]["checkpoint_interval"] = 3000
    config["training"]["batch_size"] = 8
    config["profiling"]["attention_backend"] = "naive"
    write_json(path, config)


def make_profile_fixture(output_dir: Path) -> None:
    run_name = "fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile"
    checkpoint_path = output_dir / "checkpoints" / "checkpoint_step_0050.pt"
    summary = {
        "run_id": f"synthetic_{run_name}",
        "run_name": run_name,
        "output_dir": output_dir.as_posix(),
        "runtime_device": "cuda",
        "runtime_dtype": "bf16",
        "max_steps": 50,
        "eval_interval": 50,
        "batch_size": 4,
        "sequence_length": 1024,
        "data_loading_mode": "streaming",
        "tokenizer_vocab_size": 16384,
        "exact_parameter_count": 336630784,
        "first_train_loss": 9.9,
        "final_train_loss": 4.2,
        "final_val_loss": 9.0,
        "loss_all_finite": True,
        "val_loss_all_finite": True,
        "grad_all_finite": True,
        "metrics_rows": 50,
        "validation_rows": 1,
        "expected_validation_rows": 1,
        "checkpoint_path": checkpoint_path.as_posix(),
        "checkpoint_path_starts_with_output_dir": True,
        "checkpoint_reload_match": True,
        "success": True,
    }
    run_config = {
        "status": "profiling_ready_not_run",
        "run": {
            "run_name": run_name,
            "output_dir": output_dir.as_posix(),
        },
        "data": {
            "sequence_length": 1024,
        },
        "model": {
            "context_length": 1024,
        },
        "training": {
            "max_steps": 50,
            "eval_interval": 50,
            "batch_size": 4,
            "gradient_accumulation_steps": 4,
            "sequence_length": 1024,
        },
        "profiling": {
            "enabled": True,
            "profile_mode": "bounded_seq1024_sdpa_profile",
            "attention_backend": "sdpa",
            "record_tokens_per_sec": True,
            "record_memory": True,
            "record_mfu": True,
        },
    }
    metadata = {
        "status": "success",
        "gpu_name": "NVIDIA A100-SXM4-40GB",
        "git_commit": "synthetic",
    }
    metrics = [
        {
            "step": step,
            "tokens_seen": step * 16384,
            "train_loss": 9.5 / step,
            "val_loss": None,
            "tokens_per_sec": 40000.0,
            "elapsed_seconds": 0.4,
            "gpu_memory_allocated_gib": 2.7,
            "gpu_memory_reserved_gib": 8.5,
            "mfu": None,
        }
        for step in range(1, 51)
    ]
    metrics[-1]["val_loss"] = 9.0
    validation_metrics = [{"step": 50, "tokens_seen": 819200, "val_loss": 9.0}]

    write_json(output_dir / "summary.json", summary)
    write_json(output_dir / "run_config.json", run_config)
    write_json(output_dir / "run_metadata.json", metadata)
    write_jsonl(output_dir / "metrics.jsonl", metrics)
    write_jsonl(output_dir / "validation_metrics.jsonl", validation_metrics)


def main() -> int:
    blockers: list[str] = []
    mode_spec = find_mode_spec(RUNNER_PATH, MODE_NAME)
    config = load_json(CONFIG_PATH) if CONFIG_PATH.exists() else {}
    if mode_spec is None:
        blockers.append(f"{MODE_NAME} mode is missing from MODE_SPECS")
        mode_spec = {}
    if not CONFIG_PATH.exists():
        blockers.append(f"missing config: {CONFIG_PATH.relative_to(REPO_ROOT).as_posix()}")

    training = config.get("training", {}) if isinstance(config.get("training"), dict) else {}
    model = config.get("model", {}) if isinstance(config.get("model"), dict) else {}
    data = config.get("data", {}) if isinstance(config.get("data"), dict) else {}
    profiling = config.get("profiling", {}) if isinstance(config.get("profiling"), dict) else {}
    sampling = config.get("sampling", {}) if isinstance(config.get("sampling"), dict) else {}
    validation_sampling = config.get("validation_sampling", {}) if isinstance(config.get("validation_sampling"), dict) else {}

    config_path = mode_spec.get("config_path")
    expected_result_package = mode_spec.get("result_package")
    context_length = model.get("context_length")
    max_steps = training.get("max_steps")
    batch_size = training.get("batch_size")
    grad_accum = training.get("gradient_accumulation_steps")
    attention_backend = profiling.get("attention_backend")
    profiling_flags = {flag: profiling.get(flag) for flag in EXPECTED_FLAGS}

    if config_path != EXPECTED_CONFIG_PATH:
        blockers.append(f"mode config_path expected {EXPECTED_CONFIG_PATH!r}, got {config_path!r}")
    if mode_spec.get("package_path") != EXPECTED_PACKAGE_PATH:
        blockers.append(f"mode package_path expected {EXPECTED_PACKAGE_PATH!r}, got {mode_spec.get('package_path')!r}")
    if expected_result_package != EXPECTED_RESULT_PACKAGE:
        blockers.append(f"result_package expected {EXPECTED_RESULT_PACKAGE!r}, got {expected_result_package!r}")
    if mode_spec.get("train") is not True:
        blockers.append("seq1024 profiling mode must run the bounded training/profiling path")
    if context_length != 1024 or data.get("sequence_length") != 1024 or training.get("sequence_length") != 1024:
        blockers.append("context/sequence length must be 1024 across model, data, and training")
    if max_steps != 50:
        blockers.append(f"max_steps expected 50, got {max_steps!r}")
    if batch_size != 4:
        blockers.append(f"batch_size expected 4, got {batch_size!r}")
    if grad_accum != 4:
        blockers.append(f"grad_accum expected 4, got {grad_accum!r}")
    if attention_backend != "sdpa":
        blockers.append(f"attention_backend expected sdpa, got {attention_backend!r}")
    if sampling.get("policy") != "shuffle_buffer" or sampling.get("shuffle_seed") != 1337:
        blockers.append("train sampling must be shuffle_buffer with seed 1337")
    if validation_sampling.get("policy") != "shuffle_buffer" or validation_sampling.get("shuffle_seed") != 7331:
        blockers.append("validation_sampling must be shuffle_buffer with seed 7331")
    for flag, value in profiling_flags.items():
        if value is not True:
            blockers.append(f"profiling.{flag} expected true, got {value!r}")

    readiness_passed = False
    synthetic_artifact_validation_passed = False
    bad_config_rejected = False
    readiness_output = ""
    artifact_output = ""
    bad_output = ""
    snapshots = snapshot_paths([summary_path_for_config(config)]) if config else {}
    try:
        readiness_returncode, readiness_output, readiness_summary = run_checker(CONFIG_PATH)
        readiness_passed = (
            readiness_returncode == 0
            and readiness_summary is not None
            and readiness_summary.get("status") == "success"
            and readiness_summary.get("readiness_gate_type") == "bounded_seq1024_sdpa_profile"
            and readiness_summary.get("max_steps") == 50
            and readiness_summary.get("profiling_attention_backend") == "sdpa"
            and readiness_summary.get("profiling_expected_result_package") == EXPECTED_RESULT_PACKAGE
        )
        if not readiness_passed:
            blockers.append("seq1024 50-step profile config did not pass readiness gate")

        with tempfile.TemporaryDirectory(prefix="mvp30_seq1024_profile_") as temp_dir:
            profile_dir = Path(temp_dir) / "profile"
            make_profile_fixture(profile_dir)
            artifact_returncode, artifact_output, artifact_summary = run_artifact_validator(profile_dir)
            synthetic_artifact_validation_passed = (
                artifact_returncode == 0
                and artifact_summary is not None
                and artifact_summary.get("status") == "success"
                and artifact_summary.get("artifact_validation_gate_type") == "bounded_seq1024_sdpa_profile"
                and artifact_summary.get("metrics_rows_actual") == 50
                and artifact_summary.get("validation_rows_actual") == 1
            )
            if not synthetic_artifact_validation_passed:
                blockers.append("synthetic seq1024 50-step profile artifact did not pass validation")

            bad_config_path = Path(temp_dir) / "bad_seq1024_profile.json"
            make_bad_config(bad_config_path)
            bad_returncode, bad_output, bad_summary = run_checker(bad_config_path)
            bad_config_rejected = (
                bad_returncode != 0
                and (
                    (
                        bad_summary is not None
                        and bad_summary.get("status") == "failed"
                        and bad_summary.get("blocker_count", 0) > 0
                    )
                    or "valueerror" in bad_output.lower()
                    or "blocker" in bad_output.lower()
                )
            )
            if not bad_config_rejected:
                blockers.append("bad seq1024 profile config was not rejected")
    finally:
        restore_snapshots(snapshots)

    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "mode_name": MODE_NAME,
        "config_path": config_path,
        "context_length": context_length,
        "max_steps": max_steps,
        "batch_size": batch_size,
        "grad_accum": grad_accum,
        "attention_backend": attention_backend,
        "expected_result_package": expected_result_package,
        "profiling_flags": profiling_flags,
        "readiness_passed": readiness_passed,
        "synthetic_artifact_validation_passed": synthetic_artifact_validation_passed,
        "bad_config_rejected": bad_config_rejected,
        "readiness_output_excerpt": readiness_output.splitlines()[-8:],
        "artifact_output_excerpt": artifact_output.splitlines()[-8:],
        "bad_config_output_excerpt": bad_output.splitlines()[-8:],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
