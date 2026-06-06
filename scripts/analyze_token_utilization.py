from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.packing import estimate_padding_waste, pack_document_lengths, token_utilization  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze synthetic document length packing utilization."
    )
    parser.add_argument("--context-length", type=int, default=1024)
    parser.add_argument(
        "--lengths",
        default="128,256,64,512,300,120",
        help="Comma-separated synthetic document token lengths.",
    )
    args = parser.parse_args()

    lengths = [int(value.strip()) for value in args.lengths.split(",") if value.strip()]
    packs = pack_document_lengths(lengths, args.context_length)
    result = {
        "analysis_status": "passed",
        "context_length": args.context_length,
        "document_lengths": lengths,
        "packs": packs,
        "utilization": token_utilization(packs, args.context_length),
        "padding_waste": estimate_padding_waste(lengths, args.context_length),
        "modal_gpu_training_run": False,
        "raw_data_touched": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
