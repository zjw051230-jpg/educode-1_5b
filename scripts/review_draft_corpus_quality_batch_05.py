from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from validate_draft_corpus_batch_03 import PROJECT_ROOT, parse_jsonl_registry

BATCH_ROOT = PROJECT_ROOT / "data" / "real_corpus" / "draft_queue" / "domain_synthetic_batch_05"
VALIDATION_MANIFEST_PATH = BATCH_ROOT / "batch_05_validation_manifest.jsonl"
VALIDATION_SUMMARY_PATH = BATCH_ROOT / "batch_05_validation_summary.json"
QUALITY_MANIFEST_PATH = BATCH_ROOT / "batch_05_quality_review_manifest.jsonl"
QUALITY_SUMMARY_PATH = BATCH_ROOT / "batch_05_quality_review_summary.json"

QUALITY_PASS = "quality_pass"
QUALITY_NEEDS_EDIT = "needs_edit"
QUALITY_REJECT = "reject"
MIN_MARKDOWN_SECTION_COUNT = 4
INTERNAL_REPEAT_THRESHOLD = 3
TRACE_NOTE_PATTERN = re.compile(r"^#\s*trace_note_\d+:", re.IGNORECASE)
CHINESE_CHAR_PATTERN = re.compile(r"[一-鿿]")
LATIN_WORD_PATTERN = re.compile(r"[A-Za-z]{2,}")
URL_PATTERN = re.compile(r"https?://|www\.", re.IGNORECASE)
EXTERNAL_REFERENCE_PATTERN = re.compile(
    r"\b(github|wikipedia|stack overflow|stackoverflow|arxiv|doi|paper|blog post|according to|source:)\b",
    re.IGNORECASE,
)
STRONG_CLAIM_PATTERN = re.compile(
    r"\b(production ready|state of the art|benchmark winner|definitive proof|guaranteed improvement|guaranteed quality)\b",
    re.IGNORECASE,
)

DOMAIN_DRIFT_PATTERNS = {
    "medical": re.compile(r"\b(patient|treatment|prescription|disease)\b", re.IGNORECASE),
    "financial": re.compile(r"\b(investment|portfolio|stock price|trading advice|loan approval|mortgage)\b", re.IGNORECASE),
    "legal": re.compile(r"\b(lawsuit|legal advice|contract dispute|tax filing|court ruling)\b", re.IGNORECASE),
}


def load_validation_manifest() -> list[dict[str, Any]]:
    rows, errors = parse_jsonl_registry(VALIDATION_MANIFEST_PATH)
    if errors:
        raise ValueError("; ".join(errors))
    return rows


def load_validation_summary() -> dict[str, Any]:
    return json.loads(VALIDATION_SUMMARY_PATH.read_text(encoding="utf-8"))


def strip_markdown_metadata(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                return "\n".join(lines[index + 1 :])
    return text


def strip_python_metadata(text: str) -> str:
    lines = text.splitlines()
    start_index = 0
    saw_metadata = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            if saw_metadata:
                start_index = index + 1
                continue
            start_index = index + 1
            continue
        if stripped.startswith("#"):
            saw_metadata = True
            start_index = index + 1
            continue
        break
    return "\n".join(lines[start_index:])


def strip_metadata(text: str, file_type: str) -> str:
    if file_type == "markdown":
        return strip_markdown_metadata(text)
    return strip_python_metadata(text)


def nonempty_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def count_markdown_sections(lines: list[str]) -> int:
    return sum(1 for line in lines if line.startswith("##"))


def is_significant_line(line: str) -> bool:
    stripped = line.strip()
    if len(stripped) < 24:
        return False
    if stripped.startswith(("#", "##", "###", "- ", "* ", "```")):
        return False
    if re.match(r"\d+\.\s", stripped):
        return False
    return True


def collect_repeated_internal_lines(lines: list[str]) -> list[str]:
    counts = Counter()
    for line in lines:
        stripped = line.strip()
        if is_significant_line(line):
            counts[stripped] += 1
            continue
        if len(stripped) >= 24 and stripped.startswith(("- ", "* ")):
            counts[stripped] += 1
    return sorted(line for line, count in counts.items() if count >= INTERNAL_REPEAT_THRESHOLD)


def count_trace_notes(lines: list[str]) -> int:
    return sum(1 for line in lines if TRACE_NOTE_PATTERN.match(line.strip()))


def collect_domain_drift_flags(text: str) -> list[str]:
    hits: list[str] = []
    for name, pattern in DOMAIN_DRIFT_PATTERNS.items():
        if pattern.search(text):
            hits.append(name)
    return sorted(hits)


def collect_external_reference_flags(text: str) -> list[str]:
    hits: list[str] = []
    if URL_PATTERN.search(text):
        hits.append("url")
    if EXTERNAL_REFERENCE_PATTERN.search(text):
        hits.append("external_reference_term")
    return hits


def collect_claim_strength_flags(text: str) -> list[str]:
    if STRONG_CLAIM_PATTERN.search(text):
        return ["strong_claim_language"]
    return []


def build_feature_rows(validation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    feature_rows: list[dict[str, Any]] = []
    for row in validation_rows:
        file_path = PROJECT_ROOT / str(row["file_path"])
        raw_text = file_path.read_text(encoding="utf-8")
        body_text = strip_metadata(raw_text, str(row["file_type"]))
        lines = body_text.splitlines()
        stripped_lines = nonempty_lines(body_text)
        repeated_internal_lines = collect_repeated_internal_lines(lines)
        trace_note_count = count_trace_notes(lines)
        markdown_section_count = count_markdown_sections(stripped_lines) if row["file_type"] == "markdown" else 0
        domain_drift_flags = collect_domain_drift_flags(body_text)
        external_reference_flags = collect_external_reference_flags(body_text)
        claim_strength_flags = collect_claim_strength_flags(body_text)
        bilingual_pair_ok = None
        if row["worker_id"] == "CC-5" and row["file_type"] == "markdown":
            has_chinese = bool(CHINESE_CHAR_PATTERN.search(body_text))
            has_latin = bool(LATIN_WORD_PATTERN.search(body_text))
            bilingual_pair_ok = ("EN:" in body_text and has_chinese) or (has_chinese and has_latin)

        feature_rows.append(
            {
                "topic_id": row["topic_id"],
                "worker_id": row["worker_id"],
                "worker_directory": row["worker_directory"],
                "subcategory": row["subcategory"],
                "title": row["title"],
                "file_path": row["file_path"],
                "file_type": row["file_type"],
                "line_count": row["line_count"],
                "char_count": row["char_count"],
                "repeated_internal_lines": repeated_internal_lines,
                "trace_note_count": trace_note_count,
                "markdown_section_count": markdown_section_count,
                "domain_drift_flags": domain_drift_flags,
                "external_reference_flags": external_reference_flags,
                "claim_strength_flags": claim_strength_flags,
                "bilingual_pair_ok": bilingual_pair_ok,
            }
        )
    return feature_rows


def review_rows(feature_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in feature_rows:
        flags: list[str] = []
        notes: list[str] = []

        if row["external_reference_flags"]:
            flags.extend(row["external_reference_flags"])
            notes.append("external-source style reference detected in draft body")
        if row["domain_drift_flags"]:
            flags.extend(f"domain_drift:{flag}" for flag in row["domain_drift_flags"])
            notes.append("domain-drift terminology detected outside the project backbone")
        if row["claim_strength_flags"]:
            flags.extend(row["claim_strength_flags"])
            notes.append("strong claim language detected and should be softened for draft-review use")
        if row["repeated_internal_lines"]:
            flags.append("repeated_internal_line")
            notes.append(
                f"repeated internal line patterns detected: {', '.join(row['repeated_internal_lines'][:3])}"
            )
        if row["trace_note_count"] >= INTERNAL_REPEAT_THRESHOLD:
            flags.append("trace_note_residue")
            notes.append(f"repeated trace note residue detected: {row['trace_note_count']} lines")
        if row["file_type"] == "markdown" and row["markdown_section_count"] < MIN_MARKDOWN_SECTION_COUNT:
            flags.append("thin_section_structure")
            notes.append(
                f"markdown section count below expected review scaffold: {row['markdown_section_count']}"
            )
        if row["bilingual_pair_ok"] is False:
            flags.append("bilingual_pairing_missing")
            notes.append("bilingual markdown draft is missing either mixed-script evidence or an explicit EN: pairing")

        if row["external_reference_flags"] or row["domain_drift_flags"]:
            quality_state = QUALITY_REJECT
        elif flags:
            quality_state = QUALITY_NEEDS_EDIT
        else:
            quality_state = QUALITY_PASS

        records.append(
            {
                "topic_id": row["topic_id"],
                "worker_id": row["worker_id"],
                "worker_directory": row["worker_directory"],
                "subcategory": row["subcategory"],
                "title": row["title"],
                "file_path": row["file_path"],
                "file_type": row["file_type"],
                "line_count": row["line_count"],
                "char_count": row["char_count"],
                "markdown_section_count": row["markdown_section_count"],
                "repeated_internal_line_count": len(row["repeated_internal_lines"]),
                "repeated_internal_line_examples": row["repeated_internal_lines"][:3],
                "trace_note_count": row["trace_note_count"],
                "quality_flags": flags,
                "quality_state": quality_state,
                "quality_notes": notes,
            }
        )
    return records


def build_summary(records: list[dict[str, Any]], validation_summary: dict[str, Any]) -> dict[str, Any]:
    state_counts = Counter(record["quality_state"] for record in records)
    worker_counts = Counter(record["worker_id"] for record in records)
    worker_state_counts: dict[str, Counter[str]] = defaultdict(Counter)
    file_type_counts = Counter(record["file_type"] for record in records)
    flag_counts = Counter(flag for record in records for flag in record["quality_flags"])
    for record in records:
        worker_state_counts[record["worker_id"]][record["quality_state"]] += 1

    if state_counts[QUALITY_REJECT] > 0:
        quality_gate_status = "failed"
    elif state_counts[QUALITY_NEEDS_EDIT] > 0:
        quality_gate_status = "passed_with_notes"
    else:
        quality_gate_status = "passed"

    line_counts = [record["line_count"] for record in records]
    char_counts = [record["char_count"] for record in records]
    review_samples = {
        "needs_edit_examples": [
            {
                "topic_id": record["topic_id"],
                "file_path": record["file_path"],
                "quality_flags": record["quality_flags"],
            }
            for record in records
            if record["quality_state"] == QUALITY_NEEDS_EDIT
        ][:20],
        "reject_examples": [
            {
                "topic_id": record["topic_id"],
                "file_path": record["file_path"],
                "quality_flags": record["quality_flags"],
            }
            for record in records
            if record["quality_state"] == QUALITY_REJECT
        ][:20],
    }

    return {
        "batch_root": BATCH_ROOT.relative_to(PROJECT_ROOT).as_posix(),
        "validation_reference": {
            "validation_status": validation_summary.get("validation_status"),
            "validation_manifest_path": VALIDATION_MANIFEST_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "validation_summary_path": VALIDATION_SUMMARY_PATH.relative_to(PROJECT_ROOT).as_posix(),
        },
        "total_records": len(records),
        "quality_pass_count": state_counts[QUALITY_PASS],
        "needs_edit_count": state_counts[QUALITY_NEEDS_EDIT],
        "reject_count": state_counts[QUALITY_REJECT],
        "quality_gate_status": quality_gate_status,
        "worker_counts": dict(sorted(worker_counts.items())),
        "worker_quality_state_counts": {
            worker_id: dict(sorted(counter.items()))
            for worker_id, counter in sorted(worker_state_counts.items())
        },
        "file_type_counts": dict(sorted(file_type_counts.items())),
        "flag_counts": dict(sorted(flag_counts.items())),
        "line_count_stats": {
            "min": min(line_counts) if line_counts else 0,
            "max": max(line_counts) if line_counts else 0,
            "mean": round(mean(line_counts), 2) if line_counts else 0.0,
        },
        "char_count_stats": {
            "min": min(char_counts) if char_counts else 0,
            "max": max(char_counts) if char_counts else 0,
            "mean": round(mean(char_counts), 2) if char_counts else 0.0,
        },
        "review_samples": review_samples,
    }


def main() -> int:
    validation_rows = load_validation_manifest()
    validation_summary = load_validation_summary()
    feature_rows = build_feature_rows(validation_rows)
    records = review_rows(feature_rows)

    QUALITY_MANIFEST_PATH.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )

    summary = build_summary(records, validation_summary)
    QUALITY_SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"total_records={summary['total_records']}")
    print(f"quality_pass_count={summary['quality_pass_count']}")
    print(f"needs_edit_count={summary['needs_edit_count']}")
    print(f"reject_count={summary['reject_count']}")
    print(f"quality_gate_status={summary['quality_gate_status']}")
    print(f"flag_counts={json.dumps(summary['flag_counts'], ensure_ascii=False, sort_keys=True)}")

    return 0 if summary["quality_gate_status"] != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
