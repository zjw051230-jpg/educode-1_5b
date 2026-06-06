from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_SUFFIXES = (
    ".tar.gz",
    ".tgz",
    ".zip",
    ".pt",
    ".pth",
    ".ckpt",
    ".safetensors",
    ".bin",
)

ALLOWED_IMPORTED_SUFFIXES = {".json", ".jsonl", ".md", ".txt"}
DEFAULT_LARGE_FILE_LIMIT_BYTES = 5 * 1024 * 1024


@dataclass(frozen=True)
class HygieneFinding:
    path: str
    reason: str
    size_bytes: int | None = None


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip()


def has_forbidden_suffix(path: str) -> bool:
    lowered = normalize_path(path).lower()
    return any(lowered.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES)


def is_result_imported_path(path: str) -> bool:
    return "/results_imported_" in f"/{normalize_path(path)}"


def is_raw_or_prepared_data_path(path: str) -> bool:
    normalized = f"/{normalize_path(path).lower()}"
    if "/data/" not in normalized:
        return False
    risky_markers = (
        "/raw/",
        "/prepared/",
        "/prepared_data/",
        "/splits/",
    )
    return any(marker in normalized for marker in risky_markers)


def is_checkpoint_path(path: str) -> bool:
    normalized = f"/{normalize_path(path).lower()}"
    return "/checkpoint" in normalized or "/checkpoints/" in normalized


def is_large_experiment_file(path: str, size_bytes: int | None, limit_bytes: int) -> bool:
    normalized = f"/{normalize_path(path).lower()}"
    return "/experiments/" in normalized and size_bytes is not None and size_bytes > limit_bytes


def classify_paths(
    paths: Iterable[str],
    *,
    repo_root: Path = REPO_ROOT,
    sizes: dict[str, int | None] | None = None,
    large_file_limit_bytes: int = DEFAULT_LARGE_FILE_LIMIT_BYTES,
) -> list[HygieneFinding]:
    findings: list[HygieneFinding] = []
    sizes = sizes or {}

    for original_path in paths:
        path = normalize_path(original_path)
        if not path:
            continue

        size_bytes = sizes.get(path)
        if size_bytes is None:
            file_path = repo_root / path
            if file_path.exists() and file_path.is_file():
                size_bytes = file_path.stat().st_size

        lowered_suffix = Path(path).suffix.lower()
        if is_result_imported_path(path) and lowered_suffix not in ALLOWED_IMPORTED_SUFFIXES:
            findings.append(HygieneFinding(path, "imported results must stay small text artifacts", size_bytes))

        if has_forbidden_suffix(path):
            findings.append(HygieneFinding(path, "forbidden large artifact or checkpoint suffix", size_bytes))

        if is_checkpoint_path(path):
            findings.append(HygieneFinding(path, "checkpoint path must not be committed", size_bytes))

        if is_raw_or_prepared_data_path(path):
            findings.append(HygieneFinding(path, "raw/prepared/split data path must not be committed", size_bytes))

        if is_large_experiment_file(path, size_bytes, large_file_limit_bytes):
            findings.append(HygieneFinding(path, "large experiment artifact must not be committed", size_bytes))

    return findings


def staged_paths(repo_root: Path = REPO_ROOT) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def build_summary(paths: list[str], findings: list[HygieneFinding]) -> dict[str, object]:
    blockers = [
        {"path": finding.path, "reason": finding.reason, "size_bytes": finding.size_bytes}
        for finding in findings
    ]
    return {
        "hygiene_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "checked_path_count": len(paths),
        "checks": [
            "forbidden tarball/checkpoint suffixes",
            "checkpoint path markers",
            "raw/prepared/split data paths",
            "non-text files in results_imported directories",
            "large files under experiments",
        ],
        "blockers": blockers,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check staged artifacts before committing.")
    parser.add_argument(
        "--paths",
        nargs="*",
        help="Explicit repo-relative paths to check. Defaults to staged files.",
    )
    parser.add_argument(
        "--large-file-limit-mb",
        type=float,
        default=DEFAULT_LARGE_FILE_LIMIT_BYTES / (1024 * 1024),
        help="Large-file blocker threshold for experiments/ paths.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = args.paths if args.paths is not None else staged_paths()
    findings = classify_paths(
        paths,
        large_file_limit_bytes=int(args.large_file_limit_mb * 1024 * 1024),
    )
    summary = build_summary(list(paths), findings)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
