from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.instruction_data import load_jsonl_samples, validate_instruction_sample


SYNTHETIC_SAMPLE = {
    "id": "synthetic-001",
    "messages": [
        {"role": "system", "content": "You are a concise coding tutor."},
        {"role": "user", "content": "Explain a loop invariant."},
        {"role": "assistant", "content": "It is a condition that stays true before and after each loop iteration."},
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate local instruction-tuning JSONL samples.")
    parser.add_argument("--input", type=Path, help="Optional local JSONL sample file.")
    parser.add_argument("--max-estimated-tokens", type=int, default=4096)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.input:
        summary = load_jsonl_samples(args.input, max_estimated_tokens=args.max_estimated_tokens)
    else:
        result = validate_instruction_sample(SYNTHETIC_SAMPLE, max_estimated_tokens=args.max_estimated_tokens)
        summary = {
            "validation_status": "passed" if result.accepted else "failed",
            "sample_count": 1,
            "accepted_count": 1 if result.accepted else 0,
            "rejected_count": 0 if result.accepted else 1,
            "results": [
                {
                    "id": SYNTHETIC_SAMPLE["id"],
                    "accepted": result.accepted,
                    "estimated_tokens": result.estimated_tokens,
                    "issues": list(result.issues),
                }
            ],
        }

    summary.update(
        {
            "gpu_used": False,
            "modal_used": False,
            "training_started": False,
            "raw_dataset_required": False,
        }
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["rejected_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
