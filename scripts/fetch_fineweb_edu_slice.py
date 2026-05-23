from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "data" / "fineweb_edu_sample10bt_50mb.json"
DEFAULT_DRY_RUN_RECORDS = 5


def read_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_repo_path(path_text: str) -> Path:
    return PROJECT_ROOT / Path(path_text)


def iter_streaming_records(config: dict[str, Any]):
    from datasets import load_dataset

    dataset = load_dataset(
        config["dataset_id"],
        name=config["dataset_config"],
        split=config["split"],
        streaming=config["streaming"],
    )
    return iter(dataset)


def build_manifest(config: dict[str, Any], actual_size_bytes: int, record_count: int) -> dict[str, Any]:
    return {
        "dataset_id": config["dataset_id"],
        "dataset_config": config["dataset_config"],
        "split": config["split"],
        "target_size_mb": config["target_size_mb"],
        "actual_size_bytes": actual_size_bytes,
        "record_count": record_count,
        "license": config["license"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "text_field": config["text_field"],
        "allowed_for_training": config["allowed_for_training"],
    }


def run_dry_run(config: dict[str, Any], preview_records: int) -> int:
    iterator = iter_streaming_records(config)
    record_count = 0
    accumulated_bytes = 0
    for _ in range(preview_records):
        record = next(iterator)
        text = str(record.get(config["text_field"], ""))
        accumulated_bytes += len(text.encode("utf-8"))
        record_count += 1

    print(f"dry_run=true")
    print(f"record_count={record_count}")
    print(f"size_mb={accumulated_bytes / (1024 * 1024):.6f}")
    print(f"output_path={config['output_jsonl']}")
    return 0


def run_fetch(config: dict[str, Any]) -> int:
    output_dir = resolve_repo_path(config["output_dir"])
    output_jsonl = resolve_repo_path(config["output_jsonl"])
    manifest_path = resolve_repo_path(config["manifest_path"])
    output_dir.mkdir(parents=True, exist_ok=True)

    target_size_bytes = int(config["target_size_mb"]) * 1024 * 1024
    iterator = iter_streaming_records(config)
    record_count = 0
    accumulated_bytes = 0

    with output_jsonl.open("w", encoding="utf-8") as handle:
        while accumulated_bytes < target_size_bytes:
            record = next(iterator)
            text = str(record.get(config["text_field"], ""))
            text_bytes = len(text.encode("utf-8"))
            handle.write(json.dumps({config["text_field"]: text}, ensure_ascii=False) + "\n")
            accumulated_bytes += text_bytes
            record_count += 1

    manifest = build_manifest(config, accumulated_bytes, record_count)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"dry_run=false")
    print(f"record_count={record_count}")
    print(f"size_mb={accumulated_bytes / (1024 * 1024):.6f}")
    print(f"output_path={output_jsonl.relative_to(PROJECT_ROOT).as_posix()}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch a bounded FineWeb-Edu streaming slice.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the fetch config JSON.")
    parser.add_argument("--dry-run", action="store_true", help="Read a few records without writing a large output file.")
    parser.add_argument(
        "--preview-records",
        type=int,
        default=DEFAULT_DRY_RUN_RECORDS,
        help="Number of records to inspect in dry-run mode.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    config = read_config(config_path)
    if args.dry_run:
        return run_dry_run(config, args.preview_records)
    return run_fetch(config)


if __name__ == "__main__":
    raise SystemExit(main())
