from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "data" / "fineweb_edu_sample10bt_50mb.json"
SUMMARY_FILENAME = "validation_summary.json"


def read_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_repo_path(path_text: str) -> Path:
    return PROJECT_ROOT / Path(path_text)


def build_summary(
    config: dict[str, Any],
    manifest: dict[str, Any],
    record_count: int,
    total_text_bytes: int,
    total_file_bytes: int,
    min_text_chars: int,
    max_text_chars: int,
    mean_text_chars: float,
    empty_text_count: int,
    duplicate_text_hash_count: int,
) -> dict[str, Any]:
    output_dir = resolve_repo_path(config["output_dir"])
    return {
        "dataset_id": manifest["dataset_id"],
        "dataset_config": manifest["dataset_config"],
        "license": manifest["license"],
        "allowed_for_training": manifest["allowed_for_training"],
        "record_count": record_count,
        "total_text_bytes": total_text_bytes,
        "total_file_bytes": total_file_bytes,
        "min_text_chars": min_text_chars,
        "max_text_chars": max_text_chars,
        "mean_text_chars": mean_text_chars,
        "empty_text_count": empty_text_count,
        "duplicate_text_hash_count": duplicate_text_hash_count,
        "target_size_mb": config["target_size_mb"],
        "summary_path": (output_dir / SUMMARY_FILENAME).relative_to(PROJECT_ROOT).as_posix(),
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }


def validate_raw_jsonl(raw_jsonl_path: Path, text_field: str) -> tuple[int, int, int, int, int, float, int, int]:
    if not raw_jsonl_path.exists():
        raise FileNotFoundError(f"missing raw jsonl: {raw_jsonl_path}")

    total_file_bytes = raw_jsonl_path.stat().st_size
    record_count = 0
    total_text_bytes = 0
    text_lengths: list[int] = []
    empty_text_count = 0
    text_hash_counts: dict[str, int] = {}

    with raw_jsonl_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                raise ValueError(f"line {line_number} is empty")

            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {line_number} is not valid JSON: {exc}") from exc

            if not isinstance(record, dict):
                raise ValueError(f"line {line_number} is not a JSON object")
            if text_field not in record:
                raise ValueError(f"line {line_number} is missing required field '{text_field}'")
            if not isinstance(record[text_field], str):
                raise ValueError(f"line {line_number} field '{text_field}' is not a string")

            text = record[text_field]
            text_bytes = text.encode("utf-8")
            text_hash = hashlib.sha256(text_bytes).hexdigest()
            text_hash_counts[text_hash] = text_hash_counts.get(text_hash, 0) + 1

            record_count += 1
            total_text_bytes += len(text_bytes)
            text_lengths.append(len(text))
            if text == "":
                empty_text_count += 1

    if record_count == 0:
        raise ValueError("raw jsonl contains no records")

    duplicate_text_hash_count = sum(1 for count in text_hash_counts.values() if count > 1)
    min_text_chars = min(text_lengths)
    max_text_chars = max(text_lengths)
    mean_text_chars = round(mean(text_lengths), 6)
    return (
        record_count,
        total_text_bytes,
        total_file_bytes,
        min_text_chars,
        max_text_chars,
        mean_text_chars,
        empty_text_count,
        duplicate_text_hash_count,
    )


def write_summary(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a bounded FineWeb-Edu slice.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the fetch config JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    config = read_config(config_path)
    raw_jsonl_path = resolve_repo_path(config["output_jsonl"])
    manifest_path = resolve_repo_path(config["manifest_path"])
    summary_path = resolve_repo_path(config["output_dir"]) / SUMMARY_FILENAME

    if not manifest_path.exists():
        raise FileNotFoundError(f"missing manifest: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    (
        record_count,
        total_text_bytes,
        total_file_bytes,
        min_text_chars,
        max_text_chars,
        mean_text_chars,
        empty_text_count,
        duplicate_text_hash_count,
    ) = validate_raw_jsonl(raw_jsonl_path, config["text_field"])

    summary = build_summary(
        config,
        manifest,
        record_count,
        total_text_bytes,
        total_file_bytes,
        min_text_chars,
        max_text_chars,
        mean_text_chars,
        empty_text_count,
        duplicate_text_hash_count,
    )
    write_summary(summary_path, summary)

    print(f"record_count={summary['record_count']}")
    print(f"total_text_bytes={summary['total_text_bytes']}")
    print(f"total_file_bytes={summary['total_file_bytes']}")
    print(f"min_text_chars={summary['min_text_chars']}")
    print(f"max_text_chars={summary['max_text_chars']}")
    print(f"mean_text_chars={summary['mean_text_chars']}")
    print(f"empty_text_count={summary['empty_text_count']}")
    print(f"duplicate_text_hash_count={summary['duplicate_text_hash_count']}")
    print(f"dataset_id={summary['dataset_id']}")
    print(f"dataset_config={summary['dataset_config']}")
    print(f"license={summary['license']}")
    print(f"allowed_for_training={summary['allowed_for_training']}")
    print(f"summary_path={summary['summary_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
