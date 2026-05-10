from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.config_loader import load_json_config
from educode.config_validator import validate_config
from educode.run_setup import (
    collect_basic_environment,
    create_run_directory,
    get_git_branch,
    get_git_commit,
    make_run_id,
    snapshot_config,
    write_run_metadata,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create minimal run setup for a config")
    parser.add_argument("config_path", nargs="?", default="configs/windows/smoke_cuda_10m.json")
    parser.add_argument("--stage", default="windows_cuda")
    parser.add_argument("--short-name", default="smoke_setup")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    config_input = Path(args.config_path)
    config_path = (PROJECT_ROOT / config_input).resolve() if not config_input.is_absolute() else config_input

    config = load_json_config(config_path)
    errors = validate_config(config)

    if errors:
        print("Validation: failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation: passed")

    run_id = make_run_id(args.stage, args.short_name)
    run_dir = create_run_directory(PROJECT_ROOT, args.stage, run_id)
    snapshot_path = snapshot_config(config_path, run_dir)

    env = collect_basic_environment()
    git_commit = get_git_commit(PROJECT_ROOT)
    git_branch = get_git_branch(PROJECT_ROOT)
    hardware_target = config.get("hardware", {}).get("target") if isinstance(config.get("hardware"), dict) else None

    metadata_path = write_run_metadata(
        run_dir=run_dir,
        run_id=run_id,
        project="EduCode-1.5B",
        stage=args.stage,
        hardware_target=hardware_target or args.stage,
        config_path=str(config_path),
        git_commit=git_commit,
        git_branch=git_branch,
        env=env,
        status="planned",
        notes="Run setup only. No training executed.",
    )

    print(f"Run ID: {run_id}")
    print(f"Run directory created: {run_dir}")
    print(f"Config snapshot created: {snapshot_path}")
    print(f"Run metadata created: {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
