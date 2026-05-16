from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from validate_draft_corpus_batch_03 import (
    BATCH_ROOT,
    EXPECTED_CATEGORY_TO_WORKER,
    EXPECTED_MARKDOWN_METADATA,
    EXPECTED_PYTHON_METADATA,
    FRAMEWORK_DIR,
    PROJECT_ROOT,
    REGISTRY_PATH,
    classify_secret_hits,
    file_type_to_suffix,
    normalize_worker_id,
    parse_jsonl_registry,
    read_metadata,
)

MANIFEST_PATH = FRAMEWORK_DIR / "draft_review_manifest.jsonl"
SUMMARY_PATH = FRAMEWORK_DIR / "draft_review_summary.json"
EXPECTED_REGISTRY_ROWS = 120
MIN_RECOMMENDED_LINES = 20
MAX_RECOMMENDED_LINES = 160
SOFT_MIN_LINES = 16
SOFT_MAX_LINES = 180
REVIEW_STATE_APPROVED = "approved_for_promotion_candidate"
REVIEW_STATE_NEEDS_EDIT = "needs_edit"
REVIEW_STATE_REJECTED = "rejected"


def parse_metadata_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    lowered = value.strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return None


def count_lines_and_chars(text: str) -> tuple[int, int]:
    return len(text.splitlines()), len(text)


def classify_length_status(line_count: int, char_count: int) -> str:
    if char_count == 0 or line_count == 0:
        return "empty"
    if MIN_RECOMMENDED_LINES <= line_count <= MAX_RECOMMENDED_LINES:
        return "within_range"
    if SOFT_MIN_LINES <= line_count < MIN_RECOMMENDED_LINES:
        return "slightly_short"
    if MAX_RECOMMENDED_LINES < line_count <= SOFT_MAX_LINES:
        return "slightly_long"
    if line_count < SOFT_MIN_LINES:
        return "too_short"
    return "too_long"


def duplicate_title_status_for(title_count: int, filename_count: int) -> str:
    if title_count > 1 and filename_count > 1:
        return "duplicate_title_and_proposed_filename"
    if title_count > 1:
        return "duplicate_title"
    if filename_count > 1:
        return "duplicate_proposed_filename"
    return "unique"


def expected_metadata_for(file_type: str) -> dict[str, str]:
    if file_type == "markdown":
        return EXPECTED_MARKDOWN_METADATA
    return EXPECTED_PYTHON_METADATA


def review_record_for_row(
    row: dict[str, Any],
    topic_id_counts: Counter[str],
    filename_counts: Counter[str],
    title_counts: Counter[str],
) -> dict[str, Any]:
    topic_id = str(row.get("topic_id", ""))
    category = str(row.get("category", ""))
    subcategory = str(row.get("subcategory", ""))
    proposed_filename = str(row.get("proposed_filename", ""))
    file_type = str(row.get("file_type", ""))
    title = str(row.get("title", ""))
    registry_worker = normalize_worker_id(str(row.get("worker_id", "")))
    expected_worker = EXPECTED_CATEGORY_TO_WORKER.get(category)

    expected_path = BATCH_ROOT / category / subcategory / proposed_filename
    relative_path = expected_path.relative_to(PROJECT_ROOT).as_posix()

    metadata_ok = False
    topic_id_ok = False
    worker_scope_ok = False
    approved_for_training_in_file: bool | None = None
    contains_external_text_in_file: bool | None = None
    contains_private_data_in_file: bool | None = None
    line_count = 0
    char_count = 0
    secret_scan_result = "missing"
    length_status = "empty"
    duplicate_title_status = duplicate_title_status_for(
        title_counts[title],
        filename_counts[proposed_filename],
    )
    review_notes: list[str] = []

    if expected_worker is None:
        review_notes.append(f"unknown category: {category}")
    if file_type not in {"markdown", "python"}:
        review_notes.append(f"unsupported file_type: {file_type}")
    else:
        expected_suffix = file_type_to_suffix(file_type)
        if not proposed_filename.endswith(expected_suffix):
            review_notes.append(
                f"registry file_type mismatch: expected suffix {expected_suffix} for {proposed_filename}"
            )

    if not expected_path.exists():
        review_notes.append(f"missing file: {relative_path}")
    else:
        text = expected_path.read_text(encoding="utf-8")
        line_count, char_count = count_lines_and_chars(text)
        length_status = classify_length_status(line_count, char_count)

        metadata, metadata_parse_error = read_metadata(expected_path, file_type if file_type in {"markdown", "python"} else "markdown")
        if metadata_parse_error is not None:
            review_notes.append(metadata_parse_error)
        else:
            expected_metadata = expected_metadata_for(file_type)
            metadata_mismatches: list[str] = []
            for key, expected_value in expected_metadata.items():
                actual_value = metadata.get(key)
                if actual_value is None:
                    metadata_mismatches.append(f"missing metadata field {key}")
                    continue
                if actual_value.strip().lower() != expected_value:
                    metadata_mismatches.append(
                        f"expected {key}={expected_value}, found {actual_value}"
                    )

            if metadata_mismatches:
                review_notes.extend(metadata_mismatches)
            else:
                metadata_ok = True

            actual_topic_id = metadata.get("topic_id")
            topic_id_ok = actual_topic_id == topic_id and topic_id_counts[topic_id] == 1
            if actual_topic_id != topic_id:
                review_notes.append(f"topic_id mismatch: {actual_topic_id} vs {topic_id}")
            if topic_id_counts[topic_id] > 1:
                review_notes.append(f"duplicate topic_id in registry: {topic_id}")

            metadata_worker = normalize_worker_id(metadata.get("worker_id"))
            worker_scope_ok = (
                expected_worker is not None
                and registry_worker == expected_worker
                and metadata_worker == expected_worker
            )
            if registry_worker != expected_worker:
                review_notes.append(
                    f"registry worker/category mismatch: {registry_worker} vs {expected_worker}"
                )
            if metadata_worker != expected_worker:
                review_notes.append(
                    f"file metadata worker mismatch: {metadata_worker} vs {expected_worker}"
                )

            approved_for_training_in_file = parse_metadata_bool(metadata.get("approved_for_training"))
            contains_external_text_in_file = parse_metadata_bool(metadata.get("contains_external_text"))
            contains_private_data_in_file = parse_metadata_bool(metadata.get("contains_private_data"))

            if approved_for_training_in_file is not False:
                review_notes.append("approved_for_training_in_file is not false")
            if contains_external_text_in_file is not False:
                review_notes.append("contains_external_text_in_file is not false")
            if contains_private_data_in_file is not False:
                review_notes.append("contains_private_data_in_file is not false")

        explanatory_hits, credential_hits = classify_secret_hits(expected_path, text)
        if credential_hits:
            secret_scan_result = "credential-style"
            review_notes.append("credential-style secret hit detected")
        elif explanatory_hits:
            secret_scan_result = "explanatory-only"
        else:
            secret_scan_result = "passed"

    if filename_counts[proposed_filename] > 1:
        review_notes.append(f"duplicate proposed_filename in registry: {proposed_filename}")
    if duplicate_title_status == "duplicate_title":
        review_notes.append(f"duplicate title in registry: {title}")
    elif duplicate_title_status == "duplicate_title_and_proposed_filename":
        review_notes.append(f"duplicate title and proposed_filename in registry: {title}")

    hard_fail = False
    if not metadata_ok:
        hard_fail = True
    if not topic_id_ok:
        hard_fail = True
    if not worker_scope_ok:
        hard_fail = True
    if approved_for_training_in_file is not False:
        hard_fail = True
    if contains_external_text_in_file is not False:
        hard_fail = True
    if contains_private_data_in_file is not False:
        hard_fail = True
    if secret_scan_result == "credential-style":
        hard_fail = True
    if char_count == 0 or line_count == 0:
        hard_fail = True
    if topic_id_counts[topic_id] > 1:
        hard_fail = True
    if length_status in {"too_short", "too_long", "empty"}:
        hard_fail = True

    soft_note = False
    if filename_counts[proposed_filename] > 1:
        soft_note = True
    if duplicate_title_status in {"duplicate_title", "duplicate_title_and_proposed_filename"}:
        soft_note = True
    if length_status in {"slightly_short", "slightly_long"}:
        soft_note = True
        review_notes.append(f"line count requires manual review: {line_count} lines ({length_status})")

    if hard_fail:
        review_state = REVIEW_STATE_REJECTED
    elif soft_note:
        review_state = REVIEW_STATE_NEEDS_EDIT
    else:
        review_state = REVIEW_STATE_APPROVED

    return {
        "topic_id": topic_id,
        "worker_id": expected_worker,
        "category": category,
        "subcategory": subcategory,
        "title": title,
        "file_path": relative_path,
        "file_type": file_type,
        "line_count": line_count,
        "char_count": char_count,
        "metadata_ok": metadata_ok,
        "topic_id_ok": topic_id_ok,
        "worker_scope_ok": worker_scope_ok,
        "approved_for_training_in_file": approved_for_training_in_file,
        "contains_external_text_in_file": contains_external_text_in_file,
        "contains_private_data_in_file": contains_private_data_in_file,
        "secret_scan_result": secret_scan_result,
        "length_status": length_status,
        "duplicate_title_status": duplicate_title_status,
        "review_state": review_state,
        "review_notes": review_notes,
    }


def build_summary(records: list[dict[str, Any]], registry_rows: list[dict[str, Any]]) -> dict[str, Any]:
    worker_counts = Counter(record["worker_id"] for record in records)
    file_type_counts = Counter(record["file_type"] for record in records)
    line_counts = [record["line_count"] for record in records]
    state_counts = Counter(record["review_state"] for record in records)
    review_state_by_worker: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        review_state_by_worker[record["worker_id"]][record["review_state"]] += 1

    secret_scan_summary = Counter(record["secret_scan_result"] for record in records)
    topic_id_counts = Counter(str(row.get("topic_id", "")) for row in registry_rows)
    filename_counts = Counter(str(row.get("proposed_filename", "")) for row in registry_rows)
    duplicate_topic_count = sum(1 for count in topic_id_counts.values() if count > 1)
    duplicate_filename_count = sum(1 for count in filename_counts.values() if count > 1)

    approved_count = state_counts[REVIEW_STATE_APPROVED]
    needs_edit_count = state_counts[REVIEW_STATE_NEEDS_EDIT]
    rejected_count = state_counts[REVIEW_STATE_REJECTED]
    total_records = len(records)

    if rejected_count > 0 or total_records != EXPECTED_REGISTRY_ROWS:
        review_gate_status = "failed"
    elif approved_count == EXPECTED_REGISTRY_ROWS:
        review_gate_status = "passed"
    elif needs_edit_count > 0:
        review_gate_status = "passed_with_notes"
    else:
        review_gate_status = "failed"

    return {
        "registry_path": REGISTRY_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "total_records": total_records,
        "approved_for_promotion_candidate_count": approved_count,
        "needs_edit_count": needs_edit_count,
        "rejected_count": rejected_count,
        "worker_counts": dict(sorted(worker_counts.items())),
        "review_state_by_worker": {
            worker_id: dict(sorted(counter.items()))
            for worker_id, counter in sorted(review_state_by_worker.items())
        },
        "file_type_counts": dict(sorted(file_type_counts.items())),
        "line_count_min": min(line_counts) if line_counts else 0,
        "line_count_max": max(line_counts) if line_counts else 0,
        "line_count_mean": round(mean(line_counts), 2) if line_counts else 0.0,
        "secret_scan_summary": dict(sorted(secret_scan_summary.items())),
        "duplicate_topic_count": duplicate_topic_count,
        "duplicate_filename_count": duplicate_filename_count,
        "review_gate_status": review_gate_status,
    }


def main() -> int:
    registry_rows, registry_errors = parse_jsonl_registry(REGISTRY_PATH)
    topic_id_counts = Counter(str(row.get("topic_id", "")) for row in registry_rows)
    filename_counts = Counter(str(row.get("proposed_filename", "")) for row in registry_rows)
    title_counts = Counter(str(row.get("title", "")) for row in registry_rows)

    records = [
        review_record_for_row(row, topic_id_counts, filename_counts, title_counts)
        for row in registry_rows
    ]

    MANIFEST_PATH.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )

    summary = build_summary(records, registry_rows)
    summary["registry_errors"] = registry_errors
    summary["registry_row_count"] = len(registry_rows)
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"total_records={summary['total_records']}")
    print(
        "approved_for_promotion_candidate="
        f"{summary['approved_for_promotion_candidate_count']}"
    )
    print(f"needs_edit={summary['needs_edit_count']}")
    print(f"rejected={summary['rejected_count']}")
    print(f"review_gate_status={summary['review_gate_status']}")
    print(
        "secret_scan_result="
        f"{json.dumps(summary['secret_scan_summary'], ensure_ascii=False, sort_keys=True)}"
    )

    return 0 if summary["review_gate_status"] != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
