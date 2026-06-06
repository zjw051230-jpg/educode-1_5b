from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def imported_run_dirs() -> list[Path]:
    return sorted(
        path.parent
        for path in (REPO_ROOT / "experiments").rglob("summary.json")
        if "results_imported_modal_streaming" in path.parts
    )


def cmd_list_runs(_: argparse.Namespace) -> int:
    runs = imported_run_dirs()
    print(f"runs_found={len(runs)}")
    print("tarballs_read=false")
    for run in runs:
        print(run.relative_to(REPO_ROOT).as_posix())
    return 0


def cmd_validate_artifacts(_: argparse.Namespace) -> int:
    blockers = []
    for run in imported_run_dirs():
        for name in ("summary.json", "metrics.jsonl", "validation_metrics.jsonl"):
            if not (run / name).exists():
                blockers.append(f"{run.relative_to(REPO_ROOT).as_posix()} missing {name}")
    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "tarballs_read": False,
        "modal_gpu_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not blockers else 1


def cmd_build_report(_: argparse.Namespace) -> int:
    report = {
        "report_status": "generated",
        "runs_found": len(imported_run_dirs()),
        "output_written": False,
        "tarballs_read": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def cmd_show_branch_inventory(_: argparse.Namespace) -> int:
    path = REPO_ROOT / "docs" / "branch_asset_inventory.md"
    print(path.read_text(encoding="utf-8").splitlines()[0])
    print(f"path={path.relative_to(REPO_ROOT).as_posix()}")
    return 0


def cmd_show_next_candidates(_: argparse.Namespace) -> int:
    candidates = [
        "docs/llm-systems-survey-roadmap",
        "feature/tokenizer-stats-analyzer",
        "feature/training-report-generator",
    ]
    print(json.dumps({"next_candidates": candidates}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="EduCode local experiment manager")
    subparsers = parser.add_subparsers(dest="command", required=True)
    commands = {
        "list-runs": cmd_list_runs,
        "validate-artifacts": cmd_validate_artifacts,
        "build-report": cmd_build_report,
        "show-branch-inventory": cmd_show_branch_inventory,
        "show-next-candidates": cmd_show_next_candidates,
    }
    for name, handler in commands.items():
        subparser = subparsers.add_parser(name)
        subparser.set_defaults(func=handler)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
