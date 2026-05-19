from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from validate_draft_corpus_batch_03 import PROJECT_ROOT, parse_jsonl_registry

BATCH_ROOT = PROJECT_ROOT / "data" / "real_corpus" / "draft_queue" / "domain_synthetic_batch_05"
VALIDATION_MANIFEST_PATH = BATCH_ROOT / "batch_05_validation_manifest.jsonl"
QUALITY_MANIFEST_PATH = BATCH_ROOT / "batch_05_quality_review_manifest.jsonl"
QUALITY_SUMMARY_PATH = BATCH_ROOT / "batch_05_quality_review_summary.json"
SAMPLING_MANIFEST_PATH = BATCH_ROOT / "batch_05_targeted_sampling_manifest.jsonl"
SAMPLING_SUMMARY_PATH = BATCH_ROOT / "batch_05_targeted_sampling_summary.json"

QUALITY_PASS = "quality_pass"
QUALITY_NEEDS_EDIT = "needs_edit"
WORKER_IDS = [f"CC-{index}" for index in range(1, 7)]
SAMPLES_PER_WORKER = 20
PASS_TARGET_PER_WORKER = 10
RISK_TARGET_PER_WORKER = 5
BOUNDARY_TARGET_PER_WORKER = 5
PRIORITY_FLAGS_BY_WORKER = {
    "CC-2": {"repeated_internal_line"},
    "CC-5": {"bilingual_pairing_missing", "thin_section_structure"},
    "CC-6": {"trace_note_residue", "thin_section_structure"},
}
REPRESENTATIVE_TOPICS_BY_WORKER = {
    "CC-2": ["B05-PDS-0001"],
    "CC-5": ["B05-BIL-0035"],
    "CC-6": ["B05-COD-0027"],
}


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows, errors = parse_jsonl_registry(path)
    if errors:
        raise ValueError("; ".join(errors))
    return rows


def load_quality_summary() -> dict[str, Any]:
    return json.loads(QUALITY_SUMMARY_PATH.read_text(encoding="utf-8"))


def index_validation_rows() -> dict[str, dict[str, Any]]:
    rows = load_rows(VALIDATION_MANIFEST_PATH)
    return {str(row["topic_id"]): row for row in rows}


def merge_rows() -> list[dict[str, Any]]:
    validation_by_topic = index_validation_rows()
    quality_rows = load_rows(QUALITY_MANIFEST_PATH)
    merged_rows: list[dict[str, Any]] = []
    for quality_row in quality_rows:
        topic_id = str(quality_row["topic_id"])
        validation_row = validation_by_topic.get(topic_id)
        if validation_row is None:
            raise ValueError(f"missing validation row for topic_id {topic_id}")
        merged_rows.append({**validation_row, **quality_row})
    return merged_rows


def add_reason(reasons: list[str], reason: str) -> None:
    if reason not in reasons:
        reasons.append(reason)


def add_selection(selected: dict[str, dict[str, Any]], row: dict[str, Any], reasons: list[str]) -> bool:
    topic_id = str(row["topic_id"])
    if topic_id in selected:
        for reason in reasons:
            add_reason(selected[topic_id]["reasons"], reason)
        return False
    selected[topic_id] = {"row": row, "reasons": []}
    for reason in reasons:
        add_reason(selected[topic_id]["reasons"], reason)
    return True


def coverage_score(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        1 if str(row.get("file_type")) == "python" else 0,
        len(str(row.get("writing_form", ""))),
        len(str(row.get("concrete_anchor", ""))),
        int(row.get("line_count", 0)),
        int(row.get("char_count", 0)),
        str(row.get("topic_id", "")),
    )


def risk_score(row: dict[str, Any], worker_id: str) -> tuple[Any, ...]:
    flags = set(str(flag) for flag in row.get("quality_flags", []))
    priority_hits = len(PRIORITY_FLAGS_BY_WORKER.get(worker_id, set()) & flags)
    return (
        priority_hits,
        len(flags),
        1 if str(row.get("file_type")) == "markdown" else 0,
        int(row.get("line_count", 0)),
        int(row.get("char_count", 0)),
        str(row.get("topic_id", "")),
    )


def pass_score(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        1 if str(row.get("file_type")) == "markdown" else 0,
        len(str(row.get("writing_form", ""))),
        len(str(row.get("concrete_anchor", ""))),
        int(row.get("line_count", 0)),
        int(row.get("char_count", 0)),
        str(row.get("topic_id", "")),
    )


def build_suggested_review_focus(row: dict[str, Any]) -> str:
    flags = [str(flag) for flag in row.get("quality_flags", [])]
    focus_points: list[str] = []
    if "repeated_internal_line" in flags:
        focus_points.append("Check whether repeated internal prompt residue weakens originality.")
    if "trace_note_residue" in flags:
        focus_points.append("Check whether repeated trace-note residue makes the code sample feel unfinished.")
    if "bilingual_pairing_missing" in flags:
        focus_points.append("Check whether the bilingual teaching signal is explicit enough on both language sides.")
    if "thin_section_structure" in flags:
        focus_points.append("Check whether the file is too thin to carry the teaching point clearly.")
    if str(row.get("file_type")) == "python":
        focus_points.append("Check whether the code performs the named topic-specific job rather than acting as a wrapper.")
    else:
        focus_points.append("Check whether the markdown structure supports a distinct teaching artifact rather than a stock scaffold.")
    return " ".join(focus_points[:3])


def build_sample_record(sample_id: str, row: dict[str, Any], reasons: list[str]) -> dict[str, Any]:
    return {
        "sample_id": sample_id,
        "topic_id": row["topic_id"],
        "worker_id": row["worker_id"],
        "file_path": row["file_path"],
        "file_type": row["file_type"],
        "review_state_from_quality": row["quality_state"],
        "risk_flags": row["quality_flags"],
        "writing_form": row.get("writing_form", ""),
        "concrete_anchor": row.get("concrete_anchor", ""),
        "sample_reason": "; ".join(reasons),
        "suggested_review_focus": build_suggested_review_focus(row),
        "human_review_status": "pending",
    }


def choose_boundary_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(rows, key=lambda row: (int(row.get("line_count", 0)), int(row.get("char_count", 0)), str(row.get("topic_id", ""))))
    if not ordered:
        return []
    candidates = [ordered[0], ordered[-1]]
    by_file_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_writing_form: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_anchor: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_file_type[str(row.get("file_type"))].append(row)
        by_writing_form[str(row.get("writing_form", ""))].append(row)
        by_anchor[str(row.get("concrete_anchor", ""))].append(row)
    for file_type in sorted(by_file_type):
        candidates.append(sorted(by_file_type[file_type], key=coverage_score, reverse=True)[0])
    for writing_form in sorted(by_writing_form):
        candidates.append(sorted(by_writing_form[writing_form], key=coverage_score, reverse=True)[0])
    for anchor in sorted(by_anchor):
        candidates.append(sorted(by_anchor[anchor], key=coverage_score, reverse=True)[0])
    unique: list[dict[str, Any]] = []
    seen_topics: set[str] = set()
    for row in candidates:
        topic_id = str(row["topic_id"])
        if topic_id in seen_topics:
            continue
        seen_topics.add(topic_id)
        unique.append(row)
    return unique


def sample_worker_rows(worker_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    worker_id = str(worker_rows[0]["worker_id"])
    selected: dict[str, dict[str, Any]] = {}
    pass_rows = [row for row in worker_rows if str(row.get("quality_state")) == QUALITY_PASS]
    risk_rows = [row for row in worker_rows if str(row.get("quality_state")) == QUALITY_NEEDS_EDIT]

    representative_topics = set(REPRESENTATIVE_TOPICS_BY_WORKER.get(worker_id, []))
    for row in worker_rows:
        if str(row.get("topic_id")) in representative_topics:
            add_selection(selected, row, ["cluster_representative"])

    for row in sorted(pass_rows, key=pass_score, reverse=True):
        if sum(1 for item in selected.values() if item["row"]["quality_state"] == QUALITY_PASS) >= PASS_TARGET_PER_WORKER:
            break
        add_selection(selected, row, ["quality_pass_representative"])

    priority_flags = PRIORITY_FLAGS_BY_WORKER.get(worker_id, set())
    prioritized_risk_rows = sorted(
        risk_rows,
        key=lambda row: risk_score(row, worker_id),
        reverse=True,
    )
    covered_priority_flags: set[str] = set()
    for flag in sorted(priority_flags):
        for row in prioritized_risk_rows:
            row_flags = set(str(item) for item in row.get("quality_flags", []))
            if flag not in row_flags:
                continue
            if add_selection(selected, row, ["needs_edit_risk_case", "priority_flags:" + flag]):
                covered_priority_flags.add(flag)
                break

    for row in prioritized_risk_rows:
        if sum(1 for item in selected.values() if item["row"]["quality_state"] == QUALITY_NEEDS_EDIT) >= RISK_TARGET_PER_WORKER:
            break
        reasons = ["needs_edit_risk_case"]
        matched_priority_flags = sorted(priority_flags & set(str(flag) for flag in row.get("quality_flags", [])))
        if matched_priority_flags:
            reasons.append("priority_flags:" + ",".join(matched_priority_flags))
        add_selection(selected, row, reasons)

    for row in choose_boundary_rows(worker_rows):
        if len(selected) >= PASS_TARGET_PER_WORKER + RISK_TARGET_PER_WORKER + BOUNDARY_TARGET_PER_WORKER:
            break
        add_selection(selected, row, ["boundary_or_representative"])

    all_rows_ranked = sorted(worker_rows, key=coverage_score, reverse=True)
    for row in all_rows_ranked:
        if len(selected) >= SAMPLES_PER_WORKER:
            break
        add_selection(selected, row, ["fallback_fill"])

    if len(selected) != SAMPLES_PER_WORKER:
        raise ValueError(f"worker {worker_id} expected {SAMPLES_PER_WORKER} samples but got {len(selected)}")

    ordered_selection = sorted(
        selected.values(),
        key=lambda item: (
            str(item["row"].get("file_type", "")),
            str(item["row"].get("writing_form", "")),
            str(item["row"].get("topic_id", "")),
        ),
    )
    sample_records: list[dict[str, Any]] = []
    worker_code = worker_id.replace("-", "")
    for index, item in enumerate(ordered_selection, start=1):
        sample_records.append(build_sample_record(f"B05-TSR-{worker_code}-{index:03d}", item["row"], item["reasons"]))

    worker_summary = {
        "sampled_total": len(sample_records),
        "sampled_quality_pass": sum(1 for record in sample_records if record["review_state_from_quality"] == QUALITY_PASS),
        "sampled_needs_edit": sum(1 for record in sample_records if record["review_state_from_quality"] == QUALITY_NEEDS_EDIT),
        "sampled_file_type_counts": dict(sorted(Counter(record["file_type"] for record in sample_records).items())),
        "sampled_risk_flag_counts": dict(sorted(Counter(flag for record in sample_records for flag in record["risk_flags"]).items())),
        "writing_forms": sorted({record["writing_form"] for record in sample_records}),
        "concrete_anchors": sorted({record["concrete_anchor"] for record in sample_records}),
    }
    return sample_records, worker_summary


def build_summary(quality_summary: dict[str, Any], sample_records: list[dict[str, Any]], worker_summaries: dict[str, Any]) -> dict[str, Any]:
    sampled_worker_counts = Counter(record["worker_id"] for record in sample_records)
    sampled_quality_state_counts = Counter(record["review_state_from_quality"] for record in sample_records)
    sampled_file_type_counts = Counter(record["file_type"] for record in sample_records)
    sampled_risk_flag_counts = Counter(flag for record in sample_records for flag in record["risk_flags"])
    return {
        "batch_root": BATCH_ROOT.relative_to(PROJECT_ROOT).as_posix(),
        "source_quality_manifest_path": QUALITY_MANIFEST_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "source_quality_summary_path": QUALITY_SUMMARY_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "d19_2_quality_gate_status": quality_summary.get("quality_gate_status"),
        "target_total_samples": len(WORKER_IDS) * SAMPLES_PER_WORKER,
        "sampled_total_files": len(sample_records),
        "sampled_worker_counts": dict(sorted(sampled_worker_counts.items())),
        "sampled_quality_state_counts": dict(sorted(sampled_quality_state_counts.items())),
        "sampled_file_type_counts": dict(sorted(sampled_file_type_counts.items())),
        "sampled_risk_flag_counts": dict(sorted(sampled_risk_flag_counts.items())),
        "worker_sampling_results": worker_summaries,
        "notes": [
            "Each worker contributes 20 samples: 10 quality_pass representatives, 5 needs_edit risk cases, and 5 boundary/representative files.",
            "Sampling joins the quality-review manifest back to the validation manifest so writing_form and concrete_anchor remain available to human reviewers.",
            "CC-2, CC-5, and CC-6 prioritize their known residual risk clusters from D19.2.",
        ],
    }


def main() -> int:
    quality_summary = load_quality_summary()
    merged_rows = merge_rows()

    rows_by_worker: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in merged_rows:
        rows_by_worker[str(row["worker_id"])].append(row)

    missing_workers = sorted(set(WORKER_IDS) - set(rows_by_worker))
    if missing_workers:
        raise ValueError(f"missing workers in merged manifest: {', '.join(missing_workers)}")

    sample_records: list[dict[str, Any]] = []
    worker_summaries: dict[str, Any] = {}
    for worker_id in WORKER_IDS:
        records, worker_summary = sample_worker_rows(rows_by_worker[worker_id])
        sample_records.extend(records)
        worker_summaries[worker_id] = worker_summary

    summary = build_summary(quality_summary, sample_records, worker_summaries)
    SAMPLING_MANIFEST_PATH.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in sample_records),
        encoding="utf-8",
    )
    SAMPLING_SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"sampled_total_files={summary['sampled_total_files']}")
    print("sampled_worker_counts=" + json.dumps(summary["sampled_worker_counts"], ensure_ascii=False, sort_keys=True))
    print("sampled_quality_state_counts=" + json.dumps(summary["sampled_quality_state_counts"], ensure_ascii=False, sort_keys=True))
    print("sampled_risk_flag_counts=" + json.dumps(summary["sampled_risk_flag_counts"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
