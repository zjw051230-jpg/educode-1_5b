from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "data" / "fineweb_edu_sample10bt_50mb.json"
DEFAULT_MAX_RECORDS = 3
DEFAULT_TIMEOUT_SECONDS = 60
DEFAULT_RETRIES = 2
DEFAULT_RETRY_SLEEP_SECONDS = 2.0
PREVIEW_CHAR_LIMIT = 300


def read_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_repo_path(path_text: str) -> Path:
    return PROJECT_ROOT / Path(path_text)


def remove_if_exists(path: Path) -> None:
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def classify_fetch_error(exc: Exception) -> dict[str, str]:
    text = str(exc)
    lower = text.lower()
    if "ssl" in lower or "unexpected eof" in lower:
        category = "ssl_connection_error"
    elif "client has been closed" in lower:
        category = "http_client_closed"
    elif "timed out" in lower or "timeout" in lower:
        category = "timeout_error"
    elif "huggingface" in lower or "hf hub" in lower:
        category = "hf_connection_error"
    else:
        category = "streaming_fetch_error"

    return {
        "error_type": type(exc).__name__,
        "error_category": category,
        "error_message": text,
    }


def print_retry_message(attempt: int, total_attempts: int, exc: Exception) -> None:
    print(
        f"attempt={attempt}/{total_attempts} "
        f"exception_type={type(exc).__name__} "
        f"message={exc}"
    )


def print_failure_guidance() -> None:
    print("suggestion_1=retry later")
    print("suggestion_2=provide HF_TOKEN if rate_or_connection_issue_persists")
    print("suggestion_3=try alternative public corpus")
    print("suggestion_4=run fetch on A100/Linux instead of Windows network")


def iter_streaming_records(config: dict[str, Any], timeout_seconds: int):
    os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", str(timeout_seconds))
    os.environ.setdefault("HF_HUB_ETAG_TIMEOUT", str(timeout_seconds))

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


def build_preview_payload(
    config: dict[str, Any],
    record_count: int,
    first_text_preview: str,
    error: dict[str, str] | None,
) -> dict[str, Any]:
    return {
        "record_count": record_count,
        "text_field": config["text_field"],
        "first_text_chars_preview": first_text_preview[:PREVIEW_CHAR_LIMIT],
        "dataset_id": config["dataset_id"],
        "dataset_config": config["dataset_config"],
        "split": config["split"],
        "error": error,
    }


def write_preview(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_dry_run(
    config: dict[str, Any],
    max_records: int,
    timeout_seconds: int,
    retries: int,
    retry_sleep_seconds: float,
    preview_output: Path | None,
) -> int:
    total_attempts = retries + 1
    last_error: dict[str, str] | None = None

    for attempt in range(1, total_attempts + 1):
        record_count = 0
        accumulated_bytes = 0
        first_text_preview = ""
        try:
            iterator = iter_streaming_records(config, timeout_seconds)
            for _ in range(max_records):
                record = next(iterator)
                text = str(record.get(config["text_field"], ""))
                if record_count == 0:
                    first_text_preview = text[:PREVIEW_CHAR_LIMIT]
                accumulated_bytes += len(text.encode("utf-8"))
                record_count += 1

            preview_payload = build_preview_payload(config, record_count, first_text_preview, None)
            if preview_output is not None:
                write_preview(preview_output, preview_payload)

            print("dry_run=true")
            print(f"record_count={record_count}")
            print(f"size_mb={accumulated_bytes / (1024 * 1024):.6f}")
            print(f"output_path={config['output_jsonl']}")
            if preview_output is not None:
                print(f"preview_output={preview_output.relative_to(PROJECT_ROOT).as_posix()}")
            return 0
        except Exception as exc:
            last_error = classify_fetch_error(exc)
            print_retry_message(attempt, total_attempts, exc)
            if attempt < total_attempts:
                time.sleep(retry_sleep_seconds)
                continue

    preview_payload = build_preview_payload(config, 0, "", last_error)
    if preview_output is not None:
        write_preview(preview_output, preview_payload)

    print("dry_run=true")
    print("record_count=0")
    print("size_mb=0.000000")
    if preview_output is not None:
        print(f"preview_output={preview_output.relative_to(PROJECT_ROOT).as_posix()}")
    if last_error is not None:
        print(f"error_type={last_error['error_type']}")
        print(f"error_category={last_error['error_category']}")
        print(f"error_message={last_error['error_message']}")
    print_failure_guidance()
    return 1


def run_fetch(config: dict[str, Any], timeout_seconds: int) -> int:
    output_dir = resolve_repo_path(config["output_dir"])
    output_jsonl = resolve_repo_path(config["output_jsonl"])
    manifest_path = resolve_repo_path(config["manifest_path"])
    output_dir.mkdir(parents=True, exist_ok=True)

    target_size_bytes = int(config["target_size_mb"]) * 1024 * 1024
    iterator = iter_streaming_records(config, timeout_seconds)
    record_count = 0
    accumulated_bytes = 0

    temp_dir = Path(tempfile.mkdtemp(prefix="fineweb_edu_", dir=output_dir))
    temp_output = temp_dir / "raw.jsonl"
    try:
        with temp_output.open("w", encoding="utf-8") as handle:
            while accumulated_bytes < target_size_bytes:
                record = next(iterator)
                text = str(record.get(config["text_field"], ""))
                text_bytes = len(text.encode("utf-8"))
                handle.write(json.dumps({config["text_field"]: text}, ensure_ascii=False) + "\n")
                accumulated_bytes += text_bytes
                record_count += 1

        temp_output.replace(output_jsonl)
        manifest = build_manifest(config, accumulated_bytes, record_count)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        print("dry_run=false")
        print(f"record_count={record_count}")
        print(f"size_mb={accumulated_bytes / (1024 * 1024):.6f}")
        print(f"output_path={output_jsonl.relative_to(PROJECT_ROOT).as_posix()}")
        return 0
    except Exception:
        remove_if_exists(temp_output)
        raise
    finally:
        remove_if_exists(temp_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch a bounded FineWeb-Edu streaming slice.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the fetch config JSON.")
    parser.add_argument("--dry-run", action="store_true", help="Read a few records without writing a large output file.")
    parser.add_argument("--max-records", type=int, default=DEFAULT_MAX_RECORDS, help="Maximum records to inspect in dry-run mode.")
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="HF request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES, help="Number of dry-run retries after the first attempt.")
    parser.add_argument(
        "--retry-sleep-seconds",
        type=float,
        default=DEFAULT_RETRY_SLEEP_SECONDS,
        help="Sleep duration between retry attempts.",
    )
    parser.add_argument(
        "--preview-output",
        default="",
        help="Optional repo-relative preview JSON written during dry-run.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    config = read_config(config_path)
    preview_output = resolve_repo_path(args.preview_output) if args.preview_output else None
    if args.dry_run:
        return run_dry_run(
            config,
            max_records=args.max_records,
            timeout_seconds=args.timeout_seconds,
            retries=args.retries,
            retry_sleep_seconds=args.retry_sleep_seconds,
            preview_output=preview_output,
        )
    return run_fetch(config, timeout_seconds=args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
