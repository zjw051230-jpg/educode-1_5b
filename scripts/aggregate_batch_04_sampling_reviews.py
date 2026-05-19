from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from validate_draft_corpus_batch_03 import PROJECT_ROOT, parse_jsonl_registry

BATCH_ROOT = PROJECT_ROOT / "data" / "real_corpus" / "draft_queue" / "domain_synthetic_batch_04"
REVIEWS_ROOT = BATCH_ROOT / "reviews"
OUTPUT_JSON_PATH = REVIEWS_ROOT / "batch_04_sampling_review_aggregate.json"
OUTPUT_JSONL_PATH = REVIEWS_ROOT / "batch_04_sampling_review_aggregate.jsonl"
WORKER_IDS = ["CC-1", "CC-2", "CC-3", "CC-4", "CC-5", "CC-6"]
EXPECTED_RECORDS_PER_WORKER = 40
EXPECTED_TOTAL_RECORDS = 240
PROMOTION_READY_DECISION = "ready_for_promotion_subset"
PROMOTION_NOT_READY_DECISION = "not_ready_for_promotion"
DIMENSION_FIELDS = [
    "educational_value",
    "practical_usefulness",
    "domain_backbone_alignment",
    "external_copy_risk",
    "misleading_claim_risk",
]
RISK_SCORE_MAP = {
    "low": 1,
    "medium": 2,
    "high": 3,
}


def review_path_for_worker(worker_id: str) -> Path:
    return REVIEWS_ROOT / f"{worker_id}_sampling_review.jsonl"



def load_worker_rows(worker_id: str) -> list[dict[str, Any]]:
    path = review_path_for_worker(worker_id)
    rows, errors = parse_jsonl_registry(path)
    if errors:
        raise ValueError(f"{path.relative_to(PROJECT_ROOT).as_posix()}: {'; '.join(errors)}")
    if len(rows) != EXPECTED_RECORDS_PER_WORKER:
        raise ValueError(
            f"worker {worker_id} expected {EXPECTED_RECORDS_PER_WORKER} review rows but found {len(rows)}"
        )
    return rows



def validate_row(worker_id: str, row: dict[str, Any], index: int) -> None:
    observed_worker = str(row.get("worker_id", "")).strip()
    if observed_worker != worker_id:
        raise ValueError(
            f"worker {worker_id} row {index} has mismatched worker_id {observed_worker!r}"
        )
    decision = str(row.get("recommended_decision", "")).strip()
    if not decision:
        raise ValueError(f"worker {worker_id} row {index} is missing recommended_decision")
    template_risk = str(row.get("template_repetition_risk", "")).strip().lower()
    if template_risk not in RISK_SCORE_MAP:
        raise ValueError(
            f"worker {worker_id} row {index} has invalid template_repetition_risk {template_risk!r}"
        )
    for field in DIMENSION_FIELDS:
        value = str(row.get(field, "")).strip().lower()
        if value not in {"low", "medium", "high"}:
            raise ValueError(f"worker {worker_id} row {index} has invalid {field} value {value!r}")



def distribution(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts = Counter(str(row.get(field, "")).strip().lower() for row in rows)
    return {label: counts.get(label, 0) for label in ("low", "medium", "high")}



def average_template_repetition_risk(rows: list[dict[str, Any]]) -> float:
    scores = [RISK_SCORE_MAP[str(row["template_repetition_risk"]).strip().lower()] for row in rows]
    return round(mean(scores), 2)



def build_worker_summary(worker_id: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    decision_counts = Counter(str(row["recommended_decision"]).strip() for row in rows)
    return {
        "records": len(rows),
        "decision_counts": dict(sorted(decision_counts.items())),
        "average_template_repetition_risk": average_template_repetition_risk(rows),
        "educational_value_distribution": distribution(rows, "educational_value"),
        "practical_usefulness_distribution": distribution(rows, "practical_usefulness"),
        "domain_backbone_alignment_distribution": distribution(rows, "domain_backbone_alignment"),
        "external_copy_risk_distribution": distribution(rows, "external_copy_risk"),
        "misleading_claim_risk_distribution": distribution(rows, "misleading_claim_risk"),
    }



def compute_promotion_readiness(decision_counts: Counter[str], reviewed_samples: int) -> str:
    strong_count = decision_counts.get("strong_candidate_for_promotion", 0)
    needs_rewrite_count = decision_counts.get("needs_rewrite", 0)
    needs_rewrite_rate = needs_rewrite_count / reviewed_samples if reviewed_samples else 1.0
    if strong_count > 0 and needs_rewrite_rate <= 0.25:
        return PROMOTION_READY_DECISION
    return PROMOTION_NOT_READY_DECISION



def build_aggregate(worker_rows: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    all_rows = [row for rows in worker_rows.values() for row in rows]
    if len(all_rows) != EXPECTED_TOTAL_RECORDS:
        raise ValueError(f"expected {EXPECTED_TOTAL_RECORDS} total review rows but found {len(all_rows)}")

    decision_counts = Counter(str(row["recommended_decision"]).strip() for row in all_rows)
    reviewed_samples = len(all_rows)
    needs_rewrite_count = decision_counts.get("needs_rewrite", 0)

    aggregate = {
        "batch_root": BATCH_ROOT.relative_to(PROJECT_ROOT).as_posix(),
        "reviews_root": REVIEWS_ROOT.relative_to(PROJECT_ROOT).as_posix(),
        "review_input_files": [review_path_for_worker(worker_id).relative_to(PROJECT_ROOT).as_posix() for worker_id in WORKER_IDS],
        "expected_records_per_worker": EXPECTED_RECORDS_PER_WORKER,
        "expected_total_records": EXPECTED_TOTAL_RECORDS,
        "reviewed_samples": reviewed_samples,
        "decision_counts": {
            "strong_candidate_for_promotion": decision_counts.get("strong_candidate_for_promotion", 0),
            "keep_as_candidate": decision_counts.get("keep_as_candidate", 0),
            "needs_rewrite": needs_rewrite_count,
            "reject": decision_counts.get("reject", 0),
        },
        "needs_rewrite_rate": round(needs_rewrite_count / reviewed_samples, 4),
        "promotion_readiness": compute_promotion_readiness(decision_counts, reviewed_samples),
        "decision_counts_by_worker": {
            worker_id: build_worker_summary(worker_id, worker_rows[worker_id])["decision_counts"]
            for worker_id in WORKER_IDS
        },
        "average_template_repetition_risk_by_worker": {
            worker_id: build_worker_summary(worker_id, worker_rows[worker_id])["average_template_repetition_risk"]
            for worker_id in WORKER_IDS
        },
        "educational_value_distribution": distribution(all_rows, "educational_value"),
        "practical_usefulness_distribution": distribution(all_rows, "practical_usefulness"),
        "domain_backbone_alignment_distribution": distribution(all_rows, "domain_backbone_alignment"),
        "external_copy_risk_distribution": distribution(all_rows, "external_copy_risk"),
        "misleading_claim_risk_distribution": distribution(all_rows, "misleading_claim_risk"),
        "worker_summaries": {
            worker_id: build_worker_summary(worker_id, worker_rows[worker_id])
            for worker_id in WORKER_IDS
        },
        "quality_summary": {
            "main_problem": "quality/template repetition",
            "promotion_blocker": "strong promotion candidates were not found and needs_rewrite dominates the reviewed sample",
        },
    }
    return aggregate



def write_outputs(aggregate: dict[str, Any]) -> None:
    OUTPUT_JSON_PATH.write_text(json.dumps(aggregate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    jsonl_rows = [
        {
            "record_type": "batch_summary",
            **aggregate,
        }
    ]
    OUTPUT_JSONL_PATH.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in jsonl_rows),
        encoding="utf-8",
    )



def main() -> int:
    worker_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for worker_id in WORKER_IDS:
        rows = load_worker_rows(worker_id)
        for index, row in enumerate(rows, start=1):
            validate_row(worker_id, row, index)
        worker_rows[worker_id] = rows

    aggregate = build_aggregate(worker_rows)
    write_outputs(aggregate)

    print(f"reviewed_samples={aggregate['reviewed_samples']}")
    print(f"promotion_readiness={aggregate['promotion_readiness']}")
    print("decision_counts=" + json.dumps(aggregate["decision_counts"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
