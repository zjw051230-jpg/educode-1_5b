from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from importlib import metadata
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _git_value(args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def _package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def capture_environment_summary() -> dict:
    return {
        "environment_summary_status": "captured",
        "python_version": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "git_branch": _git_value(["rev-parse", "--abbrev-ref", "HEAD"]),
        "git_commit": _git_value(["rev-parse", "HEAD"]),
        "git_status_short": _git_value(["status", "--short"]),
        "package_versions": {
            "torch": _package_version("torch"),
            "tokenizers": _package_version("tokenizers"),
            "datasets": _package_version("datasets"),
            "modal": _package_version("modal"),
        },
        "modal_gpu_training_run": False,
        "notes": [
            "Local environment capture only.",
            "No Modal command, GPU workload, training, profiling, tarball import, or checkpoint operation is executed.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture a local reproducibility environment summary."
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    summary = capture_environment_summary()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
