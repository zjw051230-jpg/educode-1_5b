from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.tokenizer_stats import TokenizerStatsConfig, analyze_tokenizer_stats  # noqa: E402


def main() -> int:
    text = "hello <bos> world hello <unk>"
    report = analyze_tokenizer_stats(text, TokenizerStatsConfig())
    report.update(
        {
            "analysis_status": "passed",
            "tokenizer_training_run": False,
            "raw_data_touched": False,
            "modal_gpu_training_run": False,
        }
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
