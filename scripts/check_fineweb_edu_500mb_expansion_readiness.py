from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "configs" / "data" / "fineweb_edu_sample10bt_500mb.json"
SUMMARY_FILENAME = "expansion_readiness_summary.json"
EXPECTED_CONFIG = {
    "dataset_id": "HuggingFaceFW/fineweb-edu",
    "dataset_config": "sample-10BT",
    "target_size_mb": 500,
    "output_dir": "data/public_corpus/fineweb_edu_sample10bt_500mb",
    "output_jsonl": "data/public_corpus/fineweb_edu_sample10bt_500mb/raw.jsonl",
    "manifest_path": "data/public_corpus/fineweb_edu_sample10bt_500mb/manifest.json",
}
REQUIRED_SCRIPT_PATHS = [
    "scripts/fetch_fineweb_edu_slice.py",
    "scripts/validate_fineweb_edu_slice.py",
    "scripts/intake_fineweb_edu_slice.py",
    "scripts/validate_fineweb_edu_intake.py",
]
RAW_GITIGNORE_RULE = "data/public_corpus/*/raw.jsonl"
PROCESSED_GITIGNORE_RULE = "data/public_corpus/*/processed/"
SPLITS_GITIGNORE_RULE = "data/public_corpus/*/splits/"


def repo_relative(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add_blocker(blockers: list[str], condition: bool, message: str) -> None:
    if not condition:
        blockers.append(message)


def main() -> int:
    blockers: list[str] = []
    warnings: list[str] = []

    add_blocker(blockers, CONFIG_PATH.exists(), f"missing config: {repo_relative(CONFIG_PATH)}")
    config = read_json(CONFIG_PATH) if CONFIG_PATH.exists() else {}

    for key, expected_value in EXPECTED_CONFIG.items():
        actual_value = config.get(key)
        add_blocker(
            blockers,
            actual_value == expected_value,
            f"config {key} expected {expected_value!r}, got {actual_value!r}",
        )

    for script_path_text in REQUIRED_SCRIPT_PATHS:
        script_path = PROJECT_ROOT / script_path_text
        add_blocker(blockers, script_path.exists(), f"missing script: {script_path_text}")

    gitignore_path = PROJECT_ROOT / ".gitignore"
    add_blocker(blockers, gitignore_path.exists(), "missing .gitignore")
    gitignore_lines = set(gitignore_path.read_text(encoding="utf-8").splitlines()) if gitignore_path.exists() else set()
    raw_jsonl_ignored = RAW_GITIGNORE_RULE in gitignore_lines
    processed_ignored = PROCESSED_GITIGNORE_RULE in gitignore_lines
    splits_ignored = SPLITS_GITIGNORE_RULE in gitignore_lines
    processed_splits_ignored = processed_ignored and splits_ignored

    add_blocker(blockers, raw_jsonl_ignored, f"missing .gitignore rule: {RAW_GITIGNORE_RULE}")
    add_blocker(blockers, processed_ignored, f"missing .gitignore rule: {PROCESSED_GITIGNORE_RULE}")
    add_blocker(blockers, splits_ignored, f"missing .gitignore rule: {SPLITS_GITIGNORE_RULE}")

    output_dir_text = str(config.get("output_dir", EXPECTED_CONFIG["output_dir"]))
    output_jsonl_text = str(config.get("output_jsonl", EXPECTED_CONFIG["output_jsonl"]))
    manifest_path_text = str(config.get("manifest_path", EXPECTED_CONFIG["manifest_path"]))
    output_dir = PROJECT_ROOT / output_dir_text
    raw_jsonl_path = PROJECT_ROOT / output_jsonl_text
    processed_dir = output_dir / "processed"
    splits_dir = output_dir / "splits"
    summary_path = output_dir / SUMMARY_FILENAME

    add_blocker(blockers, output_dir.exists(), f"missing output_dir: {output_dir_text}")
    add_blocker(blockers, not raw_jsonl_path.exists(), f"raw.jsonl already exists: {output_jsonl_text}")
    add_blocker(blockers, not processed_dir.exists(), f"processed directory already exists: {repo_relative(processed_dir)}")
    add_blocker(blockers, not splits_dir.exists(), f"splits directory already exists: {repo_relative(splits_dir)}")

    warnings.append(
        "Existing intake scripts are config-driven for directories but currently use 50mb output basenames; align MVP-11.1 expected filenames before intake if strict 500mb names are required."
    )

    ready_for_500mb_fetch = len(blockers) == 0
    summary = {
        "status": "ready" if ready_for_500mb_fetch else "blocked",
        "ready_for_500mb_fetch": ready_for_500mb_fetch,
        "blockers": len(blockers),
        "blocker_details": blockers,
        "warnings": warnings,
        "config_path": repo_relative(CONFIG_PATH),
        "target_size_mb": config.get("target_size_mb"),
        "output_dir": output_dir_text,
        "output_jsonl": output_jsonl_text,
        "manifest_path": manifest_path_text,
        "raw_jsonl_ignored": raw_jsonl_ignored,
        "processed_splits_ignored": processed_splits_ignored,
        "output_dir_exists": output_dir.exists(),
        "raw_jsonl_exists": raw_jsonl_path.exists(),
        "processed_dir_exists": processed_dir.exists(),
        "splits_dir_exists": splits_dir.exists(),
        "required_scripts_present": all((PROJECT_ROOT / script_path).exists() for script_path in REQUIRED_SCRIPT_PATHS),
        "no_data_downloaded_in_this_step": True,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(summary_path, summary)

    print(f"status={summary['status']}")
    print(f"ready_for_500mb_fetch={str(ready_for_500mb_fetch).lower()}")
    print(f"blockers={len(blockers)}")
    print(f"warnings={len(warnings)}")
    print(f"summary_path={repo_relative(summary_path)}")
    return 0 if ready_for_500mb_fetch else 1


if __name__ == "__main__":
    raise SystemExit(main())
