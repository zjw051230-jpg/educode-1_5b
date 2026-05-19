from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from validate_draft_corpus_batch_03 import (
    PROJECT_ROOT,
    classify_secret_hits,
    normalize_worker_id,
    parse_jsonl_registry,
    read_metadata,
)

BATCH_ROOT = PROJECT_ROOT / "data" / "real_corpus" / "draft_queue" / "domain_synthetic_batch_04"
SUMMARY_PATH = BATCH_ROOT / "batch_04_validation_summary.json"
MANIFEST_PATH = BATCH_ROOT / "batch_04_validation_manifest.jsonl"

WORKER_SPECS = {
    "cc1_ml_foundations": {
        "worker_id": "CC-1",
        "expected_total": 1000,
        "expected_markdown": 700,
        "expected_python": 300,
    },
    "cc2_python_data_systems": {
        "worker_id": "CC-2",
        "expected_total": 1000,
        "expected_markdown": 700,
        "expected_python": 300,
    },
    "cc3_transformer_architecture": {
        "worker_id": "CC-3",
        "expected_total": 1000,
        "expected_markdown": 700,
        "expected_python": 300,
    },
    "cc4_training_runtime_systems": {
        "worker_id": "CC-4",
        "expected_total": 1000,
        "expected_markdown": 700,
        "expected_python": 300,
    },
    "cc5_bilingual_qa": {
        "worker_id": "CC-5",
        "expected_total": 1000,
        "expected_markdown": 850,
        "expected_python": 150,
    },
    "cc6_code_snippets": {
        "worker_id": "CC-6",
        "expected_total": 1000,
        "expected_markdown": 300,
        "expected_python": 700,
    },
}
EXPECTED_TOTAL_TOPIC_FILES = sum(spec["expected_total"] for spec in WORKER_SPECS.values())
EXPECTED_TOTAL_MARKDOWN = sum(spec["expected_markdown"] for spec in WORKER_SPECS.values())
EXPECTED_TOTAL_PYTHON = sum(spec["expected_python"] for spec in WORKER_SPECS.values())
EXPECTED_BATCH_ID = "domain_synthetic_batch_04"
EXPECTED_MARKDOWN_METADATA = {
    "draft_status": "candidate",
    "source_category": "synthetic_examples",
    "project_backbone": "cs_ml_python_transformer_training_systems",
    "approved_for_training": "false",
    "contains_external_text": "false",
    "contains_private_data": "false",
    "target_use": "draft_review_only",
    "batch_id": EXPECTED_BATCH_ID,
}
EXPECTED_PYTHON_METADATA = EXPECTED_MARKDOWN_METADATA.copy()
ALLOWED_BATCH_OUTPUT_FILES = {
    "batch_04_validation_summary.json",
    "batch_04_validation_manifest.jsonl",
    "batch_04_quality_review_summary.json",
    "batch_04_quality_review_manifest.jsonl",
}
ALLOWED_GIT_STATUS_PATHS = {
    "README.md",
    "docs/experiment_index.md",
    "docs/d18_batch_04_draft_corpus_validation_review.md",
    "docs/d18_batch_04_worker_aggregation_summary.md",
    "docs/d18_batch_04_human_sampling_plan.md",
    "scripts/validate_draft_corpus_batch_04.py",
    "scripts/review_draft_corpus_quality_batch_04.py",
}
ALLOWED_GIT_STATUS_PREFIXES = (
    BATCH_ROOT.relative_to(PROJECT_ROOT).as_posix() + "/",
)
SUMMARY_EXPECTED_KEYS = {
    "worker_id",
    "target_count",
    "generated_count",
    "markdown_count",
    "python_count",
}


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


def normalize_file_type(value: Any, path_hint: str | None = None) -> str | None:
    text = str(value or "").strip().lower()
    mapping = {
        "markdown": "markdown",
        "md": "markdown",
        ".md": "markdown",
        "python": "python",
        "py": "python",
        ".py": "python",
    }
    if text in mapping:
        return mapping[text]
    if path_hint is not None:
        suffix = Path(path_hint).suffix.lower()
        if suffix == ".md":
            return "markdown"
        if suffix == ".py":
            return "python"
    return None


def file_type_to_suffix(file_type: str) -> str:
    if file_type == "markdown":
        return ".md"
    return ".py"


def expected_metadata_for(file_type: str) -> dict[str, str]:
    if file_type == "markdown":
        return EXPECTED_MARKDOWN_METADATA
    return EXPECTED_PYTHON_METADATA


def parse_git_status_lines() -> tuple[list[dict[str, str]], list[str]]:
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as exc:
        return [], [f"git status failed: {exc.stderr.strip() or exc.stdout.strip() or exc}"]

    entries: list[dict[str, str]] = []
    errors: list[str] = []
    for raw_line in result.stdout.splitlines():
        if not raw_line.strip():
            continue
        if len(raw_line) < 4:
            errors.append(f"unable to parse git status line: {raw_line}")
            continue
        status_code = raw_line[:2]
        path_text = raw_line[3:]
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        normalized_path = path_text.replace("\\", "/")
        entries.append({"status": status_code, "path": normalized_path})
    return entries, errors


def is_allowed_git_status_path(path_text: str) -> bool:
    return path_text in ALLOWED_GIT_STATUS_PATHS or path_text.startswith(ALLOWED_GIT_STATUS_PREFIXES)


def is_explanatory_support_secret_hit(hit: dict[str, Any]) -> bool:
    context = str(hit.get("context", "")).lower()
    file_path = str(hit.get("file", ""))
    if "/batch_summary.md" in file_path and "no matches for api_key" in context:
        return True
    if "/progress_" in file_path and "secret-scan status" in context:
        return True
    return False


def normalize_support_secret_hits(
    explanatory_hits: list[dict[str, Any]],
    credential_hits: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    normalized_explanatory = list(explanatory_hits)
    normalized_credential: list[dict[str, Any]] = []
    for hit in credential_hits:
        if is_explanatory_support_secret_hit(hit):
            normalized_hit = dict(hit)
            normalized_hit["classification"] = "explanatory-only"
            normalized_explanatory.append(normalized_hit)
            continue
        normalized_credential.append(hit)
    return normalized_explanatory, normalized_credential


def parse_summary_value_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped.startswith("-"):
        return None
    body = stripped[1:].strip()
    if ":" not in body:
        return None
    key, value = body.split(":", 1)
    return key.strip(), value.strip()


def parse_batch_summary_counts(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        parsed = parse_summary_value_line(line)
        if parsed is None:
            continue
        key, value = parsed
        if key in SUMMARY_EXPECTED_KEYS and key not in values:
            values[key] = value
    return values


def first_present_str(row: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = row.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return None


def normalize_relative_path(category: str, row: dict[str, Any], notes: list[str]) -> Path | None:
    raw_path = first_present_str(row, "relative_path", "path", "filename")
    raw_filename = first_present_str(row, "proposed_filename", "filename")
    subcategory = first_present_str(row, "subcategory", "subdir", "subdirectory")
    worker_root = BATCH_ROOT / category

    if raw_path is not None:
        normalized = raw_path.replace("\\", "/")
        if normalized.startswith(BATCH_ROOT.relative_to(PROJECT_ROOT).as_posix() + "/"):
            return Path(normalized)
        if normalized.startswith(category + "/"):
            return (BATCH_ROOT / normalized).relative_to(PROJECT_ROOT)
        if "/" in normalized:
            return (worker_root / normalized).relative_to(PROJECT_ROOT)

    if raw_filename is not None and subcategory is not None:
        return (worker_root / subcategory / raw_filename).relative_to(PROJECT_ROOT)

    notes.append("unable to resolve file path from manifest row")
    return None


def normalize_manifest_row(category: str, row: dict[str, Any]) -> dict[str, Any]:
    notes: list[str] = []
    spec = WORKER_SPECS[category]
    expected_worker = spec["worker_id"]
    topic_id = str(row.get("topic_id", "")).strip()
    title = str(row.get("title", "")).strip()
    batch_id = str(row.get("batch_id", "")).strip() or None
    worker_id = normalize_worker_id(first_present_str(row, "worker_id") or expected_worker)
    subcategory = first_present_str(row, "subcategory", "subdir", "subdirectory") or ""
    relative_path = normalize_relative_path(category, row, notes)
    file_path_text = relative_path.as_posix() if relative_path is not None else ""
    proposed_filename = ""
    if relative_path is not None:
        proposed_filename = relative_path.name
    elif first_present_str(row, "proposed_filename", "filename") is not None:
        proposed_filename = Path(first_present_str(row, "proposed_filename", "filename") or "").name

    normalized_file_type = normalize_file_type(
        row.get("file_type"),
        file_path_text or proposed_filename,
    )
    if normalized_file_type is None:
        notes.append(f"unsupported manifest file_type: {row.get('file_type')}")

    manifest_flag_errors: list[str] = []
    approved_for_training = row.get("approved_for_training")
    if approved_for_training is not None and approved_for_training is not False:
        manifest_flag_errors.append("manifest approved_for_training is not false")

    contains_external_text = row.get("contains_external_text")
    if contains_external_text is not None and contains_external_text is not False:
        manifest_flag_errors.append("manifest contains_external_text is not false")

    contains_private_data = row.get("contains_private_data")
    if contains_private_data is not None and contains_private_data is not False:
        manifest_flag_errors.append("manifest contains_private_data is not false")

    target_use = first_present_str(row, "target_use")
    if target_use is not None and target_use != "draft_review_only":
        manifest_flag_errors.append(f"manifest target_use is not draft_review_only: {target_use}")

    if batch_id is not None and batch_id != EXPECTED_BATCH_ID:
        manifest_flag_errors.append(f"manifest batch_id mismatch: {batch_id}")

    notes.extend(manifest_flag_errors)

    return {
        "topic_id": topic_id,
        "worker_directory": category,
        "worker_id": worker_id,
        "expected_worker_id": expected_worker,
        "subcategory": subcategory,
        "title": title,
        "batch_id": batch_id,
        "file_type": normalized_file_type,
        "file_path": file_path_text,
        "proposed_filename": proposed_filename,
        "manifest_flag_errors": manifest_flag_errors,
        "normalization_notes": notes,
    }


def collect_worker_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    records: list[dict[str, Any]] = []
    summary: dict[str, Any] = {
        "registry_errors": [],
        "worker_manifest_paths": {},
        "batch_summary_paths": {},
        "progress_file_counts": {},
        "worker_summary_checks": {},
    }

    for category, spec in WORKER_SPECS.items():
        worker_root = BATCH_ROOT / category
        manifest_path = worker_root / "worker_topic_manifest.jsonl"
        summary["worker_manifest_paths"][category] = manifest_path.relative_to(PROJECT_ROOT).as_posix()
        summary["batch_summary_paths"][category] = (worker_root / "batch_summary.md").relative_to(PROJECT_ROOT).as_posix()

        progress_files = sorted(
            path.relative_to(PROJECT_ROOT).as_posix()
            for path in worker_root.glob("progress*.md")
            if path.is_file()
        )
        summary["progress_file_counts"][category] = len(progress_files)

        batch_summary_path = worker_root / "batch_summary.md"
        batch_summary_values: dict[str, str] = {}
        batch_summary_errors: list[str] = []
        if not batch_summary_path.exists():
            batch_summary_errors.append("missing batch_summary.md")
        else:
            batch_summary_values = parse_batch_summary_counts(batch_summary_path)
            expected_summary_values = {
                "worker_id": spec["worker_id"],
                "target_count": str(spec["expected_total"]),
                "generated_count": str(spec["expected_total"]),
                "markdown_count": str(spec["expected_markdown"]),
                "python_count": str(spec["expected_python"]),
            }
            for key, expected_value in expected_summary_values.items():
                actual_value = batch_summary_values.get(key)
                if actual_value is None:
                    batch_summary_errors.append(f"batch_summary missing {key}")
                elif actual_value != expected_value:
                    batch_summary_errors.append(
                        f"batch_summary {key} mismatch: expected {expected_value}, found {actual_value}"
                    )

        if len(progress_files) != 10:
            batch_summary_errors.append(f"expected 10 progress files, found {len(progress_files)}")

        summary["worker_summary_checks"][category] = {
            "worker_id": spec["worker_id"],
            "batch_summary_values": batch_summary_values,
            "batch_summary_errors": batch_summary_errors,
            "progress_file_count": len(progress_files),
            "progress_files": progress_files,
        }

        if not manifest_path.exists():
            summary["registry_errors"].append(f"missing worker manifest: {manifest_path.relative_to(PROJECT_ROOT).as_posix()}")
            continue

        rows, errors = parse_jsonl_registry(manifest_path)
        if errors:
            summary["registry_errors"].extend(
                f"{manifest_path.relative_to(PROJECT_ROOT).as_posix()}: {error}"
                for error in errors
            )

        for row in rows:
            normalized = normalize_manifest_row(category, row)
            normalized["manifest_path"] = manifest_path.relative_to(PROJECT_ROOT).as_posix()
            records.append(normalized)

    return records, summary


def build_validation_records(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    records: list[dict[str, Any]] = []
    line_counts: list[int] = []
    char_counts: list[int] = []
    explanatory_secret_hits: list[dict[str, Any]] = []
    credential_secret_hits: list[dict[str, Any]] = []
    metadata_errors: list[str] = []
    missing_files: list[str] = []
    scope_errors: list[str] = []
    duplicate_topic_ids = Counter(row["topic_id"] for row in rows if row["topic_id"])
    duplicate_file_paths = Counter(row["file_path"] for row in rows if row["file_path"])
    worker_manifest_counts = Counter(row["worker_id"] for row in rows)
    worker_manifest_file_type_counts: dict[str, Counter[str]] = defaultdict(Counter)
    worker_disk_file_type_counts: dict[str, Counter[str]] = defaultdict(Counter)
    disk_files_seen: set[Path] = set()

    for row in rows:
        topic_id = row["topic_id"]
        worker_id = row["worker_id"]
        expected_worker_id = row["expected_worker_id"]
        file_type = row["file_type"]
        file_path_text = row["file_path"]
        notes = list(row["normalization_notes"])
        manifest_row_ok = True

        if not topic_id:
            notes.append("missing topic_id in manifest row")
            manifest_row_ok = False
        if not row["subcategory"]:
            notes.append("missing subcategory in manifest row")
            manifest_row_ok = False
        if not row["title"]:
            notes.append("missing title in manifest row")
            manifest_row_ok = False
        if worker_id != expected_worker_id:
            notes.append(f"manifest worker mismatch: {worker_id} vs {expected_worker_id}")
            manifest_row_ok = False
        if file_type is None:
            manifest_row_ok = False
        if row["manifest_flag_errors"]:
            manifest_row_ok = False
        if duplicate_topic_ids[topic_id] > 1:
            notes.append(f"duplicate topic_id across worker manifests: {topic_id}")
            manifest_row_ok = False
        if file_path_text and duplicate_file_paths[file_path_text] > 1:
            notes.append(f"duplicate file_path across worker manifests: {file_path_text}")
            manifest_row_ok = False

        if file_type is not None:
            worker_manifest_file_type_counts[expected_worker_id][file_type] += 1

        metadata_ok = False
        topic_id_ok = False
        worker_scope_ok = False
        approved_for_training_in_file: bool | None = None
        contains_external_text_in_file: bool | None = None
        contains_private_data_in_file: bool | None = None
        line_count = 0
        char_count = 0
        secret_scan_result = "missing"
        file_exists = False

        file_path = PROJECT_ROOT / file_path_text if file_path_text else None
        if file_path is None:
            notes.append("missing file path after normalization")
        else:
            expected_worker_root = BATCH_ROOT / row["worker_directory"]
            try:
                file_path.relative_to(expected_worker_root)
            except ValueError:
                notes.append(f"file path escaped worker directory: {file_path_text}")
                scope_errors.append(f"file path escaped worker directory: {file_path_text}")
                manifest_row_ok = False

            if not file_path.exists():
                missing_files.append(file_path_text)
                notes.append(f"missing file: {file_path_text}")
            else:
                file_exists = True
                disk_files_seen.add(file_path)
                text = file_path.read_text(encoding="utf-8")
                line_count, char_count = count_lines_and_chars(text)
                line_counts.append(line_count)
                char_counts.append(char_count)

                if file_type is None:
                    notes.append("cannot parse file metadata without normalized file_type")
                else:
                    expected_suffix = file_type_to_suffix(file_type)
                    if file_path.suffix.lower() != expected_suffix:
                        notes.append(
                            f"file suffix mismatch: expected {expected_suffix}, found {file_path.suffix.lower()}"
                        )
                        manifest_row_ok = False

                    metadata, metadata_parse_error = read_metadata(file_path, file_type)
                    if metadata_parse_error is not None:
                        notes.append(metadata_parse_error)
                        metadata_errors.append(f"{file_path_text}: {metadata_parse_error}")
                    else:
                        expected_metadata = expected_metadata_for(file_type)
                        mismatches: list[str] = []
                        for key, expected_value in expected_metadata.items():
                            actual_value = metadata.get(key)
                            if actual_value is None:
                                mismatches.append(f"missing metadata field {key}")
                                continue
                            if actual_value.strip().lower() != expected_value:
                                mismatches.append(
                                    f"expected {key}={expected_value}, found {actual_value}"
                                )

                        if mismatches:
                            notes.extend(mismatches)
                            metadata_errors.extend(f"{file_path_text}: {item}" for item in mismatches)
                        else:
                            metadata_ok = True

                        actual_topic_id = metadata.get("topic_id")
                        topic_id_ok = actual_topic_id == topic_id and duplicate_topic_ids[topic_id] == 1
                        if actual_topic_id != topic_id:
                            notes.append(f"topic_id mismatch: {actual_topic_id} vs {topic_id}")
                            metadata_errors.append(
                                f"{file_path_text}: topic_id mismatch ({actual_topic_id} vs {topic_id})"
                            )

                        metadata_worker = normalize_worker_id(metadata.get("worker_id"))
                        worker_scope_ok = metadata_worker == expected_worker_id
                        if metadata_worker != expected_worker_id:
                            notes.append(f"file metadata worker mismatch: {metadata_worker} vs {expected_worker_id}")
                            metadata_errors.append(
                                f"{file_path_text}: worker_id mismatch ({metadata_worker} vs {expected_worker_id})"
                            )

                        approved_for_training_in_file = parse_metadata_bool(metadata.get("approved_for_training"))
                        contains_external_text_in_file = parse_metadata_bool(metadata.get("contains_external_text"))
                        contains_private_data_in_file = parse_metadata_bool(metadata.get("contains_private_data"))
                        if approved_for_training_in_file is not False:
                            notes.append("approved_for_training_in_file is not false")
                        if contains_external_text_in_file is not False:
                            notes.append("contains_external_text_in_file is not false")
                        if contains_private_data_in_file is not False:
                            notes.append("contains_private_data_in_file is not false")

                explanatory_hits, credential_hits = classify_secret_hits(file_path, text)
                explanatory_secret_hits.extend(explanatory_hits)
                credential_secret_hits.extend(credential_hits)
                if credential_hits:
                    secret_scan_result = "credential-style"
                    notes.append("credential-style secret hit detected")
                elif explanatory_hits:
                    secret_scan_result = "explanatory-only"
                else:
                    secret_scan_result = "passed"

                if file_type is not None:
                    worker_disk_file_type_counts[expected_worker_id][file_type] += 1

        validation_ok = True
        if not manifest_row_ok:
            validation_ok = False
        if not file_exists:
            validation_ok = False
        if not metadata_ok:
            validation_ok = False
        if not topic_id_ok:
            validation_ok = False
        if not worker_scope_ok:
            validation_ok = False
        if approved_for_training_in_file is not False:
            validation_ok = False
        if contains_external_text_in_file is not False:
            validation_ok = False
        if contains_private_data_in_file is not False:
            validation_ok = False
        if secret_scan_result == "credential-style":
            validation_ok = False
        if char_count == 0 or line_count == 0:
            validation_ok = False
            if file_exists:
                notes.append("file is empty")

        records.append(
            {
                "topic_id": topic_id,
                "worker_id": expected_worker_id,
                "worker_directory": row["worker_directory"],
                "subcategory": row["subcategory"],
                "title": row["title"],
                "file_path": file_path_text,
                "file_type": file_type,
                "line_count": line_count,
                "char_count": char_count,
                "manifest_row_ok": manifest_row_ok,
                "metadata_ok": metadata_ok,
                "topic_id_ok": topic_id_ok,
                "worker_scope_ok": worker_scope_ok,
                "approved_for_training_in_file": approved_for_training_in_file,
                "contains_external_text_in_file": contains_external_text_in_file,
                "contains_private_data_in_file": contains_private_data_in_file,
                "secret_scan_result": secret_scan_result,
                "validation_status": "passed" if validation_ok else "failed",
                "validation_notes": notes,
            }
        )

    summary = {
        "line_counts": line_counts,
        "char_counts": char_counts,
        "metadata_errors": metadata_errors,
        "missing_files": missing_files,
        "scope_errors": scope_errors,
        "duplicate_topic_id_count": sum(1 for count in duplicate_topic_ids.values() if count > 1),
        "duplicate_file_path_count": sum(1 for count in duplicate_file_paths.values() if count > 1),
        "worker_manifest_counts": worker_manifest_counts,
        "worker_manifest_file_type_counts": worker_manifest_file_type_counts,
        "worker_disk_file_type_counts": worker_disk_file_type_counts,
        "disk_files_seen": disk_files_seen,
        "explanatory_secret_hits": explanatory_secret_hits,
        "credential_secret_hits": credential_secret_hits,
    }
    return records, summary


def scan_support_files() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    explanatory_hits: list[dict[str, Any]] = []
    credential_hits: list[dict[str, Any]] = []
    scope_errors: list[str] = []

    for category in WORKER_SPECS:
        worker_root = BATCH_ROOT / category
        if not worker_root.exists():
            scope_errors.append(f"missing worker directory: {worker_root.relative_to(PROJECT_ROOT).as_posix()}")
            continue

        support_files = [worker_root / "batch_summary.md", worker_root / "worker_topic_manifest.jsonl"]
        support_files.extend(
            path for path in worker_root.glob("progress*.md") if path.is_file()
        )
        for path in support_files:
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            explanatory, credential = classify_secret_hits(path, text)
            explanatory_hits.extend(explanatory)
            credential_hits.extend(credential)

    return explanatory_hits, credential_hits, scope_errors


def find_unexpected_files(expected_topic_files: set[Path]) -> list[str]:
    unexpected_files: list[str] = []

    for path in BATCH_ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(PROJECT_ROOT).as_posix()

        if path in expected_topic_files:
            continue
        if path.parent == BATCH_ROOT and path.name in ALLOWED_BATCH_OUTPUT_FILES:
            continue
        if path.name == "batch_summary.md":
            continue
        if path.name == "worker_topic_manifest.jsonl":
            continue
        if path.parent in {BATCH_ROOT / category for category in WORKER_SPECS} and path.name.startswith("progress") and path.suffix == ".md":
            continue

        unexpected_files.append(relative_path)

    return unexpected_files


def build_summary(
    rows: list[dict[str, Any]],
    records: list[dict[str, Any]],
    row_summary: dict[str, Any],
    validation_summary: dict[str, Any],
) -> dict[str, Any]:
    git_status_entries, git_status_errors = parse_git_status_lines()
    git_scope_errors = [
        f"out-of-scope git status path: {entry['status']} {entry['path']}"
        for entry in git_status_entries
        if not is_allowed_git_status_path(entry["path"])
    ]

    support_explanatory_hits, support_credential_hits, support_scope_errors = scan_support_files()
    support_explanatory_hits, support_credential_hits = normalize_support_secret_hits(
        support_explanatory_hits,
        support_credential_hits,
    )
    unexpected_files = find_unexpected_files(validation_summary["disk_files_seen"])

    state_counts = Counter(record["validation_status"] for record in records)
    file_type_counts = Counter(record["file_type"] for record in records if record["file_type"] is not None)
    worker_validation_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        worker_validation_counts[record["worker_id"]][record["validation_status"]] += 1

    worker_rollup: dict[str, Any] = {}
    for category, spec in WORKER_SPECS.items():
        worker_id = spec["worker_id"]
        worker_rollup[worker_id] = {
            "worker_directory": category,
            "expected_total": spec["expected_total"],
            "expected_markdown": spec["expected_markdown"],
            "expected_python": spec["expected_python"],
            "manifest_rows": validation_summary["worker_manifest_counts"].get(worker_id, 0),
            "manifest_markdown": validation_summary["worker_manifest_file_type_counts"].get(worker_id, Counter()).get("markdown", 0),
            "manifest_python": validation_summary["worker_manifest_file_type_counts"].get(worker_id, Counter()).get("python", 0),
            "disk_markdown": validation_summary["worker_disk_file_type_counts"].get(worker_id, Counter()).get("markdown", 0),
            "disk_python": validation_summary["worker_disk_file_type_counts"].get(worker_id, Counter()).get("python", 0),
            "progress_file_count": row_summary["progress_file_counts"].get(category, 0),
            "batch_summary_check": row_summary["worker_summary_checks"].get(category, {}),
            "validation_status_counts": dict(sorted(worker_validation_counts.get(worker_id, Counter()).items())),
        }

    all_registry_errors = list(row_summary["registry_errors"])
    all_registry_errors.extend(git_status_errors)

    metadata_errors = list(validation_summary["metadata_errors"])
    scope_errors = list(validation_summary["scope_errors"])
    scope_errors.extend(support_scope_errors)
    scope_errors.extend(unexpected_files)

    summary_secret_explanatory = list(validation_summary["explanatory_secret_hits"])
    summary_secret_explanatory.extend(support_explanatory_hits)
    summary_secret_credential = list(validation_summary["credential_secret_hits"])
    summary_secret_credential.extend(support_credential_hits)

    if summary_secret_credential:
        secret_scan_result = "failed"
    elif summary_secret_explanatory:
        secret_scan_result = "explanatory-only"
    else:
        secret_scan_result = "passed"

    validation_status = "passed"
    if (
        len(rows) != EXPECTED_TOTAL_TOPIC_FILES
        or len(records) != EXPECTED_TOTAL_TOPIC_FILES
        or state_counts.get("failed", 0) > 0
        or all_registry_errors
        or validation_summary["missing_files"]
        or metadata_errors
        or scope_errors
        or git_scope_errors
        or summary_secret_credential
        or file_type_counts.get("markdown", 0) != EXPECTED_TOTAL_MARKDOWN
        or file_type_counts.get("python", 0) != EXPECTED_TOTAL_PYTHON
    ):
        validation_status = "failed"

    return {
        "validation_status": validation_status,
        "batch_root": BATCH_ROOT.relative_to(PROJECT_ROOT).as_posix(),
        "total_manifest_rows": len(rows),
        "total_topic_files": len(records),
        "expected_total_topic_files": EXPECTED_TOTAL_TOPIC_FILES,
        "markdown_count": file_type_counts.get("markdown", 0),
        "python_count": file_type_counts.get("python", 0),
        "expected_markdown_count": EXPECTED_TOTAL_MARKDOWN,
        "expected_python_count": EXPECTED_TOTAL_PYTHON,
        "passed_record_count": state_counts.get("passed", 0),
        "failed_record_count": state_counts.get("failed", 0),
        "duplicate_topic_id_count": validation_summary["duplicate_topic_id_count"],
        "duplicate_file_path_count": validation_summary["duplicate_file_path_count"],
        "worker_rollup": worker_rollup,
        "registry_errors": all_registry_errors,
        "metadata_errors": metadata_errors,
        "metadata_errors_count": len(metadata_errors),
        "missing_files": validation_summary["missing_files"],
        "missing_files_count": len(validation_summary["missing_files"]),
        "scope_errors": scope_errors,
        "scope_errors_count": len(scope_errors),
        "unexpected_files": unexpected_files,
        "git_scope": {
            "checked_with_git_status": True,
            "allowed_exact_paths": sorted(ALLOWED_GIT_STATUS_PATHS),
            "allowed_prefixes": list(ALLOWED_GIT_STATUS_PREFIXES),
            "observed_entries": git_status_entries,
            "out_of_scope_errors": git_scope_errors,
            "out_of_scope_error_count": len(git_scope_errors),
        },
        "secret_scan": {
            "result": secret_scan_result,
            "explanatory_only_count": len(summary_secret_explanatory),
            "credential_style_count": len(summary_secret_credential),
            "explanatory_only_examples": summary_secret_explanatory[:20],
            "credential_style_examples": summary_secret_credential[:20],
        },
        "line_count_stats": {
            "min": min(validation_summary["line_counts"]) if validation_summary["line_counts"] else 0,
            "max": max(validation_summary["line_counts"]) if validation_summary["line_counts"] else 0,
            "mean": round(mean(validation_summary["line_counts"]), 2) if validation_summary["line_counts"] else 0.0,
        },
        "char_count_stats": {
            "min": min(validation_summary["char_counts"]) if validation_summary["char_counts"] else 0,
            "max": max(validation_summary["char_counts"]) if validation_summary["char_counts"] else 0,
            "mean": round(mean(validation_summary["char_counts"]), 2) if validation_summary["char_counts"] else 0.0,
        },
        "approval_state": {
            "all_records_approved_for_training_false": all(
                record["approved_for_training_in_file"] is False for record in records
            ),
            "all_records_contains_external_text_false": all(
                record["contains_external_text_in_file"] is False for record in records
            ),
            "all_records_contains_private_data_false": all(
                record["contains_private_data_in_file"] is False for record in records
            ),
        },
    }


def main() -> int:
    rows, row_summary = collect_worker_rows()
    records, validation_summary = build_validation_records(rows)

    MANIFEST_PATH.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )

    summary = build_summary(rows, records, row_summary, validation_summary)
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"validation_status={summary['validation_status']}")
    print(f"total_manifest_rows={summary['total_manifest_rows']}")
    print(f"total_topic_files={summary['total_topic_files']}")
    print(f"markdown_count={summary['markdown_count']}")
    print(f"python_count={summary['python_count']}")
    print(f"passed_record_count={summary['passed_record_count']}")
    print(f"failed_record_count={summary['failed_record_count']}")
    print(f"missing_files={summary['missing_files_count']}")
    print(f"metadata_errors={summary['metadata_errors_count']}")
    print(f"scope_errors={summary['scope_errors_count']}")
    print(f"git_scope_errors={summary['git_scope']['out_of_scope_error_count']}")
    print(f"secret_scan_result={summary['secret_scan']['result']}")

    return 0 if summary["validation_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
