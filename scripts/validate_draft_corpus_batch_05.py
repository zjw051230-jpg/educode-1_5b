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

BATCH_ROOT = PROJECT_ROOT / "data" / "real_corpus" / "draft_queue" / "domain_synthetic_batch_05"
SUMMARY_PATH = BATCH_ROOT / "batch_05_validation_summary.json"
MANIFEST_PATH = BATCH_ROOT / "batch_05_validation_manifest.jsonl"
EXPECTED_BATCH_ID = "domain_synthetic_batch_05"
WORKER_SPECS = {
    "cc1_ml_foundations": {
        "worker_id": "CC-1",
        "expected_total": 100,
        "expected_markdown": 70,
        "expected_python": 30,
        "topic_prefix": "B05-MLF-",
    },
    "cc2_python_data_systems": {
        "worker_id": "CC-2",
        "expected_total": 100,
        "expected_markdown": 60,
        "expected_python": 40,
        "topic_prefix": "B05-PDS-",
    },
    "cc3_transformer_architecture": {
        "worker_id": "CC-3",
        "expected_total": 100,
        "expected_markdown": 60,
        "expected_python": 40,
        "topic_prefix": "B05-TRF-",
    },
    "cc4_training_runtime_systems": {
        "worker_id": "CC-4",
        "expected_total": 100,
        "expected_markdown": 60,
        "expected_python": 40,
        "topic_prefix": "B05-RTS-",
    },
    "cc5_bilingual_qa": {
        "worker_id": "CC-5",
        "expected_total": 100,
        "expected_markdown": 85,
        "expected_python": 15,
        "topic_prefix": "B05-BIL-",
    },
    "cc6_code_snippets": {
        "worker_id": "CC-6",
        "expected_total": 100,
        "expected_markdown": 30,
        "expected_python": 70,
        "topic_prefix": "B05-COD-",
    },
}
EXPECTED_TOTAL_TOPIC_FILES = 600
EXPECTED_TOTAL_MARKDOWN = 365
EXPECTED_TOTAL_PYTHON = 235
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
REQUIRED_SUPPORT_FILES = {
    "batch_summary.md",
    "anti_template_self_check.md",
    "progress_0025.md",
    "progress_0050.md",
    "progress_0075.md",
    "progress_0100.md",
}
ALLOWED_BATCH_OUTPUT_FILES = {
    "batch_05_validation_summary.json",
    "batch_05_validation_manifest.jsonl",
    "batch_05_quality_review_summary.json",
    "batch_05_quality_review_manifest.jsonl",
}
ALLOWED_GIT_STATUS_PATHS = {
    "README.md",
    "docs/experiment_index.md",
    "docs/d19_2_batch_05_repair_aware_validation_review.md",
    "docs/d19_2_batch_05_worker_aggregation_summary.md",
    "docs/d19_3_batch_05_sampling_review_plan.md",
    "scripts/validate_draft_corpus_batch_05.py",
    "scripts/review_draft_corpus_quality_batch_05.py",
    "tests/test_validate_draft_corpus_batch_05.py",
    "tests/test_review_draft_corpus_quality_batch_05.py",
}
ALLOWED_GIT_STATUS_PREFIXES = (
    BATCH_ROOT.relative_to(PROJECT_ROOT).as_posix() + "/",
)


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
        entries.append({"status": status_code, "path": path_text.replace("\\", "/")})
    return entries, errors



def is_allowed_git_status_path(path_text: str) -> bool:
    return path_text in ALLOWED_GIT_STATUS_PATHS or path_text.startswith(ALLOWED_GIT_STATUS_PREFIXES)



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
    if path_hint:
        suffix = Path(path_hint).suffix.lower()
        if suffix == ".md":
            return "markdown"
        if suffix == ".py":
            return "python"
    return None



def normalize_relative_path(category: str, row: dict[str, Any], notes: list[str]) -> Path | None:
    raw_filename = str(row.get("filename", "")).strip()
    raw_subdirectory = str(row.get("subdirectory", "")).strip()
    raw_path = str(row.get("filename", "")).strip()
    worker_root = BATCH_ROOT / category

    if raw_path.startswith(BATCH_ROOT.relative_to(PROJECT_ROOT).as_posix() + "/"):
        return Path(raw_path)
    if raw_filename and raw_subdirectory:
        return (worker_root / raw_subdirectory / raw_filename).relative_to(PROJECT_ROOT)
    notes.append(f"unable to resolve file path for row {row}")
    return None



def expected_metadata_for(file_type: str) -> dict[str, str]:
    if file_type == "markdown":
        return EXPECTED_MARKDOWN_METADATA
    return EXPECTED_PYTHON_METADATA



def count_lines_and_chars(text: str) -> tuple[int, int]:
    return len(text.splitlines()), len(text)



def reclassify_batch_05_secret_hits(
    explanatory_hits: list[dict[str, Any]], credential_hits: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    normalized_explanatory_hits = list(explanatory_hits)
    normalized_credential_hits: list[dict[str, Any]] = []
    for hit in credential_hits:
        context = str(hit.get("context", "")).lower()
        if "secret_scan_result" in context and "no matches for" in context:
            reclassified_hit = dict(hit)
            reclassified_hit["classification"] = "explanatory-only"
            normalized_explanatory_hits.append(reclassified_hit)
        else:
            normalized_credential_hits.append(hit)
    return normalized_explanatory_hits, normalized_credential_hits



def main() -> int:
    git_status_entries, git_status_errors = parse_git_status_lines()
    missing_files: list[str] = []
    metadata_errors: list[str] = []
    scope_errors: list[str] = []
    explanatory_secret_hits: list[dict[str, Any]] = []
    credential_secret_hits: list[dict[str, Any]] = []
    validation_records: list[dict[str, Any]] = []
    seen_topic_ids: set[str] = set()
    seen_paths: set[str] = set()
    duplicate_topic_id_count = 0
    duplicate_file_path_count = 0
    worker_manifest_count = 0
    batch_summary_count = 0
    anti_template_self_check_count = 0
    progress_checkpoint_count = 0
    worker_counts = Counter()
    file_type_counts_by_worker: dict[str, Counter[str]] = defaultdict(Counter)
    total_markdown = 0
    total_python = 0
    line_counts: list[int] = []
    char_total = 0

    for category, spec in WORKER_SPECS.items():
        worker_root = BATCH_ROOT / category
        if not worker_root.exists():
            scope_errors.append(f"missing worker directory: {worker_root.relative_to(PROJECT_ROOT).as_posix()}")
            continue

        manifest_path = worker_root / "worker_topic_manifest.jsonl"
        if not manifest_path.exists():
            missing_files.append(manifest_path.relative_to(PROJECT_ROOT).as_posix())
            continue
        worker_manifest_count += 1

        rows, errors = parse_jsonl_registry(manifest_path)
        if errors:
            metadata_errors.extend(
                f"{manifest_path.relative_to(PROJECT_ROOT).as_posix()}: {error}" for error in errors
            )
        if len(rows) != spec["expected_total"]:
            scope_errors.append(
                f"{manifest_path.relative_to(PROJECT_ROOT).as_posix()}: expected {spec['expected_total']} rows, found {len(rows)}"
            )

        for support_name in REQUIRED_SUPPORT_FILES:
            support_path = worker_root / support_name
            if not support_path.exists():
                missing_files.append(support_path.relative_to(PROJECT_ROOT).as_posix())
            else:
                text = support_path.read_text(encoding="utf-8")
                explanatory_hits, credential_hits = classify_secret_hits(support_path, text)
                explanatory_hits, credential_hits = reclassify_batch_05_secret_hits(
                    explanatory_hits, credential_hits
                )
                explanatory_secret_hits.extend(explanatory_hits)
                credential_secret_hits.extend(credential_hits)
                if support_name == "batch_summary.md":
                    batch_summary_count += 1
                elif support_name == "anti_template_self_check.md":
                    anti_template_self_check_count += 1
                elif support_name.startswith("progress_"):
                    progress_checkpoint_count += 1

        for row in rows:
            topic_id = str(row.get("topic_id", "")).strip()
            if topic_id in seen_topic_ids:
                duplicate_topic_id_count += 1
            else:
                seen_topic_ids.add(topic_id)

            if not topic_id.startswith(spec["topic_prefix"]):
                scope_errors.append(f"{topic_id}: wrong topic prefix for {spec['worker_id']}")

            notes: list[str] = []
            rel_path = normalize_relative_path(category, row, notes)
            if rel_path is None:
                scope_errors.extend(notes)
                continue
            rel_path_text = rel_path.as_posix()
            if rel_path_text in seen_paths:
                duplicate_file_path_count += 1
            else:
                seen_paths.add(rel_path_text)

            file_path = PROJECT_ROOT / rel_path
            if not file_path.exists():
                missing_files.append(rel_path_text)
                continue

            if not rel_path_text.startswith((BATCH_ROOT / category).relative_to(PROJECT_ROOT).as_posix() + "/"):
                scope_errors.append(f"{topic_id}: path outside worker scope: {rel_path_text}")

            file_type = normalize_file_type(row.get("file_type"), rel_path_text)
            if file_type is None:
                scope_errors.append(f"{topic_id}: unrecognized file_type {row.get('file_type')!r}")
                continue

            metadata, metadata_parse_error = read_metadata(file_path, file_type)
            if metadata_parse_error is not None:
                metadata_errors.append(f"{rel_path_text}: {metadata_parse_error}")

            expected_metadata = expected_metadata_for(file_type)
            for key, expected_value in expected_metadata.items():
                actual_value = metadata.get(key)
                if actual_value is None:
                    metadata_errors.append(f"{rel_path_text}: missing metadata field {key}")
                    continue
                if actual_value.strip().lower() != expected_value:
                    metadata_errors.append(
                        f"{rel_path_text}: expected {key}={expected_value}, found {actual_value}"
                    )

            metadata_worker = normalize_worker_id(metadata.get("worker_id"))
            if metadata_worker != spec["worker_id"]:
                metadata_errors.append(
                    f"{rel_path_text}: worker_id mismatch ({metadata_worker} vs {spec['worker_id']})"
                )
            if metadata.get("topic_id") != topic_id:
                metadata_errors.append(
                    f"{rel_path_text}: topic_id mismatch ({metadata.get('topic_id')} vs {topic_id})"
                )

            text = file_path.read_text(encoding="utf-8")
            line_count, char_count = count_lines_and_chars(text)
            line_counts.append(line_count)
            char_total += char_count
            worker_counts[spec["worker_id"]] += 1
            file_type_counts_by_worker[spec["worker_id"]][file_type] += 1
            if file_type == "markdown":
                total_markdown += 1
            else:
                total_python += 1

            explanatory_hits, credential_hits = classify_secret_hits(file_path, text)
            explanatory_secret_hits.extend(explanatory_hits)
            credential_secret_hits.extend(credential_hits)

            validation_records.append(
                {
                    "topic_id": topic_id,
                    "worker_id": spec["worker_id"],
                    "worker_directory": category,
                    "subcategory": str(row.get("subdirectory", "")).strip(),
                    "title": str(row.get("title", "")).strip(),
                    "file_path": rel_path_text,
                    "file_type": file_type,
                    "line_count": line_count,
                    "char_count": char_count,
                    "learning_objective": str(row.get("learning_objective", "")).strip(),
                    "writing_form": str(row.get("writing_form", "")).strip(),
                    "concrete_anchor": str(row.get("concrete_anchor", "")).strip(),
                    "anti_template_note": str(row.get("anti_template_note", "")).strip(),
                    "approved_for_training": False,
                    "contains_external_text": False,
                    "contains_private_data": False,
                }
            )

    for entry in git_status_entries:
        if not is_allowed_git_status_path(entry["path"]):
            scope_errors.append(f"out-of-scope git status path: {entry['status']} {entry['path']}")
    scope_errors.extend(git_status_errors)

    total_topic_files = len(validation_records)
    if total_topic_files != EXPECTED_TOTAL_TOPIC_FILES:
        scope_errors.append(f"expected {EXPECTED_TOTAL_TOPIC_FILES} topic files, found {total_topic_files}")
    if total_markdown != EXPECTED_TOTAL_MARKDOWN:
        scope_errors.append(f"expected {EXPECTED_TOTAL_MARKDOWN} markdown files, found {total_markdown}")
    if total_python != EXPECTED_TOTAL_PYTHON:
        scope_errors.append(f"expected {EXPECTED_TOTAL_PYTHON} python files, found {total_python}")

    for category, spec in WORKER_SPECS.items():
        worker_id = spec["worker_id"]
        if worker_counts.get(worker_id, 0) != spec["expected_total"]:
            scope_errors.append(
                f"expected {spec['expected_total']} files for {worker_id}, found {worker_counts.get(worker_id, 0)}"
            )
        if file_type_counts_by_worker[worker_id].get("markdown", 0) != spec["expected_markdown"]:
            scope_errors.append(
                f"expected {spec['expected_markdown']} markdown files for {worker_id}, found {file_type_counts_by_worker[worker_id].get('markdown', 0)}"
            )
        if file_type_counts_by_worker[worker_id].get("python", 0) != spec["expected_python"]:
            scope_errors.append(
                f"expected {spec['expected_python']} python files for {worker_id}, found {file_type_counts_by_worker[worker_id].get('python', 0)}"
            )

    validation_status = "passed"
    if missing_files or metadata_errors or scope_errors or duplicate_topic_id_count or duplicate_file_path_count or credential_secret_hits:
        validation_status = "failed"
    elif explanatory_secret_hits:
        validation_status = "passed_with_notes"

    summary = {
        "batch_root": BATCH_ROOT.relative_to(PROJECT_ROOT).as_posix(),
        "validation_status": validation_status,
        "total_topic_files": total_topic_files,
        "markdown_topic_files": total_markdown,
        "python_topic_files": total_python,
        "worker_manifest_count": worker_manifest_count,
        "batch_summary_count": batch_summary_count,
        "anti_template_self_check_count": anti_template_self_check_count,
        "progress_checkpoint_count": progress_checkpoint_count,
        "worker_counts": dict(sorted(worker_counts.items())),
        "file_type_counts_by_worker": {
            worker_id: dict(sorted(counter.items())) for worker_id, counter in sorted(file_type_counts_by_worker.items())
        },
        "line_count_min": min(line_counts) if line_counts else 0,
        "line_count_max": max(line_counts) if line_counts else 0,
        "line_count_mean": round(mean(line_counts), 2) if line_counts else 0.0,
        "char_count_total": char_total,
        "missing_files": len(missing_files),
        "metadata_errors": len(metadata_errors),
        "scope_errors": len(scope_errors),
        "duplicate_topic_id_count": duplicate_topic_id_count,
        "duplicate_file_path_count": duplicate_file_path_count,
        "explanatory_secret_hit_count": len(explanatory_secret_hits),
        "credential_style_secret_hit_count": len(credential_secret_hits),
        "secret_scan_result": "credential-style" if credential_secret_hits else ("explanatory-only" if explanatory_secret_hits else "clean"),
        "missing_file_examples": missing_files[:20],
        "metadata_error_examples": metadata_errors[:20],
        "scope_error_examples": scope_errors[:20],
    }

    MANIFEST_PATH.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in validation_records),
        encoding="utf-8",
    )
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"total_topic_files={summary['total_topic_files']}")
    print(f"markdown_topic_files={summary['markdown_topic_files']}")
    print(f"python_topic_files={summary['python_topic_files']}")
    print(f"validation_status={summary['validation_status']}")
    print(f"metadata_errors={summary['metadata_errors']}")
    print(f"scope_errors={summary['scope_errors']}")
    print(f"credential_style_secret_hit_count={summary['credential_style_secret_hit_count']}")
    return 0 if validation_status in {"passed", "passed_with_notes"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
