from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPO_ROOT / "scripts" / "check_a100_execution_readiness.py"
PROFILE_CONFIG_PATH = REPO_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile.json"
TRAIN_3000_CONFIG_PATH = REPO_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"
EXPECTED_PROFILE_PACKAGE = "/vol/results/mvp28_a100_5gb_50step_sdpa_profile_results.tar.gz"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_repo_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


def summary_path_for_config(config_path: Path) -> Path:
    config = load_json(config_path)
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
    output = completed.stdout + completed.stderr
    return completed.returncode, output, summary


def make_bad_profile_config(path: Path) -> None:
    config = load_json(PROFILE_CONFIG_PATH)
    config["training"]["max_steps"] = 10000
    config["profiling"]["record_memory"] = False
    config["profiling"]["expected_result_package"] = "/vol/results/not_the_expected_profile_package.tar.gz"
    write_json(path, config)


def main() -> int:
    blockers: list[str] = []
    profile_summary_path = summary_path_for_config(PROFILE_CONFIG_PATH)
    train_summary_path = summary_path_for_config(TRAIN_3000_CONFIG_PATH)
    snapshots = snapshot_paths([profile_summary_path, train_summary_path])

    profile_config_readiness_passed = False
    train_config_readiness_still_passed = False
    bad_profile_rejected = False
    profile_output = ""
    train_output = ""
    bad_output = ""

    try:
        profile_returncode, profile_output, profile_summary = run_checker(PROFILE_CONFIG_PATH)
        profile_config_readiness_passed = (
            profile_returncode == 0
            and profile_summary is not None
            and profile_summary.get("status") == "success"
            and profile_summary.get("readiness_gate_type") == "bounded_sdpa_profile"
            and profile_summary.get("max_steps") == 50
            and profile_summary.get("profiling_attention_backend") == "sdpa"
            and profile_summary.get("profiling_record_tokens_per_sec") is True
            and profile_summary.get("profiling_record_memory") is True
            and profile_summary.get("profiling_record_mfu") is True
            and profile_summary.get("profiling_expected_result_package") == EXPECTED_PROFILE_PACKAGE
            and profile_summary.get("validation_sampling_policy") == "shuffle_buffer"
        )
        if not profile_config_readiness_passed:
            blockers.append("profile 50-step config did not pass bounded_sdpa_profile readiness")

        train_returncode, train_output, train_summary = run_checker(TRAIN_3000_CONFIG_PATH)
        train_config_readiness_still_passed = (
            train_returncode == 0
            and train_summary is not None
            and train_summary.get("status") == "success"
            and train_summary.get("readiness_gate_type") == "training_execution"
            and train_summary.get("max_steps") == 3000
        )
        if not train_config_readiness_still_passed:
            blockers.append("train_5gb_3000 config no longer passes training_execution readiness")

        with tempfile.TemporaryDirectory(prefix="mvp28_bad_profile_") as temp_dir:
            bad_config_path = Path(temp_dir) / "bad_profile.json"
            make_bad_profile_config(bad_config_path)
            bad_returncode, bad_output, bad_summary = run_checker(bad_config_path)
            bad_profile_rejected = (
                bad_returncode != 0
                and bad_summary is not None
                and bad_summary.get("status") == "failed"
                and bad_summary.get("readiness_gate_type") == "bounded_sdpa_profile"
                and bad_summary.get("blocker_count", 0) > 0
            )
        if not bad_profile_rejected:
            blockers.append("synthetic bad profile config was not rejected")

        # Leave the real profile summary in a passing state for local inspection, then restore all summary files below.
        run_checker(PROFILE_CONFIG_PATH)
    finally:
        restore_snapshots(snapshots)

    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "profile_config_readiness_passed": profile_config_readiness_passed,
        "train_config_readiness_still_passed": train_config_readiness_still_passed,
        "bad_profile_rejected": bad_profile_rejected,
        "blockers": blockers,
        "profile_checker_output_excerpt": profile_output.splitlines()[-8:],
        "train_checker_output_excerpt": train_output.splitlines()[-8:],
        "bad_profile_checker_output_excerpt": bad_output.splitlines()[-8:],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
