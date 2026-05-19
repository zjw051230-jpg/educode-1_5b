from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from validate_draft_corpus_batch_03 import PROJECT_ROOT, parse_jsonl_registry, read_metadata

BATCH_ID = "domain_synthetic_batch_05"
BATCH_ROOT = PROJECT_ROOT / "data" / "real_corpus" / "draft_queue" / BATCH_ID
REVIEW_MANIFEST_PATH = BATCH_ROOT / "batch_05_targeted_sample_review_manifest.jsonl"
CANDIDATE_MANIFEST_PATH = BATCH_ROOT / "batch_05_promotion_subset_candidates.jsonl"
CANDIDATE_SUMMARY_PATH = BATCH_ROOT / "batch_05_promotion_subset_summary.json"

STRONG = "strong_candidate_for_promotion"
KEEP = "keep_as_candidate"
REWRITE = "needs_rewrite"
REJECT = "reject"
EXPECTED_SELECTED_COUNT = 92
FORMAL_PROMOTION_STATUS = "candidate_only_not_promoted"
REQUIRED_NEXT_STEP = "D20.2 formal promotion copy/review"


def load_review_rows() -> list[dict[str, Any]]:
    rows, errors = parse_jsonl_registry(REVIEW_MANIFEST_PATH)
    if errors:
        raise ValueError("; ".join(errors))
    return rows


def require_metadata_value(metadata: dict[str, str], key: str, expected_value: str, file_path: str) -> None:
    actual_value = metadata.get(key)
    if actual_value != expected_value:
        raise ValueError(
            f"{file_path} expected metadata {key}={expected_value!r} but found {actual_value!r}"
        )


def validate_selected_row(row: dict[str, Any]) -> dict[str, str]:
    file_path = PROJECT_ROOT / str(row["file_path"])
    if not file_path.exists():
        raise ValueError(f"missing selected file: {row['file_path']}")

    metadata, metadata_error = read_metadata(file_path, str(row["file_type"]))
    if metadata_error is not None:
        raise ValueError(f"{row['file_path']} metadata error: {metadata_error}")

    require_metadata_value(metadata, "batch_id", BATCH_ID, str(row["file_path"]))
    require_metadata_value(metadata, "approved_for_training", "false", str(row["file_path"]))
    require_metadata_value(metadata, "contains_external_text", "false", str(row["file_path"]))
    require_metadata_value(metadata, "contains_private_data", "false", str(row["file_path"]))
    require_metadata_value(metadata, "source_category", "synthetic_examples", str(row["file_path"]))

    topic_id = str(metadata.get("topic_id", "")).strip()
    worker_id = str(metadata.get("worker_id", "")).strip()
    if not topic_id:
        raise ValueError(f"{row['file_path']} missing topic_id metadata")
    if not worker_id:
        raise ValueError(f"{row['file_path']} missing worker_id metadata")
    if topic_id != str(row["topic_id"]):
        raise ValueError(f"{row['file_path']} topic_id mismatch: {topic_id} != {row['topic_id']}")
    if worker_id != str(row["worker_id"]):
        raise ValueError(f"{row['file_path']} worker_id mismatch: {worker_id} != {row['worker_id']}")
    return metadata


def build_candidate_record(index: int, row: dict[str, Any], metadata: dict[str, str]) -> dict[str, Any]:
    return {
        "candidate_id": f"B05-PSC-{index:03d}",
        "topic_id": row["topic_id"],
        "worker_id": row["worker_id"],
        "file_path": row["file_path"],
        "file_type": row["file_type"],
        "source_batch_id": metadata["batch_id"],
        "source_category": metadata["source_category"],
        "promotion_decision_from_d19_3": row["promotion_decision"],
        "selected_for_promotion_subset": True,
        "approved_for_training": False,
        "formal_promotion_status": FORMAL_PROMOTION_STATUS,
        "selection_reason": "Selected from D19.3 sampled review because promotion_decision == strong_candidate_for_promotion.",
        "required_next_step": REQUIRED_NEXT_STEP,
    }


def build_summary(review_rows: list[dict[str, Any]], candidate_rows: list[dict[str, Any]]) -> dict[str, Any]:
    decision_counts = Counter(str(row["promotion_decision"]) for row in review_rows)
    selected_by_worker = Counter(str(row["worker_id"]) for row in candidate_rows)
    selected_file_type_counts = Counter(str(row["file_type"]) for row in candidate_rows)
    return {
        "selected_count": len(candidate_rows),
        "excluded_keep_as_candidate": decision_counts[KEEP],
        "excluded_needs_rewrite": decision_counts[REWRITE],
        "excluded_reject": decision_counts[REJECT],
        "selected_by_worker": dict(sorted(selected_by_worker.items())),
        "selected_file_type_counts": dict(sorted(selected_file_type_counts.items())),
        "source_batch_id": BATCH_ID,
        "formal_promotion_done": False,
        "intake_done": False,
        "tokenizer_training_done": False,
        "model_training_done": False,
    }


def main() -> int:
    review_rows = load_review_rows()
    selected_review_rows = [row for row in review_rows if str(row.get("promotion_decision")) == STRONG]

    if len(selected_review_rows) != EXPECTED_SELECTED_COUNT:
        raise ValueError(
            f"expected {EXPECTED_SELECTED_COUNT} strong candidates but found {len(selected_review_rows)}"
        )

    candidate_rows: list[dict[str, Any]] = []
    for index, row in enumerate(selected_review_rows, start=1):
        metadata = validate_selected_row(row)
        candidate_rows.append(build_candidate_record(index, row, metadata))

    summary = build_summary(review_rows, candidate_rows)
    CANDIDATE_MANIFEST_PATH.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in candidate_rows),
        encoding="utf-8",
    )
    CANDIDATE_SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"selected_count={summary['selected_count']}")
    print("selected_by_worker=" + json.dumps(summary["selected_by_worker"], ensure_ascii=False, sort_keys=True))
    print(
        "selected_file_type_counts="
        + json.dumps(summary["selected_file_type_counts"], ensure_ascii=False, sort_keys=True)
    )
    print(f"excluded_keep_as_candidate={summary['excluded_keep_as_candidate']}")
    print(f"excluded_needs_rewrite={summary['excluded_needs_rewrite']}")
    print(f"excluded_reject={summary['excluded_reject']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
