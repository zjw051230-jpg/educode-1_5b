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
CONFIG_PATH = (
    REPO_ROOT
    / "configs"
    / "a100"
    / "fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight.json"
)
MODE_NAME = "preflight_5gb_10step_seq1024_sdpa_memory"
EXPECTED_CONFIG_PATH = "configs/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight.json"
EXPECTED_PACKAGE_PATH = "/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz"
EXPECTED_RESULT_PACKAGE = "/vol/results/mvp29_a100_5gb_10step_seq1024_sdpa_memory_preflight_results.tar.gz"
EXPECTED_FLAGS = ("record_tokens_per_sec", "record_memory", "record_mfu")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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


def make_bad_seq1024_config(path: Path) -> None:
    config = load_json(CONFIG_PATH)
    config["training"]["max_steps"] = 3000
    config["training"]["save_interval"] = 3000
    config["training"]["checkpoint_interval"] = 3000
    config["training"]["batch_size"] = 8
    config["profiling"]["expected_result_package"] = "/vol/results/bad_seq1024_memory_preflight.tar.gz"
    write_json(path, config)


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
    validation_sampling = (
        config.get("validation_sampling", {}) if isinstance(config.get("validation_sampling"), dict) else {}
    )

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
        blockers.append("memory preflight mode must run the bounded training/profiling path")
    if context_length != 1024 or data.get("sequence_length") != 1024 or training.get("sequence_length") != 1024:
        blockers.append("context/sequence length must be 1024 across model, data, and training")
    if max_steps != 10:
        blockers.append(f"max_steps expected 10, got {max_steps!r}")
    if batch_size != 4:
        blockers.append(f"batch_size expected 4, got {batch_size!r}")
    if grad_accum != 4:
        blockers.append(f"grad_accum expected 4, got {grad_accum!r}")
    if attention_backend != "sdpa":
        blockers.append(f"attention_backend expected sdpa, got {attention_backend!r}")
    if data.get("data_loading_mode") != "streaming" or data.get("streaming") is not True:
        blockers.append("data_loading_mode must be streaming")
    if sampling.get("policy") != "shuffle_buffer" or sampling.get("shuffle_seed") != 1337:
        blockers.append("train sampling must be shuffle_buffer with seed 1337")
    if validation_sampling.get("policy") != "shuffle_buffer" or validation_sampling.get("shuffle_seed") != 7331:
        blockers.append("validation_sampling must be shuffle_buffer with seed 7331")
    for flag, value in profiling_flags.items():
        if value is not True:
            blockers.append(f"profiling.{flag} expected true, got {value!r}")

    readiness_passed = False
    bad_config_rejected = False
    readiness_output = ""
    bad_output = ""
    snapshots = snapshot_paths([summary_path_for_config(config)]) if config else {}
    try:
        readiness_returncode, readiness_output, readiness_summary = run_checker(CONFIG_PATH)
        readiness_passed = (
            readiness_returncode == 0
            and readiness_summary is not None
            and readiness_summary.get("status") == "success"
            and readiness_summary.get("readiness_gate_type") == "bounded_seq1024_sdpa_memory_preflight"
            and readiness_summary.get("max_steps") == 10
            and readiness_summary.get("profiling_attention_backend") == "sdpa"
            and readiness_summary.get("profiling_record_tokens_per_sec") is True
            and readiness_summary.get("profiling_record_memory") is True
            and readiness_summary.get("profiling_record_mfu") is True
            and readiness_summary.get("profiling_expected_result_package") == EXPECTED_RESULT_PACKAGE
        )
        if not readiness_passed:
            blockers.append("seq1024 memory preflight config did not pass readiness gate")

        with tempfile.TemporaryDirectory(prefix="mvp29_bad_seq1024_") as temp_dir:
            bad_config_path = Path(temp_dir) / "bad_seq1024.json"
            make_bad_seq1024_config(bad_config_path)
            bad_returncode, bad_output, bad_summary = run_checker(bad_config_path)
            bad_config_rejected = (
                bad_returncode != 0
                and bad_summary is not None
                and bad_summary.get("status") == "failed"
                and bad_summary.get("readiness_gate_type") == "bounded_seq1024_sdpa_memory_preflight"
                and bad_summary.get("blocker_count", 0) > 0
            )
        if not bad_config_rejected:
            blockers.append("bad seq1024 memory preflight config was not rejected")
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
        "bad_config_rejected": bad_config_rejected,
        "readiness_output_excerpt": readiness_output.splitlines()[-8:],
        "bad_config_output_excerpt": bad_output.splitlines()[-8:],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
