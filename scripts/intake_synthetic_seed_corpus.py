from __future__ import annotations

import json
import random
import re
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "real_corpus" / "raw" / "synthetic_seed"
MANIFEST_PATH = PROJECT_ROOT / "data" / "real_corpus" / "metadata" / "source_manifest.synthetic_seed.jsonl"
PROCESSED_PATH = PROJECT_ROOT / "data" / "real_corpus" / "processed" / "synthetic_seed.processed.jsonl"
TRAIN_PATH = PROJECT_ROOT / "data" / "real_corpus" / "splits" / "synthetic_seed.train.jsonl"
VAL_PATH = PROJECT_ROOT / "data" / "real_corpus" / "splits" / "synthetic_seed.val.jsonl"
DROPPED_PATH = PROJECT_ROOT / "data" / "real_corpus" / "metadata" / "synthetic_seed.dropped_files.jsonl"
SUMMARY_PATH = PROJECT_ROOT / "data" / "real_corpus" / "metadata" / "synthetic_seed.intake_summary.json"

ALLOWED_SUFFIXES = {".md", ".txt", ".py"}
EXPECTED_SOURCE_ID = "source_synthetic_seed_000001"
SPLIT_SEED = 1337
VAL_RATIO = 0.10

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("api_key", re.compile(r"(?i)\bapi[_\- ]?key\b\s*[:=]")),
    ("secret", re.compile(r"(?i)\bsecret\b\s*[:=]")),
    ("password", re.compile(r"(?i)\bpassword\b\s*[:=]")),
    ("private_key", re.compile(r"(?i)(\bprivate[_\- ]?key\b\s*[:=]|-----BEGIN [A-Z ]*PRIVATE KEY-----)")),
    ("sk-", re.compile(r"\bsk-[A-Za-z0-9]{8,}\b")),
]


def load_manifest() -> dict[str, Any]:
    manifest_lines = MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
    non_empty_lines = [line for line in manifest_lines if line.strip()]
    if len(non_empty_lines) != 1:
        raise ValueError(f"expected exactly one manifest line, found {len(non_empty_lines)}")

    manifest = json.loads(non_empty_lines[0])

    if manifest.get("source_id") != EXPECTED_SOURCE_ID:
        raise ValueError(f"unexpected source_id: {manifest.get('source_id')}")
    if manifest.get("allowed_for_training") is not True:
        raise ValueError("manifest allowed_for_training must be true")
    if manifest.get("privacy_risk") != "none":
        raise ValueError(f"manifest privacy_risk must be none, got {manifest.get('privacy_risk')}")

    return manifest


def normalize_text(raw_text: str) -> str:
    normalized_newlines = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned_lines = [line.rstrip() for line in normalized_newlines.split("\n")]
    return "\n".join(cleaned_lines).strip()


def detect_secret_patterns(text: str) -> list[str]:
    matches: list[str] = []
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            matches.append(label)
    return matches


def list_candidate_files() -> list[Path]:
    return sorted(
        [path for path in RAW_DIR.iterdir() if path.is_file() and path.suffix.lower() in ALLOWED_SUFFIXES],
        key=lambda path: path.name.lower(),
    )


def assign_splits(document_ids: list[str]) -> dict[str, str]:
    shuffled_ids = list(document_ids)
    random.Random(SPLIT_SEED).shuffle(shuffled_ids)

    if not shuffled_ids:
        return {}

    val_count = max(1, int(round(len(shuffled_ids) * VAL_RATIO)))
    if len(shuffled_ids) > 1:
        val_count = min(val_count, len(shuffled_ids) - 1)

    val_ids = set(shuffled_ids[:val_count])
    return {document_id: ("val" if document_id in val_ids else "train") for document_id in document_ids}


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> int:
    manifest = load_manifest()
    candidate_files = list_candidate_files()

    processed_entries: list[dict[str, Any]] = []
    dropped_entries: list[dict[str, Any]] = []
    secret_scan_hits = 0

    for file_path in candidate_files:
        raw_text = file_path.read_text(encoding="utf-8")
        cleaned_text = normalize_text(raw_text)
        relative_source_path = file_path.relative_to(PROJECT_ROOT).as_posix()

        if not cleaned_text:
            dropped_entries.append(
                {
                    "source_id": manifest["source_id"],
                    "source_path": relative_source_path,
                    "reason": "empty_after_cleaning",
                }
            )
            continue

        matched_patterns = detect_secret_patterns(cleaned_text)
        if matched_patterns:
            secret_scan_hits += 1
            dropped_entries.append(
                {
                    "source_id": manifest["source_id"],
                    "source_path": relative_source_path,
                    "reason": "secret_pattern_detected",
                    "matched_patterns": matched_patterns,
                }
            )
            continue

        processed_entries.append(
            {
                "id": f"{manifest['source_id']}_doc_{len(processed_entries) + 1:04d}",
                "source_id": manifest["source_id"],
                "source_path": relative_source_path,
                "source_category": manifest["source_category"],
                "split": "pending",
                "text": cleaned_text,
                "metadata": {
                    "file_name": file_path.name,
                    "file_extension": file_path.suffix.lower(),
                    "line_count": cleaned_text.count("\n") + 1,
                    "character_count": len(cleaned_text),
                },
            }
        )

    split_assignments = assign_splits([entry["id"] for entry in processed_entries])
    train_entries: list[dict[str, Any]] = []
    val_entries: list[dict[str, Any]] = []

    for entry in processed_entries:
        entry["split"] = split_assignments[entry["id"]]
        if entry["split"] == "train":
            train_entries.append(entry)
        else:
            val_entries.append(entry)

    write_jsonl(PROCESSED_PATH, processed_entries)
    write_jsonl(TRAIN_PATH, train_entries)
    write_jsonl(VAL_PATH, val_entries)
    write_jsonl(DROPPED_PATH, dropped_entries)

    summary = {
        "source_id": manifest["source_id"],
        "source_category": manifest["source_category"],
        "input_dir": RAW_DIR.relative_to(PROJECT_ROOT).as_posix(),
        "allowed_suffixes": sorted(ALLOWED_SUFFIXES),
        "split_seed": SPLIT_SEED,
        "validation": {
            "source_id_match": True,
            "allowed_for_training": True,
            "privacy_risk": manifest["privacy_risk"],
        },
        "counts": {
            "processed_docs": len(processed_entries),
            "train_docs": len(train_entries),
            "val_docs": len(val_entries),
            "dropped_files": len(dropped_entries),
            "secret_scan_hits": secret_scan_hits,
        },
        "outputs": {
            "processed_jsonl": PROCESSED_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "train_jsonl": TRAIN_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "val_jsonl": VAL_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "dropped_jsonl": DROPPED_PATH.relative_to(PROJECT_ROOT).as_posix(),
        },
    }

    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"source_id: {manifest['source_id']}")
    print(f"processed_docs: {len(processed_entries)}")
    print(f"train_docs: {len(train_entries)}")
    print(f"val_docs: {len(val_entries)}")
    print(f"dropped_files: {len(dropped_entries)}")
    print(f"secret_scan_hits: {secret_scan_hits}")
    print(f"processed_output: {PROCESSED_PATH.relative_to(PROJECT_ROOT).as_posix()}")
    print(f"summary_output: {SUMMARY_PATH.relative_to(PROJECT_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
