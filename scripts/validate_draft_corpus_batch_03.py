from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BATCH_ROOT = PROJECT_ROOT / "data" / "real_corpus" / "draft_queue" / "domain_synthetic_batch_03"
FRAMEWORK_DIR = BATCH_ROOT / "00_framework"
REGISTRY_PATH = FRAMEWORK_DIR / "topic_registry.jsonl"
SUMMARY_PATH = FRAMEWORK_DIR / "draft_validation_summary.json"

EXPECTED_REGISTRY_ROWS = 120
EXPECTED_WORKER_COUNTS = {
    "CC-1": 20,
    "CC-2": 20,
    "CC-3": 20,
    "CC-4": 20,
    "CC-5": 20,
    "CC-6": 20,
}
EXPECTED_CATEGORY_TO_WORKER = {
    "cc1_ml_foundations": "CC-1",
    "cc2_python_data_systems": "CC-2",
    "cc3_transformer_architecture": "CC-3",
    "cc4_training_runtime_systems": "CC-4",
    "cc5_bilingual_qa": "CC-5",
    "cc6_code_snippets": "CC-6",
}
EXPECTED_MARKDOWN_METADATA = {
    "draft_status": "candidate",
    "source_category": "synthetic_examples",
    "project_backbone": "cs_ml_python_transformer_training_systems",
    "approved_for_training": "false",
    "contains_external_text": "false",
    "contains_private_data": "false",
    "target_use": "draft_review_only",
}
EXPECTED_PYTHON_METADATA = EXPECTED_MARKDOWN_METADATA.copy()
ALLOWED_FRAMEWORK_FILES = {
    "topic_registry.jsonl",
    "draft_markdown_template.md",
    "draft_python_template.py",
    "draft_validation_summary.json",
}
ALLOWED_GIT_STATUS_PATHS = {
    "README.md",
    "docs/experiment_index.md",
    "docs/d17_1_draft_corpus_generation_validation.md",
    "docs/d17_1_worker_aggregation_summary.md",
    "scripts/validate_draft_corpus_batch_03.py",
}
ALLOWED_GIT_STATUS_PREFIXES = (
    "data/real_corpus/draft_queue/domain_synthetic_batch_03/",
)
SECRET_PATTERNS = {
    "api_key": re.compile(r"(?i)\bapi[_-]?key\b"),
    "password": re.compile(r"(?i)\bpassword\b"),
    "private_key": re.compile(r"(?i)\bprivate[_-]?key\b"),
    "sk-": re.compile(r"(?i)\bsk-[a-z0-9]{8,}\b"),
    "secret": re.compile(r"(?i)\bsecret\b"),
    "token": re.compile(r"(?i)\btoken\b"),
}
CREDENTIAL_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(api[_-]?key|password|private[_-]?key|secret|access[_-]?token|auth[_-]?token)\b\s*[:=]\s*['\"]?([^'\"\s]{8,}|[^'\"]{8,})['\"]?"
)
PRIVATE_KEY_BLOCK_PATTERN = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
PLACEHOLDER_TERMS = {
    "example",
    "dummy",
    "placeholder",
    "sample",
    "fake",
    "test",
    "demo",
    "teaching",
    "educational",
    "synthetic",
}
TOKEN_EXPLANATORY_TERMS = {
    "next token",
    "special token",
    "tokenizer",
    "token ids",
    "token id",
    "token count",
    "token boundary",
    "tokenization",
    "token embeddings",
    "token prediction",
    "id_to_token",
    "token_to_id",
    "source_category",
    "approved_for_training",
    "target_use",
}


def normalize_worker_id(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip().upper().replace("_", "").replace(" ", "")
    match = re.fullmatch(r"CC-?(\d)", text)
    if not match:
        return value.strip()
    return f"CC-{match.group(1)}"


def file_type_to_suffix(file_type: str) -> str:
    mapping = {
        "markdown": ".md",
        "python": ".py",
    }
    return mapping[file_type]


def parse_jsonl_registry(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                errors.append(f"registry line {line_number} is empty")
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"registry line {line_number} is not valid JSON: {exc}")
                continue
            if not isinstance(row, dict):
                errors.append(f"registry line {line_number} is not a JSON object")
                continue
            rows.append(row)
    return rows, errors


def parse_markdown_metadata(text: str) -> tuple[dict[str, str], str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "missing opening YAML header"

    metadata: dict[str, str] = {}
    closing_index = None
    for index in range(1, len(lines)):
        line = lines[index].strip()
        if line == "---":
            closing_index = index
            break
        if ":" not in lines[index]:
            continue
        key, value = lines[index].split(":", 1)
        metadata[key.strip()] = value.strip()

    if closing_index is None:
        return metadata, "missing closing YAML header"
    return metadata, None


def parse_python_metadata(text: str) -> tuple[dict[str, str], str | None]:
    metadata: dict[str, str] = {}
    saw_metadata = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if saw_metadata:
                break
            continue
        if not stripped.startswith("#"):
            break
        saw_metadata = True
        body = stripped[1:].strip()
        if ":" not in body:
            continue
        key, value = body.split(":", 1)
        metadata[key.strip()] = value.strip()
    if not saw_metadata:
        return metadata, "missing leading metadata comments"
    return metadata, None


def read_metadata(path: Path, file_type: str) -> tuple[dict[str, str], str | None]:
    text = path.read_text(encoding="utf-8")
    if file_type == "markdown":
        return parse_markdown_metadata(text)
    return parse_python_metadata(text)


def count_lines(path: Path) -> int:
    return sum(1 for _ in path.open("r", encoding="utf-8"))


def classify_secret_hits(path: Path, text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    explanatory_hits: list[dict[str, Any]] = []
    credential_hits: list[dict[str, Any]] = []
    lines = text.splitlines()

    for line_number, line in enumerate(lines, start=1):
        lowered = line.lower()

        if PRIVATE_KEY_BLOCK_PATTERN.search(line):
            credential_hits.append(
                {
                    "file": path.relative_to(PROJECT_ROOT).as_posix(),
                    "line": line_number,
                    "pattern": "private_key",
                    "context": line.strip()[:160],
                    "classification": "credential-style",
                }
            )
            continue

        assignment_match = CREDENTIAL_ASSIGNMENT_PATTERN.search(line)
        if assignment_match:
            assigned_value = assignment_match.group(2).strip().strip('"\'')
            if not any(term in assigned_value.lower() for term in PLACEHOLDER_TERMS):
                credential_hits.append(
                    {
                        "file": path.relative_to(PROJECT_ROOT).as_posix(),
                        "line": line_number,
                        "pattern": assignment_match.group(1).lower(),
                        "context": line.strip()[:160],
                        "classification": "credential-style",
                    }
                )
                continue

        for pattern_name, pattern in SECRET_PATTERNS.items():
            if not pattern.search(line):
                continue

            classification = "explanatory-only"
            if pattern_name == "sk-":
                classification = "credential-style"
            elif pattern_name in {"api_key", "password", "private_key"}:
                if not any(term in lowered for term in PLACEHOLDER_TERMS):
                    classification = "credential-style"
            elif pattern_name == "secret":
                if (
                    "secret scan" not in lowered
                    and "secret-pattern" not in lowered
                    and "secret pattern" not in lowered
                    and "secret-like" not in lowered
                    and "secret-like strings" not in lowered
                    and "secret-like content" not in lowered
                    and "secret-like value" not in lowered
                    and "secret-like values" not in lowered
                    and "secret-like token" not in lowered
                    and "secret-like tokens" not in lowered
                    and "secret-like credential" not in lowered
                    and not any(term in lowered for term in PLACEHOLDER_TERMS)
                ):
                    classification = "credential-style"
            elif pattern_name == "token":
                if not any(term in lowered for term in TOKEN_EXPLANATORY_TERMS):
                    classification = "explanatory-only"

            hit = {
                "file": path.relative_to(PROJECT_ROOT).as_posix(),
                "line": line_number,
                "pattern": pattern_name,
                "context": line.strip()[:160],
                "classification": classification,
            }
            if classification == "credential-style":
                credential_hits.append(hit)
            else:
                explanatory_hits.append(hit)

    return explanatory_hits, credential_hits


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


def main() -> int:
    registry_rows, registry_parse_errors = parse_jsonl_registry(REGISTRY_PATH)
    registry_errors = list(registry_parse_errors)
    git_status_entries, git_status_errors = parse_git_status_lines()
    registry_errors.extend(git_status_errors)
    missing_files: list[str] = []
    metadata_errors: list[str] = []
    scope_errors: list[str] = []
    explanatory_secret_hits: list[dict[str, Any]] = []
    credential_secret_hits: list[dict[str, Any]] = []
    actual_topic_paths: set[Path] = set()
    expected_topic_paths: set[Path] = set()
    worker_counts = Counter()
    markdown_count = 0
    python_count = 0
    worker_file_type_counts: dict[str, Counter[str]] = defaultdict(Counter)
    line_counts: list[int] = []

    topic_ids = [row.get("topic_id") for row in registry_rows]
    registry_relative_targets = [
        f"{row.get('category')}/{row.get('subcategory')}/{row.get('proposed_filename')}"
        for row in registry_rows
    ]

    if len(registry_rows) != EXPECTED_REGISTRY_ROWS:
        registry_errors.append(
            f"expected {EXPECTED_REGISTRY_ROWS} registry rows, found {len(registry_rows)}"
        )
    if len(topic_ids) != len(set(topic_ids)):
        registry_errors.append("topic_id values are not unique")
    if len(registry_relative_targets) != len(set(registry_relative_targets)):
        registry_errors.append("registry target paths are not unique")

    for row in registry_rows:
        category = row.get("category")
        subcategory = row.get("subcategory")
        topic_id = row.get("topic_id")
        file_type = row.get("file_type")
        proposed_filename = row.get("proposed_filename")
        registry_worker = normalize_worker_id(str(row.get("worker_id", "")))

        if category not in EXPECTED_CATEGORY_TO_WORKER:
            scope_errors.append(f"unknown registry category for {topic_id}: {category}")
            continue
        expected_worker = EXPECTED_CATEGORY_TO_WORKER[category]
        worker_counts[registry_worker] += 1

        if registry_worker != expected_worker:
            registry_errors.append(
                f"registry worker/category mismatch for {topic_id}: {registry_worker} vs {category}"
            )

        if row.get("approved_for_training") is not False:
            metadata_errors.append(f"registry approved_for_training is not false for {topic_id}")
        if row.get("contains_external_text") is not False:
            metadata_errors.append(f"registry contains_external_text is not false for {topic_id}")
        if row.get("contains_private_data") is not False:
            metadata_errors.append(f"registry contains_private_data is not false for {topic_id}")

        if file_type not in {"markdown", "python"}:
            scope_errors.append(f"unsupported file_type for {topic_id}: {file_type}")
            continue

        expected_suffix = file_type_to_suffix(file_type)
        if not str(proposed_filename).endswith(expected_suffix):
            scope_errors.append(
                f"file_type mismatch in registry for {topic_id}: {proposed_filename} should end with {expected_suffix}"
            )

        expected_path = BATCH_ROOT / category / subcategory / str(proposed_filename)
        expected_topic_paths.add(expected_path)

        if not expected_path.exists():
            missing_files.append(expected_path.relative_to(PROJECT_ROOT).as_posix())
            continue

        actual_topic_paths.add(expected_path)

        if expected_path.suffix != expected_suffix:
            scope_errors.append(
                f"file_type mismatch on disk for {topic_id}: {expected_path.name} does not match {file_type}"
            )

        metadata, metadata_parse_error = read_metadata(expected_path, file_type)
        if metadata_parse_error is not None:
            metadata_errors.append(
                f"{expected_path.relative_to(PROJECT_ROOT).as_posix()}: {metadata_parse_error}"
            )

        expected_metadata = EXPECTED_MARKDOWN_METADATA if file_type == "markdown" else EXPECTED_PYTHON_METADATA
        for key, expected_value in expected_metadata.items():
            actual_value = metadata.get(key)
            if actual_value is None:
                metadata_errors.append(
                    f"{expected_path.relative_to(PROJECT_ROOT).as_posix()}: missing metadata field {key}"
                )
                continue
            if actual_value.strip().lower() != expected_value:
                metadata_errors.append(
                    f"{expected_path.relative_to(PROJECT_ROOT).as_posix()}: expected {key}={expected_value}, found {actual_value}"
                )

        actual_topic_id = metadata.get("topic_id")
        if actual_topic_id != topic_id:
            metadata_errors.append(
                f"{expected_path.relative_to(PROJECT_ROOT).as_posix()}: topic_id mismatch ({actual_topic_id} vs {topic_id})"
            )

        actual_worker = normalize_worker_id(metadata.get("worker_id"))
        if actual_worker != expected_worker:
            metadata_errors.append(
                f"{expected_path.relative_to(PROJECT_ROOT).as_posix()}: worker_id mismatch ({actual_worker} vs {expected_worker})"
            )

        line_counts.append(count_lines(expected_path))
        if file_type == "markdown":
            markdown_count += 1
        else:
            python_count += 1
        worker_file_type_counts[expected_worker][file_type] += 1

        text = expected_path.read_text(encoding="utf-8")
        explanatory_hits, credential_hits = classify_secret_hits(expected_path, text)
        explanatory_secret_hits.extend(explanatory_hits)
        credential_secret_hits.extend(credential_hits)

    for worker_id, expected_count in EXPECTED_WORKER_COUNTS.items():
        observed = worker_counts.get(worker_id, 0)
        if observed != expected_count:
            registry_errors.append(
                f"expected {expected_count} registry rows for {worker_id}, found {observed}"
            )

    batch_summary_paths = []
    for category in EXPECTED_CATEGORY_TO_WORKER:
        batch_summary_path = BATCH_ROOT / category / "batch_summary.md"
        if batch_summary_path.exists():
            batch_summary_paths.append(batch_summary_path)
            text = batch_summary_path.read_text(encoding="utf-8")
            explanatory_hits, credential_hits = classify_secret_hits(batch_summary_path, text)
            explanatory_secret_hits.extend(explanatory_hits)
            credential_secret_hits.extend(credential_hits)
        else:
            scope_errors.append(
                f"missing batch_summary.md for {category}: {(BATCH_ROOT / category / 'batch_summary.md').relative_to(PROJECT_ROOT).as_posix()}"
            )

    expected_extra_files = {FRAMEWORK_DIR / name for name in ALLOWED_FRAMEWORK_FILES}
    for path in BATCH_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.name == ".gitkeep":
            continue
        if path in expected_topic_paths:
            continue
        if path in batch_summary_paths:
            continue
        if path in expected_extra_files:
            continue
        scope_errors.append(f"unexpected file in batch scope: {path.relative_to(PROJECT_ROOT).as_posix()}")

    git_scope_errors: list[str] = []
    for entry in git_status_entries:
        path_text = entry["path"]
        if not is_allowed_git_status_path(path_text):
            git_scope_errors.append(f"out-of-scope git status path: {entry['status']} {path_text}")

    total_topic_files = len(actual_topic_paths)
    batch_summary_count = len(batch_summary_paths)

    if credential_secret_hits:
        secret_scan_result = "failed"
    elif explanatory_secret_hits:
        secret_scan_result = "explanatory-only"
    else:
        secret_scan_result = "passed"

    validation_status = "passed"
    if (
        registry_errors
        or missing_files
        or metadata_errors
        or scope_errors
        or git_scope_errors
        or credential_secret_hits
        or len(registry_rows) != EXPECTED_REGISTRY_ROWS
        or total_topic_files != EXPECTED_REGISTRY_ROWS
        or batch_summary_count != 6
    ):
        validation_status = "failed"

    summary = {
        "validation_status": validation_status,
        "registry_path": REGISTRY_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "registry_rows": len(registry_rows),
        "registry_errors": registry_errors,
        "total_topic_files": total_topic_files,
        "markdown_count": markdown_count,
        "python_count": python_count,
        "batch_summary_count": batch_summary_count,
        "worker_counts": dict(sorted(worker_counts.items())),
        "file_type_counts_by_worker": {
            worker_id: dict(sorted(counter.items()))
            for worker_id, counter in sorted(worker_file_type_counts.items())
        },
        "line_count_stats": {
            "min": min(line_counts) if line_counts else 0,
            "max": max(line_counts) if line_counts else 0,
            "mean": round(mean(line_counts), 2) if line_counts else 0.0,
        },
        "missing_files": missing_files,
        "missing_files_count": len(missing_files),
        "metadata_errors": metadata_errors,
        "metadata_errors_count": len(metadata_errors),
        "scope_errors": scope_errors,
        "scope_errors_count": len(scope_errors),
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
            "explanatory_only_count": len(explanatory_secret_hits),
            "credential_style_count": len(credential_secret_hits),
            "explanatory_only_examples": explanatory_secret_hits[:20],
            "credential_style_examples": credential_secret_hits[:20],
        },
        "approval_state": {
            "all_registry_rows_approved_for_training_false": all(
                row.get("approved_for_training") is False for row in registry_rows
            ),
            "all_registry_rows_contains_external_text_false": all(
                row.get("contains_external_text") is False for row in registry_rows
            ),
            "all_registry_rows_contains_private_data_false": all(
                row.get("contains_private_data") is False for row in registry_rows
            ),
        },
    }

    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"validation_status={validation_status}")
    print(f"registry_rows={len(registry_rows)}")
    print(f"total_topic_files={total_topic_files}")
    print(f"batch_summary_count={batch_summary_count}")
    print(f"markdown_count={markdown_count}")
    print(f"python_count={python_count}")
    print(f"missing_files={len(missing_files)}")
    print(f"metadata_errors={len(metadata_errors)}")
    print(f"scope_errors={len(scope_errors) + len(registry_errors)}")
    print(f"git_scope_errors={len(git_scope_errors)}")
    print(f"secret_scan_result={secret_scan_result}")

    return 0 if validation_status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
