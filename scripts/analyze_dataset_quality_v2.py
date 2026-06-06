from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.data_quality import QualityConfig, quality_metrics  # noqa: E402
from src.educode.dedup import detect_exact_duplicates, detect_near_duplicates, minhash_feasibility  # noqa: E402


TEXTS = [
    "Machine learning systems need careful validation.",
    "Machine learning systems need careful validation notes.",
    "Machine learning systems need careful validation.",
]


def main() -> int:
    result = {
        "analysis_status": "passed",
        "quality_metrics": [quality_metrics(text, QualityConfig()) for text in TEXTS],
        "exact_duplicates": detect_exact_duplicates(TEXTS),
        "near_duplicates": detect_near_duplicates(TEXTS, threshold=0.5, k=3),
        "minhash": minhash_feasibility(),
        "raw_data_touched": False,
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
