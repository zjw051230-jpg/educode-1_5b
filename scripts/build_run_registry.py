from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.run_registry import find_imported_summary_files, import_summary_file, write_registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local JSONL registry from imported run summaries.")
    parser.add_argument("--repo-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional JSONL output path. Omit this for dry-run summary output only.",
    )
    parser.add_argument("--run-type", choices=["training", "profile", "preflight", "smoke", "unknown"])
    parser.add_argument("--attention-backend")
    parser.add_argument("--context-length", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary_paths = find_imported_summary_files(args.repo_root)
    records = [import_summary_file(path, repo_root=args.repo_root) for path in summary_paths]

    if args.run_type:
        records = [record for record in records if record.run_type == args.run_type]
    if args.attention_backend:
        records = [record for record in records if record.attention_backend == args.attention_backend]
    if args.context_length:
        records = [record for record in records if record.context_length == args.context_length]

    if args.output:
        write_registry(args.output, records)

    payload = {
        "registry_status": "passed",
        "records_found": len(records),
        "summary_files_scanned": len(summary_paths),
        "output_written": args.output is not None,
        "output_path": str(args.output) if args.output else None,
        "tarballs_touched": False,
        "external_service_used": False,
        "records": [record.to_dict() for record in records[:10]],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
