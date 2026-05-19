from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from validate_draft_corpus_batch_03 import PROJECT_ROOT, parse_jsonl_registry, read_metadata

BATCH_ROOT = PROJECT_ROOT / "data" / "real_corpus" / "draft_queue" / "domain_synthetic_batch_05"
SAMPLING_MANIFEST_PATH = BATCH_ROOT / "batch_05_targeted_sampling_manifest.jsonl"
REVIEW_MANIFEST_PATH = BATCH_ROOT / "batch_05_targeted_sample_review_manifest.jsonl"
REVIEW_SUMMARY_PATH = BATCH_ROOT / "batch_05_targeted_sample_review_summary.json"

HIGH = "high"
MEDIUM = "medium"
LOW = "low"
NA = "not_applicable"
STRONG = "strong_candidate_for_promotion"
KEEP = "keep_as_candidate"
REWRITE = "needs_rewrite"
REJECT = "reject"


def load_sampling_rows() -> list[dict[str, Any]]:
    rows, errors = parse_jsonl_registry(SAMPLING_MANIFEST_PATH)
    if errors:
        raise ValueError("; ".join(errors))
    return rows


def score_topic_specificity(row: dict[str, Any], text: str) -> str:
    quality_state = str(row.get("review_state_from_quality"))
    risk_flags = set(str(flag) for flag in row.get("risk_flags", []))
    if quality_state == "quality_pass" and len(text) >= 1200:
        return HIGH
    if "trace_note_residue" in risk_flags:
        return HIGH
    if quality_state == "needs_edit":
        return MEDIUM
    return MEDIUM


def score_concrete_anchor_quality(row: dict[str, Any]) -> str:
    anchor = str(row.get("concrete_anchor", "")).strip().lower()
    if not anchor:
        return LOW
    if anchor in {"tensor shape", "numeric toy example", "before/after comparison", "failure scenario", "debugging transcript", "metrics interpretation", "schema mismatch", "repair checklist", "mini code trace", "decision checklist", "small pseudo-run log", "config snippet"}:
        return HIGH
    return MEDIUM


def score_template_repetition_risk(row: dict[str, Any]) -> str:
    flags = set(str(flag) for flag in row.get("risk_flags", []))
    if "repeated_internal_line" in flags or "trace_note_residue" in flags:
        return HIGH
    if "thin_section_structure" in flags or "bilingual_pairing_missing" in flags:
        return MEDIUM
    return LOW


def score_educational_value(row: dict[str, Any], topic_specificity: str, anchor_quality: str) -> str:
    if topic_specificity == HIGH and anchor_quality == HIGH:
        return HIGH
    if topic_specificity == LOW or anchor_quality == LOW:
        return MEDIUM
    return MEDIUM


def score_python_topic_fit(row: dict[str, Any], text: str) -> str:
    if str(row.get("file_type")) != "python":
        return NA
    if "trace_note_residue" in set(str(flag) for flag in row.get("risk_flags", [])):
        return HIGH
    if "def topic_action" in text or "def main" in text:
        return HIGH
    return MEDIUM


def score_bilingual_quality(row: dict[str, Any], text: str) -> str:
    if str(row.get("worker_id")) != "CC-5" or str(row.get("file_type")) != "markdown":
        return NA
    flags = set(str(flag) for flag in row.get("risk_flags", []))
    if "bilingual_pairing_missing" in flags:
        return LOW
    if "EN:" in text and any("一" <= char <= "鿿" for char in text):
        return HIGH
    return MEDIUM


def decide_promotion(
    metadata_ok: bool,
    topic_specificity: str,
    concrete_anchor_quality: str,
    template_repetition_risk: str,
    educational_value: str,
) -> str:
    if not metadata_ok:
        return REJECT
    if (
        topic_specificity == HIGH
        and concrete_anchor_quality == HIGH
        and template_repetition_risk == LOW
        and educational_value == HIGH
    ):
        return STRONG
    if template_repetition_risk == HIGH:
        return REWRITE
    return KEEP


def build_review_notes(
    row: dict[str, Any],
    topic_specificity: str,
    concrete_anchor_quality: str,
    template_repetition_risk: str,
    promotion_decision: str,
) -> str:
    notes: list[str] = []
    if row.get("risk_flags"):
        notes.append("quality-review flags carried into sampling: " + ", ".join(str(flag) for flag in row["risk_flags"]))
    notes.append(f"topic_specificity={topic_specificity}")
    notes.append(f"concrete_anchor_quality={concrete_anchor_quality}")
    notes.append(f"template_repetition_risk={template_repetition_risk}")
    notes.append(f"promotion_decision={promotion_decision}")
    return "; ".join(notes)


def review_row(row: dict[str, Any]) -> dict[str, Any]:
    file_path = PROJECT_ROOT / str(row["file_path"])
    text = file_path.read_text(encoding="utf-8")
    metadata, metadata_error = read_metadata(file_path, str(row["file_type"]))
    metadata_ok = metadata_error is None and metadata.get("topic_id") == row["topic_id"]
    topic_specificity = score_topic_specificity(row, text)
    concrete_anchor_quality = score_concrete_anchor_quality(row)
    template_repetition_risk = score_template_repetition_risk(row)
    educational_value = score_educational_value(row, topic_specificity, concrete_anchor_quality)
    python_topic_fit = score_python_topic_fit(row, text)
    bilingual_quality = score_bilingual_quality(row, text)
    promotion_decision = decide_promotion(
        metadata_ok,
        topic_specificity,
        concrete_anchor_quality,
        template_repetition_risk,
        educational_value,
    )
    review_notes = build_review_notes(
        row,
        topic_specificity,
        concrete_anchor_quality,
        template_repetition_risk,
        promotion_decision,
    )
    return {
        "sample_id": row["sample_id"],
        "topic_id": row["topic_id"],
        "worker_id": row["worker_id"],
        "file_path": row["file_path"],
        "file_type": row["file_type"],
        "metadata_ok": metadata_ok,
        "topic_specificity": topic_specificity,
        "concrete_anchor_quality": concrete_anchor_quality,
        "template_repetition_risk": template_repetition_risk,
        "educational_value": educational_value,
        "python_topic_fit": python_topic_fit,
        "bilingual_quality": bilingual_quality,
        "promotion_decision": promotion_decision,
        "review_notes": review_notes,
    }


def build_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    decision_counts = Counter(record["promotion_decision"] for record in records)
    worker_decision_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        worker_decision_counts[record["worker_id"]][record["promotion_decision"]] += 1
    strong_count = decision_counts[STRONG]
    promotion_readiness = "may_support_small_promotion_subset" if strong_count >= 60 and decision_counts[REJECT] == 0 else "still_needs_another_repair_pass"
    return {
        "batch_root": BATCH_ROOT.relative_to(PROJECT_ROOT).as_posix(),
        "source_sampling_manifest_path": SAMPLING_MANIFEST_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "total_reviewed_samples": len(records),
        "strong_candidate_for_promotion_count": decision_counts[STRONG],
        "keep_as_candidate_count": decision_counts[KEEP],
        "needs_rewrite_count": decision_counts[REWRITE],
        "reject_count": decision_counts[REJECT],
        "promotion_readiness": promotion_readiness,
        "worker_decision_counts": {
            worker_id: dict(sorted(counter.items()))
            for worker_id, counter in sorted(worker_decision_counts.items())
        },
        "review_samples": {
            "strong_examples": [
                {"topic_id": record["topic_id"], "file_path": record["file_path"]}
                for record in records
                if record["promotion_decision"] == STRONG
            ][:20],
            "rewrite_examples": [
                {"topic_id": record["topic_id"], "file_path": record["file_path"], "review_notes": record["review_notes"]}
                for record in records
                if record["promotion_decision"] == REWRITE
            ][:20],
        },
    }


def main() -> int:
    sampling_rows = load_sampling_rows()
    records = [review_row(row) for row in sampling_rows]
    REVIEW_MANIFEST_PATH.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )
    summary = build_summary(records)
    REVIEW_SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"total_reviewed_samples={summary['total_reviewed_samples']}")
    print(f"strong_candidate_for_promotion_count={summary['strong_candidate_for_promotion_count']}")
    print(f"keep_as_candidate_count={summary['keep_as_candidate_count']}")
    print(f"needs_rewrite_count={summary['needs_rewrite_count']}")
    print(f"reject_count={summary['reject_count']}")
    print(f"promotion_readiness={summary['promotion_readiness']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
