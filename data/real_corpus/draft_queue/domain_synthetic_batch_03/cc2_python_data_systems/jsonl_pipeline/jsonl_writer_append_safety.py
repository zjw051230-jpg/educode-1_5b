# draft_status: candidate
# topic_id: PDS-006
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC2
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

import json
from pathlib import Path
from typing import Any


def append_jsonl_row(path: str | Path, row: dict[str, Any]) -> None:
    target = Path(path)
    if not isinstance(row, dict):
        raise TypeError("row must be a dictionary")
    encoded = json.dumps(row, ensure_ascii=False)
    if "\n" in encoded:
        raise ValueError("encoded JSON row must stay on one physical line")
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(encoded)
        handle.write("\n")


def main() -> None:
    sample = {
        "id": "draft-row-1",
        "text": "Append mode should preserve earlier rows.",
        "source_category": "synthetic_examples",
    }
    append_jsonl_row("draft_metrics.jsonl", sample)


if __name__ == "__main__":
    main()
