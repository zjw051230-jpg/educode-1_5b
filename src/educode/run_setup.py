from __future__ import annotations

import json
import platform
import re
import shutil
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def _sanitize_part(value: str) -> str:
    cleaned = value.strip().lower().replace(" ", "_")
    cleaned = re.sub(r"[^a-z0-9_-]+", "", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned)
    return cleaned.strip("_-")


def make_run_id(stage: str, short_name: str, now: datetime | None = None) -> str:
    sanitized_stage = _sanitize_part(stage)
    sanitized_short_name = _sanitize_part(short_name)

    if not sanitized_stage:
        raise ValueError("stage must not be empty")
    if not sanitized_short_name:
        raise ValueError("short_name must not be empty")

    timestamp = (now or datetime.now()).strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{sanitized_stage}_{sanitized_short_name}"


def _run_git_command(project_root: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
    except Exception:
        return None

    value = result.stdout.strip()
    return value or None


def get_git_commit(project_root: Path) -> str | None:
    return _run_git_command(project_root, ["rev-parse", "HEAD"])


def get_git_branch(project_root: Path) -> str | None:
    return _run_git_command(project_root, ["branch", "--show-current"])


def collect_basic_environment() -> dict[str, Any]:
    return {
        "hostname": socket.gethostname(),
        "os": platform.platform(),
        "python_version": sys.version.replace("\n", " "),
    }


def create_run_directory(project_root: Path, stage: str, run_id: str) -> Path:
    run_dir = project_root / "experiments" / stage / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def snapshot_config(config_path: Path, run_dir: Path) -> Path:
    snapshot_path = run_dir / "run_config.json"
    shutil.copyfile(config_path, snapshot_path)
    return snapshot_path


def write_run_metadata(
    run_dir: Path,
    run_id: str,
    project: str,
    stage: str,
    hardware_target: str,
    config_path: str,
    git_commit: str | None,
    git_branch: str | None,
    env: dict[str, Any],
    status: str = "planned",
    notes: str = "",
) -> Path:
    metadata = {
        "run_id": run_id,
        "project": project,
        "stage": stage,
        "hardware_target": hardware_target,
        "hostname": env.get("hostname"),
        "os": env.get("os"),
        "python_version": env.get("python_version"),
        "torch_version": None,
        "cuda_available": None,
        "cuda_version": None,
        "cudnn_version": None,
        "gpu_name": None,
        "gpu_memory_gib": None,
        "git_commit": git_commit,
        "git_branch": git_branch,
        "config_path": config_path,
        "start_time": datetime.now().isoformat(timespec="seconds"),
        "end_time": None,
        "status": status,
        "notes": notes,
    }

    metadata_path = run_dir / "run_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    return metadata_path
