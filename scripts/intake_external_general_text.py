from __future__ import annotations

import json
import random
import re
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = (
    PROJECT_ROOT
    / "data"
    / "real_corpus"
    / "raw"
    / "external_general_text"
    / "project_gutenberg_small_sample"
    / "candidate_pg_0001_alice"
)
RAW_PATH = RAW_DIR / "alice_pg11_raw.txt"
SOURCE_NOTE_PATH = RAW_DIR / "SOURCE.md"
MANIFEST_PATH = PROJECT_ROOT / "data" / "real_corpus" / "metadata" / "source_manifest.external_general_text.jsonl"
CANDIDATES_PATH = PROJECT_ROOT / "data" / "real_corpus" / "metadata" / "project_gutenberg_candidates.reviewed.jsonl"
PROCESSED_PATH = PROJECT_ROOT / "data" / "real_corpus" / "processed" / "external_general_text.processed.jsonl"
TRAIN_PATH = PROJECT_ROOT / "data" / "real_corpus" / "splits" / "external_general_text.train.jsonl"
VAL_PATH = PROJECT_ROOT / "data" / "real_corpus" / "splits" / "external_general_text.val.jsonl"
DROPPED_PATH = PROJECT_ROOT / "data" / "real_corpus" / "metadata" / "external_general_text.dropped_files.jsonl"
SUMMARY_PATH = PROJECT_ROOT / "data" / "real_corpus" / "metadata" / "external_general_text.intake_summary.json"

EXPECTED_SOURCE_ID = "external_general_text_project_gutenberg_000001"
EXPECTED_CANDIDATE_ID = "candidate_pg_0001"
EXPECTED_SOURCE_CATEGORY = "external_general_text"
EXPECTED_PROJECT_ROLE = "supplement_only_not_project_backbone"
SPLIT_SEED = 1337
VAL_RATIO = 0.10

START_MARKER_RE = re.compile(r"^\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*$", re.MULTILINE)
END_MARKER_RE = re.compile(r"^\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*$", re.MULTILINE)
CHAPTER_RE = re.compile(r"(?ms)^CHAPTER ([IVXLCDM]+)\.\n([^\n]+)\n+(.*?)(?=^CHAPTER [IVXLCDM]+\.\n|\Z)")

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("api_key", re.compile(r"(?i)\bapi[_\- ]?key\b")),
    ("secret", re.compile(r"(?i)\bsecret\b")),
    ("password", re.compile(r"(?i)\bpassword\b")),
    ("private_key", re.compile(r"(?i)(\bprivate[_\- ]?key\b|-----BEGIN [A-Z ]*PRIVATE KEY-----)")),
    ("sk-", re.compile(r"\bsk-[A-Za-z0-9]{8,}\b")),
]


def read_single_jsonl_record(path: Path) -> dict[str, Any]:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) != 1:
        raise ValueError(f"expected exactly one JSONL record in {path}, found {len(lines)}")
    return json.loads(lines[0])



def read_jsonl_records(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]



def parse_source_note(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        match = re.match(r"^- ([a-z_]+): `([^`]*)`$", line)
        if match:
            fields[match.group(1)] = match.group(2)
    return fields



def normalize_line_endings(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")



def clean_text(text: str) -> str:
    normalized = normalize_line_endings(text)
    cleaned_lines = [line.rstrip() for line in normalized.split("\n")]

    compacted_lines: list[str] = []
    blank_pending = False
    for line in cleaned_lines:
        if line == "":
            if compacted_lines:
                blank_pending = True
            continue
        if blank_pending:
            compacted_lines.append("")
            blank_pending = False
        compacted_lines.append(line)

    return "\n".join(compacted_lines).strip()



def trim_gutenberg_boilerplate(raw_text: str) -> tuple[str, bool]:
    normalized = normalize_line_endings(raw_text)
    start_match = START_MARKER_RE.search(normalized)
    end_match = END_MARKER_RE.search(normalized)

    if start_match and end_match and start_match.end() < end_match.start():
        return normalized[start_match.end() : end_match.start()].strip("\n"), True

    return normalized.strip("\n"), False



def extract_sections(trimmed_text: str, raw_relative_path: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    matches = list(CHAPTER_RE.finditer(trimmed_text))
    if not matches:
        raise ValueError("no chapter sections found in trimmed Project Gutenberg text")

    sections: list[dict[str, Any]] = []
    dropped_entries: list[dict[str, Any]] = []

    front_matter = trimmed_text[: matches[0].start()].strip()
    if front_matter:
        dropped_entries.append(
            {
                "source_id": EXPECTED_SOURCE_ID,
                "candidate_id": EXPECTED_CANDIDATE_ID,
                "source_path": raw_relative_path,
                "reason": "front_matter_excluded_before_first_chapter",
            }
        )

    for index, match in enumerate(matches, start=1):
        numeral = match.group(1).strip()
        chapter_title = match.group(2).strip()
        chapter_body = clean_text(match.group(3))

        if not chapter_body:
            dropped_entries.append(
                {
                    "source_id": EXPECTED_SOURCE_ID,
                    "candidate_id": EXPECTED_CANDIDATE_ID,
                    "source_path": raw_relative_path,
                    "reason": "empty_section_after_cleaning",
                    "section": f"CHAPTER {numeral}",
                }
            )
            continue

        section_text = clean_text(f"CHAPTER {numeral}.\n{chapter_title}\n\n{chapter_body}")
        if not section_text:
            dropped_entries.append(
                {
                    "source_id": EXPECTED_SOURCE_ID,
                    "candidate_id": EXPECTED_CANDIDATE_ID,
                    "source_path": raw_relative_path,
                    "reason": "empty_document_after_section_assembly",
                    "section": f"CHAPTER {numeral}",
                }
            )
            continue

        sections.append(
            {
                "index": index,
                "numeral": numeral,
                "chapter_title": chapter_title,
                "text": section_text,
            }
        )

    return sections, dropped_entries



def assign_splits(document_ids: list[str]) -> dict[str, str]:
    if not document_ids:
        return {}

    shuffled_ids = list(document_ids)
    random.Random(SPLIT_SEED).shuffle(shuffled_ids)

    val_count = max(1, int(round(len(shuffled_ids) * VAL_RATIO)))
    if len(shuffled_ids) > 1:
        val_count = min(val_count, len(shuffled_ids) - 1)

    val_ids = set(shuffled_ids[:val_count])
    return {document_id: ("val" if document_id in val_ids else "train") for document_id in document_ids}



def classify_secret_hits(records: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    hits: list[dict[str, Any]] = []
    potential_real_secret = False

    for record in records:
        text = record["text"]
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                start = max(0, match.start() - 40)
                end = min(len(text), match.end() + 40)
                excerpt = text[start:end].replace("\n", " ")

                if label == "secret":
                    contextual_secret = re.search(
                        r"(?i)(api|token|access|client|auth|credential|private|password|key)\W{0,10}secret|secret\W{0,10}(api|token|access|client|auth|credential|private|password|key)",
                        excerpt,
                    )
                    hits.append(
                        {
                            "id": record["id"],
                            "split": record["split"],
                            "pattern": label,
                            "excerpt": excerpt,
                            "classification": "potential_real_secret" if contextual_secret else "benign_content_word",
                        }
                    )
                    if contextual_secret:
                        potential_real_secret = True
                    continue

                hits.append(
                    {
                        "id": record["id"],
                        "split": record["split"],
                        "pattern": label,
                        "excerpt": excerpt,
                        "classification": "potential_real_secret",
                    }
                )
                potential_real_secret = True

    if not hits:
        return "no_hits", hits
    if potential_real_secret:
        return "potential_real_secret", hits
    return "explanatory/license-only", hits



def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")



def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"missing raw text file: {RAW_PATH}")
    if not SOURCE_NOTE_PATH.exists():
        raise FileNotFoundError(f"missing source note: {SOURCE_NOTE_PATH}")

    manifest = read_single_jsonl_record(MANIFEST_PATH)
    if manifest.get("source_id") != EXPECTED_SOURCE_ID:
        raise ValueError(f"unexpected manifest source_id: {manifest.get('source_id')}")
    if manifest.get("source_category") != EXPECTED_SOURCE_CATEGORY:
        raise ValueError(f"unexpected manifest source_category: {manifest.get('source_category')}")
    if manifest.get("project_role") != EXPECTED_PROJECT_ROLE:
        raise ValueError(f"unexpected manifest project_role: {manifest.get('project_role')}")
    if manifest.get("selected_candidate_id") != EXPECTED_CANDIDATE_ID:
        raise ValueError(f"unexpected selected_candidate_id: {manifest.get('selected_candidate_id')}")
    if manifest.get("external_download") is not True:
        raise ValueError("manifest external_download must be true")
    if manifest.get("data_added") is not True:
        raise ValueError("manifest data_added must be true")
    if manifest.get("raw_local_path") != RAW_PATH.relative_to(PROJECT_ROOT).as_posix():
        raise ValueError("manifest raw_local_path does not match expected raw file")
    if manifest.get("source_note_path") != SOURCE_NOTE_PATH.relative_to(PROJECT_ROOT).as_posix():
        raise ValueError("manifest source_note_path does not match expected SOURCE.md")

    candidate_records = read_jsonl_records(CANDIDATES_PATH)
    candidate = next((record for record in candidate_records if record.get("candidate_id") == EXPECTED_CANDIDATE_ID), None)
    if candidate is None:
        raise ValueError(f"candidate {EXPECTED_CANDIDATE_ID} not found in reviewed candidates JSONL")
    if candidate.get("text_downloaded") is not True:
        raise ValueError("candidate text_downloaded must be true")
    if candidate.get("approved_for_training") not in {False, None}:
        raise ValueError("candidate approved_for_training must remain false before training approval")

    source_note = parse_source_note(SOURCE_NOTE_PATH)
    if source_note.get("candidate_id") != EXPECTED_CANDIDATE_ID:
        raise ValueError("SOURCE.md candidate_id does not match expected candidate")
    if source_note.get("source_category") != EXPECTED_SOURCE_CATEGORY:
        raise ValueError("SOURCE.md source_category does not match expected value")
    if source_note.get("project_role") != EXPECTED_PROJECT_ROLE:
        raise ValueError("SOURCE.md project_role does not match expected value")
    if source_note.get("local_raw_file") != RAW_PATH.name:
        raise ValueError("SOURCE.md local_raw_file does not match raw file name")

    return manifest, candidate, source_note



def build_records(
    manifest: dict[str, Any],
    candidate: dict[str, Any],
    source_note: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    raw_relative_path = RAW_PATH.relative_to(PROJECT_ROOT).as_posix()
    source_note_relative_path = SOURCE_NOTE_PATH.relative_to(PROJECT_ROOT).as_posix()

    raw_text = RAW_PATH.read_text(encoding="utf-8")
    trimmed_text, header_footer_removed = trim_gutenberg_boilerplate(raw_text)
    sections, dropped_entries = extract_sections(trimmed_text, raw_relative_path)
    if not sections:
        raise ValueError("no processed sections were produced from the raw Gutenberg sample")

    title = source_note.get("title") or candidate.get("title") or manifest.get("selected_title")
    author = source_note.get("author") or candidate.get("author")
    landing_page = source_note.get("landing_page") or candidate.get("gutenberg_landing_page")

    processed_entries: list[dict[str, Any]] = []
    for section in sections:
        processed_entries.append(
            {
                "id": f"{EXPECTED_CANDIDATE_ID}_chapter_{section['index']:02d}",
                "source_id": EXPECTED_SOURCE_ID,
                "candidate_id": EXPECTED_CANDIDATE_ID,
                "source_category": EXPECTED_SOURCE_CATEGORY,
                "split": "pending",
                "text": section["text"],
                "metadata": {
                    "title": title,
                    "author": author,
                    "landing_page": landing_page,
                    "raw_path": raw_relative_path,
                    "source_note_path": source_note_relative_path,
                    "header_footer_removed_in_processed": header_footer_removed,
                    "project_role": EXPECTED_PROJECT_ROLE,
                },
            }
        )

    split_assignments = assign_splits([record["id"] for record in processed_entries])
    train_entries: list[dict[str, Any]] = []
    val_entries: list[dict[str, Any]] = []

    for record in processed_entries:
        record["split"] = split_assignments[record["id"]]
        if record["split"] == "train":
            train_entries.append(record)
        else:
            val_entries.append(record)

    secret_scan_result, secret_hits = classify_secret_hits(processed_entries)
    if secret_scan_result == "potential_real_secret":
        raise ValueError(f"potential real secret detected in processed output candidates: {secret_hits}")

    summary = {
        "source_id": EXPECTED_SOURCE_ID,
        "candidate_id": EXPECTED_CANDIDATE_ID,
        "source_category": EXPECTED_SOURCE_CATEGORY,
        "input": {
            "raw_dir": RAW_DIR.relative_to(PROJECT_ROOT).as_posix(),
            "raw_path": raw_relative_path,
            "source_note_path": source_note_relative_path,
        },
        "processing": {
            "header_footer_removed_in_processed": header_footer_removed,
            "split_method": "chapter",
            "split_seed": SPLIT_SEED,
            "val_ratio": VAL_RATIO,
        },
        "counts": {
            "processed_docs": len(processed_entries),
            "train_docs": len(train_entries),
            "val_docs": len(val_entries),
            "dropped_files": len(dropped_entries),
        },
        "secret_scan": {
            "result": secret_scan_result,
            "hit_count": len(secret_hits),
            "hits": secret_hits,
        },
        "outputs": {
            "processed_jsonl": PROCESSED_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "train_jsonl": TRAIN_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "val_jsonl": VAL_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "dropped_jsonl": DROPPED_PATH.relative_to(PROJECT_ROOT).as_posix(),
            "summary_json": SUMMARY_PATH.relative_to(PROJECT_ROOT).as_posix(),
        },
        "validation": {
            "manifest_source_id_match": manifest.get("source_id") == EXPECTED_SOURCE_ID,
            "candidate_downloaded": candidate.get("text_downloaded") is True,
            "approved_for_training_before_review": candidate.get("approved_for_training") is False,
        },
    }

    return processed_entries, dropped_entries, summary



def main() -> int:
    manifest, candidate, source_note = validate_inputs()
    processed_entries, dropped_entries, summary = build_records(manifest, candidate, source_note)

    write_jsonl(PROCESSED_PATH, processed_entries)
    write_jsonl(TRAIN_PATH, [record for record in processed_entries if record["split"] == "train"])
    write_jsonl(VAL_PATH, [record for record in processed_entries if record["split"] == "val"])
    write_jsonl(DROPPED_PATH, dropped_entries)
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"source_id: {summary['source_id']}")
    print(f"candidate_id: {summary['candidate_id']}")
    print(f"processed_docs: {summary['counts']['processed_docs']}")
    print(f"train_docs: {summary['counts']['train_docs']}")
    print(f"val_docs: {summary['counts']['val_docs']}")
    print(f"dropped_files: {summary['counts']['dropped_files']}")
    print(f"header_footer_removed_in_processed: {summary['processing']['header_footer_removed_in_processed']}")
    print(f"secret_scan_result: {summary['secret_scan']['result']}")
    print(f"processed_output: {summary['outputs']['processed_jsonl']}")
    print(f"train_output: {summary['outputs']['train_jsonl']}")
    print(f"val_output: {summary['outputs']['val_jsonl']}")
    print(f"summary_output: {summary['outputs']['summary_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
