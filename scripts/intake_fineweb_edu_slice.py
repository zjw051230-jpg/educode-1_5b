from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "data" / "fineweb_edu_sample10bt_50mb.json"
INTAKE_SUMMARY_FILENAME = "intake_summary.json"
SPLIT_SEED = 336
TRAIN_BUCKET_CUTOFF = 95


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_repo_path(path_text: str) -> Path:
    return PROJECT_ROOT / Path(path_text)


def build_output_basename(config: dict[str, Any]) -> str:
    target_size_mb = int(config["target_size_mb"])
    if target_size_mb % 1024 == 0:
        return f"fineweb_edu_{target_size_mb // 1024}gb"
    return f"fineweb_edu_{target_size_mb}mb"


def build_output_paths(output_root: Path, config: dict[str, Any]) -> tuple[Path, Path, Path]:
    output_basename = build_output_basename(config)
    return (
        output_root / "processed" / f"{output_basename}.processed.jsonl",
        output_root / "splits" / f"{output_basename}.train.jsonl",
        output_root / "splits" / f"{output_basename}.val.jsonl",
    )


def build_doc_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def choose_split(doc_id: str) -> str:
    bucket_input = f"{SPLIT_SEED}:{doc_id}".encode("utf-8")
    bucket_value = int(hashlib.sha256(bucket_input).hexdigest(), 16) % 100
    return "train" if bucket_value < TRAIN_BUCKET_CUTOFF else "val"


def build_processed_record(config: dict[str, Any], manifest: dict[str, Any], doc_id: str, text: str) -> dict[str, Any]:
    return {
        "doc_id": doc_id,
        "text": text,
        "source_name": "fineweb_edu",
        "dataset_id": manifest["dataset_id"],
        "dataset_config": manifest["dataset_config"],
        "source_split": manifest["split"],
        "license": manifest["license"],
        "source_category": "public_pretraining_corpus",
        "allowed_for_training": manifest["allowed_for_training"],
        "provenance_raw_file": config["output_jsonl"],
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Intake a bounded FineWeb-Edu slice into processed and split JSONL artifacts.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the fetch config JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = read_json(Path(args.config))
    manifest = read_json(resolve_repo_path(config["manifest_path"]))
    raw_jsonl_path = resolve_repo_path(config["output_jsonl"])
    output_root = resolve_repo_path(config["output_dir"])
    processed_path, train_path, val_path = build_output_paths(output_root, config)
    processed_dir = processed_path.parent
    splits_dir = train_path.parent
    intake_summary_path = output_root / INTAKE_SUMMARY_FILENAME

    if not raw_jsonl_path.exists():
        raise FileNotFoundError(f"missing raw jsonl: {raw_jsonl_path}")

    processed_dir.mkdir(parents=True, exist_ok=True)
    splits_dir.mkdir(parents=True, exist_ok=True)

    processed_count = 0
    train_count = 0
    val_count = 0
    dropped_empty_count = 0
    dropped_duplicate_count = 0
    total_text_bytes = 0
    train_text_bytes = 0
    val_text_bytes = 0
    seen_text_hashes: set[str] = set()

    with raw_jsonl_path.open("r", encoding="utf-8") as raw_handle, processed_path.open("w", encoding="utf-8") as processed_handle, train_path.open("w", encoding="utf-8") as train_handle, val_path.open("w", encoding="utf-8") as val_handle:
        for line_number, raw_line in enumerate(raw_handle, start=1):
            if not raw_line.strip():
                raise ValueError(f"line {line_number} is empty")

            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {line_number} is not valid JSON: {exc}") from exc

            if not isinstance(record, dict):
                raise ValueError(f"line {line_number} is not a JSON object")
            if config["text_field"] not in record:
                raise ValueError(f"line {line_number} is missing required field '{config['text_field']}'")
            if not isinstance(record[config["text_field"]], str):
                raise ValueError(f"line {line_number} field '{config['text_field']}' is not a string")

            text = record[config["text_field"]].strip()
            if text == "":
                dropped_empty_count += 1
                continue

            text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if text_hash in seen_text_hashes:
                dropped_duplicate_count += 1
                continue
            seen_text_hashes.add(text_hash)

            doc_id = build_doc_id(text)
            processed_record = build_processed_record(config, manifest, doc_id, text)
            processed_line = json.dumps(processed_record, ensure_ascii=False) + "\n"
            processed_handle.write(processed_line)
            processed_count += 1

            text_bytes = len(text.encode("utf-8"))
            total_text_bytes += text_bytes

            split_name = choose_split(doc_id)
            if split_name == "train":
                train_handle.write(processed_line)
                train_count += 1
                train_text_bytes += text_bytes
            else:
                val_handle.write(processed_line)
                val_count += 1
                val_text_bytes += text_bytes

    summary = {
        "dataset_id": manifest["dataset_id"],
        "dataset_config": manifest["dataset_config"],
        "license": manifest["license"],
        "allowed_for_training": manifest["allowed_for_training"],
        "split_seed": SPLIT_SEED,
        "train_ratio": 0.95,
        "val_ratio": 0.05,
        "processed_count": processed_count,
        "train_count": train_count,
        "val_count": val_count,
        "dropped_empty_count": dropped_empty_count,
        "dropped_duplicate_count": dropped_duplicate_count,
        "total_text_bytes": total_text_bytes,
        "train_text_bytes": train_text_bytes,
        "val_text_bytes": val_text_bytes,
        "processed_path": processed_path.relative_to(PROJECT_ROOT).as_posix(),
        "train_path": train_path.relative_to(PROJECT_ROOT).as_posix(),
        "val_path": val_path.relative_to(PROJECT_ROOT).as_posix(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(intake_summary_path, summary)

    print(f"processed_count={processed_count}")
    print(f"train_count={train_count}")
    print(f"val_count={val_count}")
    print(f"dropped_empty_count={dropped_empty_count}")
    print(f"dropped_duplicate_count={dropped_duplicate_count}")
    print(f"total_text_bytes={total_text_bytes}")
    print(f"train_text_bytes={train_text_bytes}")
    print(f"val_text_bytes={val_text_bytes}")
    print(f"processed_path={summary['processed_path']}")
    print(f"train_path={summary['train_path']}")
    print(f"val_path={summary['val_path']}")
    print(f"intake_summary_path={intake_summary_path.relative_to(PROJECT_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
