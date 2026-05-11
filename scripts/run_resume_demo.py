from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_PATHS = [
    PROJECT_ROOT / "configs" / "windows" / "smoke_cuda_10m.json",
    PROJECT_ROOT / "scripts" / "run_50_step_toy_training.py",
    PROJECT_ROOT / "src" / "educode" / "tiny_model.py",
    PROJECT_ROOT / "src" / "educode" / "losses.py",
    PROJECT_ROOT / "src" / "educode" / "checkpoint.py",
    PROJECT_ROOT / "src" / "educode" / "generation.py",
    PROJECT_ROOT / "src" / "educode" / "run_logging.py",
]


def main() -> int:
    print("EduCode-1.5B Resume Demo")
    print("- This demo runs a bounded 50-step toy training loop.")
    print("- It uses toy data and a tiny model.")
    print("- It is not real pretraining.")

    missing_paths = [path for path in REQUIRED_PATHS if not path.exists()]
    if missing_paths:
        print("Missing required files:")
        for path in missing_paths:
            print(f"- {path}")
        return 1

    command = [sys.executable, str(PROJECT_ROOT / "scripts" / "run_50_step_toy_training.py")]
    print("Running command:")
    print(" ".join(command))

    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired as exc:
        print("Demo failed: timed out after 120 seconds.")
        if exc.stdout:
            print(exc.stdout)
        if exc.stderr:
            print(exc.stderr)
        return 1
    except Exception as exc:
        print(f"Demo failed: {exc}")
        return 1

    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print("stderr:")
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n")

    print(f"Return code: {result.returncode}")
    if result.returncode == 0:
        print("Resume demo completed successfully.")
        return 0

    print("Resume demo failed. See output above for details.")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
