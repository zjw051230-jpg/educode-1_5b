# draft_status: candidate
# topic_id: B04-COD-0151
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_04

"""Synthetic teaching example for tokenizer encode/decode helper with focus on safe text cleaning helper."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import torch
except Exception:  # pragma: no cover
    torch = None


@dataclass
class TokenizerUtilsExample051:
    topic_id: str = "B04-COD-0151"
    subtopic: str = "tokenizer_utils"
    focus: str = "tokenizer encode/decode helper"
    variant: int = 1

    def describe(self) -> dict[str, object]:
        return {
            "topic_id": self.topic_id,
            "subtopic": self.subtopic,
            "focus": self.focus,
            "variant": self.variant,
        }


def build_tokenizer_utils_example_051(values: Iterable[int]) -> dict[str, object]:
    numeric_values = [int(value) for value in values]
    summary = {
        "count": len(numeric_values),
        "sum": sum(numeric_values),
        "max": max(numeric_values) if numeric_values else 0,
        "min": min(numeric_values) if numeric_values else 0,
    }
    summary["mean"] = round(summary["sum"] / summary["count"], 4) if summary["count"] else 0.0
    return summary


def build_teaching_notes() -> list[str]:
    return [
        "Keep examples synthetic and review-oriented.",
        "Use small numbers to make shape and schema checks easy to inspect.",
        "Separate bounded smoke checks from any real training claims.",
        "Prefer explicit field names when writing summaries or manifest rows.",
    ]


def maybe_make_tensor() -> tuple[int, ...] | None:
    if torch is None:
        return None
    sample = torch.arange(12, dtype=torch.float32).view(3, 4)
    if "tokenizer_utils" in ('minimal_pytorch', 'loss_examples', 'validation_loop'):
        sample = sample + 1
    return tuple(sample.shape)


def build_preview_path(repo_root: str = "/synthetic/repo") -> str:
    return str(Path(repo_root) / "data" / "draft_queue" / "domain_synthetic_batch_04" / "tokenizer_utils" / "B04-COD-0151.json")


def main() -> None:
    example = TokenizerUtilsExample051()
    stats = build_tokenizer_utils_example_051([51, 52, 53, 54])
    payload = {
        "meta": example.describe(),
        "stats": stats,
        "notes": build_teaching_notes(),
        "tensor_shape": maybe_make_tensor(),
        "preview_path": build_preview_path(),
        "extra_focus": "safe text cleaning helper",
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    print(encoded)
    assert payload["meta"]["topic_id"] == "B04-COD-0151"
    assert stats["count"] == 4
    assert "draft_queue" in payload["preview_path"]


if __name__ == "__main__":
    main()
