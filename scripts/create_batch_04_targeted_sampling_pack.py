from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from validate_draft_corpus_batch_03 import PROJECT_ROOT, parse_jsonl_registry

BATCH_ROOT = PROJECT_ROOT / "data" / "real_corpus" / "draft_queue" / "domain_synthetic_batch_04"
QUALITY_MANIFEST_PATH = BATCH_ROOT / "batch_04_quality_review_manifest.jsonl"
QUALITY_SUMMARY_PATH = BATCH_ROOT / "batch_04_quality_review_summary.json"
SAMPLING_MANIFEST_PATH = BATCH_ROOT / "batch_04_targeted_sampling_manifest.jsonl"
SAMPLING_SUMMARY_PATH = BATCH_ROOT / "batch_04_targeted_sampling_summary.json"

QUALITY_PASS = "quality_pass"
QUALITY_NEEDS_EDIT = "needs_edit"
HIGH_RISK_FLAGS = (
    "boilerplate_density_high",
    "templated_opening_family",
    "repeated_internal_line",
)
WORKER_PRIORITY = ["CC-2", "CC-3", "CC-5", "CC-6", "CC-1", "CC-4"]
WORKER_SAMPLE_TARGETS = {
    "CC-1": {
        "total": 40,
        "quality_pass": 20,
        "risk": 20,
        "markdown_focus": False,
        "primary_pool": "quality_pass",
        "fallback_order": ["quality_pass", "risk"],
    },
    "CC-2": {
        "total": 40,
        "quality_pass": 10,
        "risk": 30,
        "markdown_focus": False,
        "primary_pool": "risk",
        "fallback_order": ["risk", "quality_pass"],
    },
    "CC-3": {
        "total": 40,
        "quality_pass": 10,
        "risk": 30,
        "markdown_focus": False,
        "primary_pool": "risk",
        "fallback_order": ["risk", "quality_pass"],
    },
    "CC-4": {
        "total": 40,
        "quality_pass": 20,
        "risk": 20,
        "markdown_focus": False,
        "primary_pool": "quality_pass",
        "fallback_order": ["quality_pass", "risk"],
    },
    "CC-5": {
        "total": 40,
        "quality_pass": 10,
        "risk": 30,
        "markdown_focus": True,
        "primary_pool": "risk",
        "fallback_order": ["risk", "quality_pass"],
    },
    "CC-6": {
        "total": 40,
        "quality_pass": 10,
        "risk": 30,
        "markdown_focus": True,
        "primary_pool": "risk",
        "fallback_order": ["risk", "quality_pass"],
    },
}


def load_quality_manifest() -> list[dict[str, Any]]:
    rows, errors = parse_jsonl_registry(QUALITY_MANIFEST_PATH)
    if errors:
        raise ValueError("; ".join(errors))
    return rows



def load_quality_summary() -> dict[str, Any]:
    return json.loads(QUALITY_SUMMARY_PATH.read_text(encoding="utf-8"))



def is_risk_row(row: dict[str, Any]) -> bool:
    flags = set(str(flag) for flag in row.get("quality_flags", []))
    return str(row.get("quality_state")) != QUALITY_PASS or any(flag in flags for flag in HIGH_RISK_FLAGS)



def risk_sort_key(row: dict[str, Any], markdown_focus: bool) -> tuple[Any, ...]:
    flags = set(str(flag) for flag in row.get("quality_flags", []))
    return (
        1 if str(row.get("quality_state")) == QUALITY_NEEDS_EDIT else 0,
        1 if "boilerplate_density_high" in flags else 0,
        1 if "templated_opening_family" in flags else 0,
        1 if "repeated_internal_line" in flags else 0,
        1 if markdown_focus and str(row.get("file_type")) == "markdown" else 0,
        len(flags),
        int(row.get("line_count", 0)),
        int(row.get("char_count", 0)),
        str(row.get("topic_id", "")),
    )



def pass_sort_key(row: dict[str, Any], markdown_focus: bool) -> tuple[Any, ...]:
    return (
        1 if markdown_focus and str(row.get("file_type")) == "markdown" else 0,
        1 if str(row.get("file_type")) == "markdown" else 0,
        int(row.get("line_count", 0)),
        int(row.get("char_count", 0)),
        str(row.get("topic_id", "")),
    )



def combined_sort_key(row: dict[str, Any], markdown_focus: bool) -> tuple[Any, ...]:
    if is_risk_row(row):
        return (2,) + risk_sort_key(row, markdown_focus)
    return (1,) + pass_sort_key(row, markdown_focus)



def ranked_rows(rows: list[dict[str, Any]], pool_name: str, markdown_focus: bool) -> list[dict[str, Any]]:
    if pool_name == "risk":
        return sorted(rows, key=lambda row: risk_sort_key(row, markdown_focus), reverse=True)
    if pool_name == "quality_pass":
        return sorted(rows, key=lambda row: pass_sort_key(row, markdown_focus), reverse=True)
    return sorted(rows, key=lambda row: combined_sort_key(row, markdown_focus), reverse=True)



def add_reason(reason_list: list[str], reason: str) -> None:
    if reason not in reason_list:
        reason_list.append(reason)



def add_selection(
    selected: dict[str, dict[str, Any]],
    row: dict[str, Any],
    reasons: list[str],
) -> bool:
    file_path = str(row["file_path"])
    if file_path in selected:
        for reason in reasons:
            add_reason(selected[file_path]["reasons"], reason)
        return False
    selected[file_path] = {"row": row, "reasons": []}
    for reason in reasons:
        add_reason(selected[file_path]["reasons"], reason)
    return True



def count_selected_by_pool(selected: dict[str, dict[str, Any]], pool_name: str) -> int:
    count = 0
    for item in selected.values():
        row = item["row"]
        if pool_name == "quality_pass" and str(row.get("quality_state")) == QUALITY_PASS:
            count += 1
        elif pool_name == "risk" and is_risk_row(row):
            count += 1
    return count



def choose_subcategory_seed(
    rows: list[dict[str, Any]],
    target: dict[str, Any],
) -> dict[str, Any]:
    markdown_focus = bool(target["markdown_focus"])
    primary_pool = str(target["primary_pool"])
    candidate_orders: list[list[dict[str, Any]]] = []
    if primary_pool == "risk":
        candidate_orders.append(ranked_rows([row for row in rows if is_risk_row(row)], "risk", markdown_focus))
        candidate_orders.append(ranked_rows([row for row in rows if str(row.get("quality_state")) == QUALITY_PASS], "quality_pass", markdown_focus))
    else:
        candidate_orders.append(ranked_rows([row for row in rows if str(row.get("quality_state")) == QUALITY_PASS], "quality_pass", markdown_focus))
        candidate_orders.append(ranked_rows([row for row in rows if is_risk_row(row)], "risk", markdown_focus))
    candidate_orders.append(ranked_rows(rows, "all", markdown_focus))
    for ordered_rows in candidate_orders:
        if ordered_rows:
            return ordered_rows[0]
    raise ValueError("subcategory seed requested from empty row set")



def longest_row(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return max(rows, key=lambda row: (int(row.get("line_count", 0)), int(row.get("char_count", 0)), str(row.get("topic_id", ""))))



def shortest_row(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return min(rows, key=lambda row: (int(row.get("line_count", 0)), int(row.get("char_count", 0)), str(row.get("topic_id", ""))))



def primary_risk_flags(row: dict[str, Any]) -> list[str]:
    flags = [str(flag) for flag in row.get("quality_flags", [])]
    ordered = [flag for flag in HIGH_RISK_FLAGS if flag in flags]
    extras = [flag for flag in flags if flag not in ordered]
    return ordered + extras



def build_risk_reason(row: dict[str, Any]) -> str:
    flags = primary_risk_flags(row)
    if flags:
        return "risk_priority:" + ",".join(flags)
    return "risk_priority:needs_edit"



def build_review_focus(row: dict[str, Any]) -> str:
    focus_points: list[str] = []
    flags = set(str(flag) for flag in row.get("quality_flags", []))
    file_type = str(row.get("file_type"))
    worker_id = str(row.get("worker_id"))
    if "boilerplate_density_high" in flags:
        focus_points.append("Check whether review-note scaffolding overwhelms the teaching point and can be trimmed.")
    if "templated_opening_family" in flags:
        focus_points.append("Check whether the opening paragraph feels too close to nearby files from the same worker block.")
    if "repeated_internal_line" in flags:
        focus_points.append("Check for repeated internal lines or duplicated explanation fragments inside the file body.")
    if file_type == "markdown":
        focus_points.append("Check whether the markdown structure helps clarity instead of repeating boilerplate sections.")
    if file_type == "python":
        focus_points.append("Check whether the code example remains distinct, concise, and educational rather than formulaic.")
    if worker_id == "CC-5" and file_type == "markdown":
        focus_points.append("Check whether the bilingual pairing teaches the same idea clearly on both language sides.")
    if not focus_points:
        focus_points.append("Use this as a cleaner baseline and compare distinctness, drafting voice, and practical educational value against note-heavy samples.")
    return " ".join(focus_points[:3])



def build_sampling_record(sample_id: str, row: dict[str, Any], reasons: list[str]) -> dict[str, Any]:
    return {
        "sample_id": sample_id,
        "topic_id": row["topic_id"],
        "worker_id": row["worker_id"],
        "subcategory": row["subcategory"],
        "title": row["title"],
        "file_path": row["file_path"],
        "file_type": row["file_type"],
        "line_count": row["line_count"],
        "char_count": row["char_count"],
        "review_state_from_d18": row["quality_state"],
        "risk_flags": row["quality_flags"],
        "sample_reason": "; ".join(reasons),
        "suggested_review_focus": build_review_focus(row),
        "human_review_status": "pending",
    }



def sample_worker_rows(worker_rows: list[dict[str, Any]], target: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    worker_id = str(worker_rows[0]["worker_id"])
    markdown_focus = bool(target["markdown_focus"])
    total_target = int(target["total"])
    selected: dict[str, dict[str, Any]] = {}

    subcategory_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in worker_rows:
        subcategory_rows[str(row["subcategory"])] .append(row)
    for subcategory in sorted(subcategory_rows):
        seed = choose_subcategory_seed(subcategory_rows[subcategory], target)
        add_selection(selected, seed, ["subcategory_coverage"])

    add_selection(selected, longest_row(worker_rows), ["longest_file"])
    add_selection(selected, shortest_row(worker_rows), ["shortest_file"])

    pass_rows = [row for row in worker_rows if str(row.get("quality_state")) == QUALITY_PASS]
    risk_rows = [row for row in worker_rows if is_risk_row(row)]

    for row in ranked_rows(pass_rows, "quality_pass", markdown_focus):
        if count_selected_by_pool(selected, "quality_pass") >= int(target["quality_pass"]):
            break
        add_selection(selected, row, ["quality_pass_baseline"])

    for row in ranked_rows(risk_rows, "risk", markdown_focus):
        if count_selected_by_pool(selected, "risk") >= int(target["risk"]):
            break
        add_selection(selected, row, [build_risk_reason(row)])

    for pool_name in target["fallback_order"]:
        ordered_rows = ranked_rows(
            pass_rows if pool_name == "quality_pass" else risk_rows,
            pool_name,
            markdown_focus,
        )
        for row in ordered_rows:
            if len(selected) >= total_target:
                break
            add_selection(selected, row, [f"fallback_fill:{pool_name}"])
        if len(selected) >= total_target:
            break

    if len(selected) < total_target:
        for row in ranked_rows(worker_rows, "all", markdown_focus):
            if len(selected) >= total_target:
                break
            add_selection(selected, row, ["fallback_fill:any_available"])

    if len(selected) != total_target:
        raise ValueError(f"worker {worker_id} expected {total_target} samples but got {len(selected)}")

    ordered_selection = sorted(
        selected.values(),
        key=lambda item: (
            str(item["row"]["subcategory"]),
            -int(item["row"].get("line_count", 0)),
            str(item["row"]["topic_id"]),
        ),
    )
    sample_records: list[dict[str, Any]] = []
    worker_code = worker_id.replace("-", "")
    for index, item in enumerate(ordered_selection, start=1):
        sample_id = f"B04-TSR-{worker_code}-{index:03d}"
        sample_records.append(build_sampling_record(sample_id, item["row"], item["reasons"]))

    sampled_rows = [record for record in sample_records]
    sampled_state_counts = Counter(record["review_state_from_d18"] for record in sampled_rows)
    sampled_flag_counts = Counter(flag for record in sampled_rows for flag in record["risk_flags"])
    sampled_file_type_counts = Counter(record["file_type"] for record in sampled_rows)
    sampled_subcategories = sorted({record["subcategory"] for record in sampled_rows})
    fallback_fill_count = sum(1 for record in sampled_rows if "fallback_fill:" in record["sample_reason"])
    constraint_notes: list[str] = []
    if len(pass_rows) < int(target["quality_pass"]):
        constraint_notes.append(
            f"requested {target['quality_pass']} quality_pass samples but only {len(pass_rows)} were available"
        )
    if len(risk_rows) < int(target["risk"]):
        constraint_notes.append(f"requested {target['risk']} risk samples but only {len(risk_rows)} were available")

    result_summary = {
        "requested_total": total_target,
        "requested_quality_pass": int(target["quality_pass"]),
        "requested_risk": int(target["risk"]),
        "available_quality_pass": len(pass_rows),
        "available_risk": len(risk_rows),
        "sampled_total": len(sample_records),
        "sampled_quality_pass": sampled_state_counts.get(QUALITY_PASS, 0),
        "sampled_risk": sum(1 for record in sampled_rows if record["review_state_from_d18"] != QUALITY_PASS or record["risk_flags"]),
        "sampled_file_type_counts": dict(sorted(sampled_file_type_counts.items())),
        "sampled_flag_counts": dict(sorted(sampled_flag_counts.items())),
        "covered_subcategory_count": len(sampled_subcategories),
        "covered_subcategories": sampled_subcategories,
        "fallback_fill_count": fallback_fill_count,
        "constraint_notes": constraint_notes,
    }
    return sample_records, result_summary



def build_summary(
    quality_summary: dict[str, Any],
    sample_records: list[dict[str, Any]],
    worker_results: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    sampled_quality_state_counts = Counter(record["review_state_from_d18"] for record in sample_records)
    sampled_risk_flag_counts = Counter(flag for record in sample_records for flag in record["risk_flags"])
    sampled_file_type_counts = Counter(record["file_type"] for record in sample_records)
    sampled_worker_counts = Counter(record["worker_id"] for record in sample_records)
    high_risk_file_count = sum(1 for record in sample_records if record["risk_flags"])
    return {
        "batch_root": BATCH_ROOT.relative_to(PROJECT_ROOT).as_posix(),
        "source_quality_manifest_path": QUALITY_MANIFEST_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "source_quality_summary_path": QUALITY_SUMMARY_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "d18_quality_gate_status": quality_summary.get("quality_gate_status"),
        "d18_total_records": quality_summary.get("total_records"),
        "target_total_samples": sum(target["total"] for target in WORKER_SAMPLE_TARGETS.values()),
        "sampled_total_files": len(sample_records),
        "sampled_worker_counts": dict(sorted(sampled_worker_counts.items())),
        "sampled_quality_state_counts": dict(sorted(sampled_quality_state_counts.items())),
        "sampled_high_risk_file_count": high_risk_file_count,
        "sampled_risk_flag_counts": dict(sorted(sampled_risk_flag_counts.items())),
        "sampled_file_type_counts": dict(sorted(sampled_file_type_counts.items())),
        "worker_priority": WORKER_PRIORITY,
        "worker_sampling_targets": {
            worker_id: {
                "total": target["total"],
                "quality_pass": target["quality_pass"],
                "risk": target["risk"],
                "markdown_focus": target["markdown_focus"],
            }
            for worker_id, target in WORKER_SAMPLE_TARGETS.items()
        },
        "worker_sampling_results": worker_results,
        "notes": [
            "Worker-level pass/risk targets are treated as desired sampling shapes, with fallback fill from available within-worker records when D18 state availability makes an exact split impossible.",
            "CC-1 and CC-4 remain cleaner baseline workers with no D18 needs_edit records.",
            "CC-2 and CC-3 remain all-needs_edit workers with no D18 quality_pass records available for sampling.",
            "CC-5 and CC-6 prioritize markdown-heavy risk sampling while preserving a small clean-control slice from the available quality_pass subset.",
        ],
    }



def main() -> int:
    quality_rows = load_quality_manifest()
    quality_summary = load_quality_summary()

    worker_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in quality_rows:
        worker_rows[str(row["worker_id"])].append(row)

    missing_workers = sorted(set(WORKER_SAMPLE_TARGETS) - set(worker_rows))
    if missing_workers:
        raise ValueError(f"missing workers in quality manifest: {', '.join(missing_workers)}")

    sample_records: list[dict[str, Any]] = []
    worker_results: dict[str, dict[str, Any]] = {}
    for worker_id in sorted(WORKER_SAMPLE_TARGETS):
        records, worker_summary = sample_worker_rows(worker_rows[worker_id], WORKER_SAMPLE_TARGETS[worker_id])
        sample_records.extend(records)
        worker_results[worker_id] = worker_summary

    summary = build_summary(quality_summary, sample_records, worker_results)

    SAMPLING_MANIFEST_PATH.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in sample_records),
        encoding="utf-8",
    )
    SAMPLING_SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"sampled_total_files={summary['sampled_total_files']}")
    print(
        "sampled_worker_counts="
        + json.dumps(summary["sampled_worker_counts"], ensure_ascii=False, sort_keys=True)
    )
    print(
        "sampled_quality_state_counts="
        + json.dumps(summary["sampled_quality_state_counts"], ensure_ascii=False, sort_keys=True)
    )
    print(
        "sampled_risk_flag_counts="
        + json.dumps(summary["sampled_risk_flag_counts"], ensure_ascii=False, sort_keys=True)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
