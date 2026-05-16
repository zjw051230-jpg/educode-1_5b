from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SYNTHETIC_PROCESSED_PATH = PROJECT_ROOT / "data" / "real_corpus" / "processed" / "synthetic_expanded.processed.jsonl"
EXTERNAL_PROCESSED_PATH = PROJECT_ROOT / "data" / "real_corpus" / "processed" / "external_general_text.processed.jsonl"
SYNTHETIC_MANIFEST_PATH = PROJECT_ROOT / "data" / "real_corpus" / "metadata" / "source_manifest.synthetic_expanded.jsonl"
EXTERNAL_MANIFEST_PATH = PROJECT_ROOT / "data" / "real_corpus" / "metadata" / "source_manifest.external_general_text.jsonl"
MIXED_PROCESSED_PATH = PROJECT_ROOT / "data" / "real_corpus" / "processed" / "mixed_domain_external.processed.jsonl"
MIXED_TRAIN_PATH = PROJECT_ROOT / "data" / "real_corpus" / "splits" / "mixed_domain_external.train.jsonl"
MIXED_VAL_PATH = PROJECT_ROOT / "data" / "real_corpus" / "splits" / "mixed_domain_external.val.jsonl"
SUMMARY_PATH = PROJECT_ROOT / "data" / "real_corpus" / "metadata" / "mixed_domain_external.mix_summary.json"

MIXED_CORPUS_ID = "mixed_domain_external_000001"
MIXED_STAGE = "D13.1"
SHUFFLE_SEED = 1337
PROJECT_BACKBONE = "CS/ML/Python/Transformer training systems education"
EXPECTED_EXTERNAL_SOURCE_CATEGORY = "external_general_text"
EXPECTED_EXTERNAL_PROJECT_ROLE = "supplement_only_not_project_backbone"


def read_single_jsonl_record(path: Path) -> dict[str, Any]:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) != 1:
        raise ValueError(f"expected exactly one JSONL record in {path}, found {len(lines)}")
    return json.loads(lines[0])



def read_jsonl_records(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]



def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")



def validate_synthetic_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("allowed_for_training") is not True:
        raise ValueError("synthetic_expanded manifest allowed_for_training must be true")



def validate_external_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("allowed_for_training") is not True:
        raise ValueError("external_general_text manifest allowed_for_training must be true")
    if manifest.get("source_category") != EXPECTED_EXTERNAL_SOURCE_CATEGORY:
        raise ValueError(
            f"external_general_text manifest source_category must be {EXPECTED_EXTERNAL_SOURCE_CATEGORY}, got {manifest.get('source_category')}"
        )
    if manifest.get("project_role") != EXPECTED_EXTERNAL_PROJECT_ROLE:
        raise ValueError(
            f"external_general_text manifest project_role must be {EXPECTED_EXTERNAL_PROJECT_ROLE}, got {manifest.get('project_role')}"
        )

    scope_text = " ".join(
        [
            str(manifest.get("approval_status", "")),
            str(manifest.get("training_use_scope", "")),
            str(manifest.get("notes", "")),
        ]
    ).lower()
    required_scope_terms = ["bounded", "supplement", "tokenizer"]
    missing_terms = [term for term in required_scope_terms if term not in scope_text]
    if missing_terms:
        raise ValueError(
            "external_general_text approval scope must retain bounded/tokenizer/supplement limits; "
            f"missing terms: {', '.join(missing_terms)}"
        )



def validate_processed_records(
    records: list[dict[str, Any]],
    *,
    expected_source_id: str,
    expected_source_category: str,
    label: str,
) -> None:
    if not records:
        raise ValueError(f"{label} processed records are empty")

    for record in records:
        if record.get("source_id") != expected_source_id:
            raise ValueError(f"{label} record has unexpected source_id: {record.get('source_id')}")
        if record.get("source_category") != expected_source_category:
            raise ValueError(
                f"{label} record has unexpected source_category: {record.get('source_category')}"
            )
        if record.get("split") not in {"train", "val"}:
            raise ValueError(f"{label} record has invalid split: {record.get('split')}")
        text = record.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"{label} record text must be a non-empty string")



def shuffle_records(records: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    shuffled = list(records)
    random.Random(seed).shuffle(shuffled)
    return shuffled



def build_mixed_record(record: dict[str, Any], mixed_index: int) -> dict[str, Any]:
    mixed_record = dict(record)
    metadata = dict(record.get("metadata") or {})

    original_processed_id = str(record["id"])
    mixed_record_id = f"{MIXED_CORPUS_ID}_doc_{mixed_index:04d}"

    metadata["mixed_stage"] = MIXED_STAGE
    metadata["project_backbone"] = PROJECT_BACKBONE

    mixed_record["id"] = mixed_record_id
    mixed_record["mixed_corpus_id"] = MIXED_CORPUS_ID
    mixed_record["original_processed_id"] = original_processed_id
    mixed_record["metadata"] = metadata
    return mixed_record



def count_by_source_category(records: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        source_category = str(record["source_category"])
        counts[source_category] = counts.get(source_category, 0) + 1
    return counts



def main() -> int:
    synthetic_manifest = read_single_jsonl_record(SYNTHETIC_MANIFEST_PATH)
    external_manifest = read_single_jsonl_record(EXTERNAL_MANIFEST_PATH)

    validate_synthetic_manifest(synthetic_manifest)
    validate_external_manifest(external_manifest)

    synthetic_records = read_jsonl_records(SYNTHETIC_PROCESSED_PATH)
    external_records = read_jsonl_records(EXTERNAL_PROCESSED_PATH)

    validate_processed_records(
        synthetic_records,
        expected_source_id=str(synthetic_manifest["source_id"]),
        expected_source_category=str(synthetic_manifest["source_category"]),
        label="synthetic_expanded",
    )
    validate_processed_records(
        external_records,
        expected_source_id=str(external_manifest["source_id"]),
        expected_source_category=EXPECTED_EXTERNAL_SOURCE_CATEGORY,
        label="external_general_text",
    )

    train_source_records = [record for record in synthetic_records + external_records if record["split"] == "train"]
    val_source_records = [record for record in synthetic_records + external_records if record["split"] == "val"]

    shuffled_train_records = shuffle_records(train_source_records, SHUFFLE_SEED)
    shuffled_val_records = shuffle_records(val_source_records, SHUFFLE_SEED)

    mixed_train_records: list[dict[str, Any]] = []
    mixed_val_records: list[dict[str, Any]] = []
    next_index = 1

    for record in shuffled_train_records:
        mixed_train_records.append(build_mixed_record(record, next_index))
        next_index += 1

    for record in shuffled_val_records:
        mixed_val_records.append(build_mixed_record(record, next_index))
        next_index += 1

    mixed_processed_records = mixed_train_records + mixed_val_records

    source_counts = count_by_source_category(mixed_processed_records)
    train_source_counts = count_by_source_category(mixed_train_records)
    val_source_counts = count_by_source_category(mixed_val_records)
    total_chars = sum(len(record["text"]) for record in mixed_processed_records)

    summary = {
        "mixed_corpus_id": MIXED_CORPUS_ID,
        "mixed_stage": MIXED_STAGE,
        "seed": SHUFFLE_SEED,
        "project_backbone": PROJECT_BACKBONE,
        "external_general_text_is_supplement": True,
        "total_docs": len(mixed_processed_records),
        "train_docs": len(mixed_train_records),
        "val_docs": len(mixed_val_records),
        "synthetic_docs": len(synthetic_records),
        "external_docs": len(external_records),
        "total_chars": total_chars,
        "source_counts": source_counts,
        "train_source_counts": train_source_counts,
        "val_source_counts": val_source_counts,
        "source_categories": sorted(source_counts),
        "inputs": {
            "synthetic_processed": SYNTHETIC_PROCESSED_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "external_processed": EXTERNAL_PROCESSED_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "synthetic_manifest": SYNTHETIC_MANIFEST_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "external_manifest": EXTERNAL_MANIFEST_PATH.relative_to(PROJECT_ROOT).as_posix(),
        },
        "split_policy": {
            "preserve_original_split": True,
            "train_docs_remain_train": True,
            "val_docs_remain_val": True,
            "shuffle_within_split_only": True,
            "document_level_split": True,
        },
        "manifest_validation": {
            "synthetic_allowed_for_training": synthetic_manifest.get("allowed_for_training") is True,
            "external_allowed_for_training": external_manifest.get("allowed_for_training") is True,
            "external_source_category": external_manifest.get("source_category"),
            "external_training_use_scope": external_manifest.get("training_use_scope"),
            "external_approval_status": external_manifest.get("approval_status"),
        },
        "outputs": {
            "processed_jsonl": MIXED_PROCESSED_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "train_jsonl": MIXED_TRAIN_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "val_jsonl": MIXED_VAL_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "summary_json": SUMMARY_PATH.relative_to(PROJECT_ROOT).as_posix(),
        },
    }

    write_jsonl(MIXED_PROCESSED_PATH, mixed_processed_records)
    write_jsonl(MIXED_TRAIN_PATH, mixed_train_records)
    write_jsonl(MIXED_VAL_PATH, mixed_val_records)
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"mixed_corpus_id: {MIXED_CORPUS_ID}")
    print(f"total_docs: {summary['total_docs']}")
    print(f"train_docs: {summary['train_docs']}")
    print(f"val_docs: {summary['val_docs']}")
    print(f"synthetic_docs: {summary['synthetic_docs']}")
    print(f"external_docs: {summary['external_docs']}")
    print(f"source_categories: {', '.join(summary['source_categories'])}")
    print(f"processed_output: {summary['outputs']['processed_jsonl']}")
    print(f"train_output: {summary['outputs']['train_jsonl']}")
    print(f"val_output: {summary['outputs']['val_jsonl']}")
    print(f"summary_output: {summary['outputs']['summary_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
