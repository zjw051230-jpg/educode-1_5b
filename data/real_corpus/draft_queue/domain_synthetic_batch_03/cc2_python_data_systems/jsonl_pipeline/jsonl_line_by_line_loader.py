# draft_status: candidate
# topic_id: PDS-001
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC2
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

import json
from pathlib import Path
from typing import Any, Dict, Iterable


def load_jsonl_rows(path: str | Path) -> Iterable[Dict[str, Any]]:
    source = Path(path)
    with source.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"line {line_number} is not a JSON object")
            yield row


def preview_dataset(rows: Iterable[Dict[str, Any]]) -> list[dict[str, Any]]:
    preview = []
    for row in rows:
        preview.append(
            {
                "text": row.get("text", ""),
                "source": row.get("source", "unknown"),
                "length": len(row.get("text", "")),
            }
        )
        if len(preview) == 3:
            break
    return preview


def main() -> None:
    sample_path = Path("draft_examples.jsonl")
    rows = load_jsonl_rows(sample_path)
    for item in preview_dataset(rows):
        print(item)


if __name__ == "__main__":
    main()
