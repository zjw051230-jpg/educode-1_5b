from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "data" / "fineweb_edu_sample10bt_50mb.json"
PROCESSED_FILENAME = "fineweb_edu_50mb.processed.jsonl"
TRAIN_FILENAME = "fineweb_edu_50mb.train.jsonl"
VAL_FILENAME = "fineweb_edu_50mb.val.jsonl"
INTAKE_SUMMARY_FILENAME = "intake_summary.json"
INTAKE_VALIDATION_SUMMARY_FILENAME = "intake_validation_summary.json"
EXPECTED_LICENSE = "odc-by"
EXPECTED_SOURCE_CATEGORY = "public_pretraining_corpus"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_repo_path(path_text: str) -> Path:
    return PROJECT_ROOT / Path(path_text)


def parse_jsonl_records(path: Path) -> tuple[list[dict[str, Any]], int]:
    if not path.exists():
        raise FileNotFoundError(f"missing jsonl file: {path}")

    records: list[dict[str, Any]] = []
    total_text_bytes = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                raise ValueError(f"line {line_number} is empty in {path}")
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {line_number} is not valid JSON in {path}: {exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"line {line_number} is not a JSON object in {path}")
            if "text" not in record:
                raise ValueError(f"line {line_number} is missing text in {path}")
            if not isinstance(record["text"], str):
                raise ValueError(f"line {line_number} text is not a string in {path}")
            if record.get("allowed_for_training") is not True:
                raise ValueError(f"line {line_number} allowed_for_training is not true in {path}")
            if record.get("license") != EXPECTED_LICENSE:
                raise ValueError(f"line {line_number} license is not {EXPECTED_LICENSE} in {path}")
            if record.get("source_category") != EXPECTED_SOURCE_CATEGORY:
                raise ValueError(f"line {line_number} source_category is not {EXPECTED_SOURCE_CATEGORY} in {path}")
            if "doc_id" not in record or not isinstance(record["doc_id"], str) or record["doc_id"] == "":
                raise ValueError(f"line {line_number} doc_id is missing or invalid in {path}")
            records.append(record)
            total_text_bytes += len(record["text"].encode("utf-8"))
    return records, total_text_bytes


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate FineWeb-Edu intake processed and split artifacts.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the fetch config JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = read_json(Path(args.config))
    output_root = resolve_repo_path(config["output_dir"])
    intake_summary_path = output_root / INTAKE_SUMMARY_FILENAME
    if not intake_summary_path.exists():
        raise FileNotFoundError(f"missing intake summary: {intake_summary_path}")

    intake_summary = read_json(intake_summary_path)
    processed_path = output_root / "processed" / PROCESSED_FILENAME
    train_path = output_root / "splits" / TRAIN_FILENAME
    val_path = output_root / "splits" / VAL_FILENAME
    validation_summary_path = output_root / INTAKE_VALIDATION_SUMMARY_FILENAME

    processed_records, total_text_bytes = parse_jsonl_records(processed_path)
    train_records, train_text_bytes = parse_jsonl_records(train_path)
    val_records, val_text_bytes = parse_jsonl_records(val_path)

    processed_doc_ids = {record["doc_id"] for record in processed_records}
    train_doc_ids = {record["doc_id"] for record in train_records}
    val_doc_ids = {record["doc_id"] for record in val_records}

    overlap = train_doc_ids & val_doc_ids
    if overlap:
        raise ValueError(f"train/val overlap detected for {len(overlap)} doc_ids")
    if len(processed_records) != len(processed_doc_ids):
        raise ValueError("processed doc_id values are not unique")
    if processed_doc_ids != train_doc_ids | val_doc_ids:
        raise ValueError("processed doc_id set does not match train/val union")

    summary = {
        "dataset_id": intake_summary["dataset_id"],
        "dataset_config": intake_summary["dataset_config"],
        "license": intake_summary["license"],
        "allowed_for_training": intake_summary["allowed_for_training"],
        "processed_count": len(processed_records),
        "train_count": len(train_records),
        "val_count": len(val_records),
        "dropped_empty_count": intake_summary["dropped_empty_count"],
        "dropped_duplicate_count": intake_summary["dropped_duplicate_count"],
        "total_text_bytes": total_text_bytes,
        "train_text_bytes": train_text_bytes,
        "val_text_bytes": val_text_bytes,
        "processed_path": processed_path.relative_to(PROJECT_ROOT).as_posix(),
        "train_path": train_path.relative_to(PROJECT_ROOT).as_posix(),
        "val_path": val_path.relative_to(PROJECT_ROOT).as_posix(),
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(validation_summary_path, summary)

    print(f"processed_count={summary['processed_count']}")
    print(f"train_count={summary['train_count']}")
    print(f"val_count={summary['val_count']}")
    print(f"dropped_empty_count={summary['dropped_empty_count']}")
    print(f"dropped_duplicate_count={summary['dropped_duplicate_count']}")
    print(f"total_text_bytes={summary['total_text_bytes']}")
    print(f"train_text_bytes={summary['train_text_bytes']}")
    print(f"val_text_bytes={summary['val_text_bytes']}")
    print(f"validation_summary_path={validation_summary_path.relative_to(PROJECT_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
