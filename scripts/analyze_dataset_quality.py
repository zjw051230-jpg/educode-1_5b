from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.data_quality import detect_near_duplicates, text_quality_metrics  # noqa: E402


SYNTHETIC_TEXTS = [
    "Machine learning systems need careful validation and artifact hygiene.",
    "Machine learning systems need careful validation and artifact hygiene notes.",
    "Tokenizer training uses small reproducible fixtures in this local check.",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run local synthetic dataset quality and dedup checks."
    )
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()

    metrics = [text_quality_metrics(text) for text in SYNTHETIC_TEXTS]
    duplicates = detect_near_duplicates(SYNTHETIC_TEXTS, threshold=args.threshold, k=4)
    result = {
        "analysis_status": "passed",
        "text_count": len(SYNTHETIC_TEXTS),
        "quality_metrics": metrics,
        "near_duplicate_pairs": duplicates,
        "raw_data_touched": False,
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
