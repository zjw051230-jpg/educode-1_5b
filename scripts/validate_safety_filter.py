from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.safety_filter import SafetyFilter, SafetyPattern, build_filter_report


def main() -> int:
    safety_filter = SafetyFilter(
        [
            SafetyPattern(name="credential_marker", pattern=r"api[_-]?key", severity="high"),
            SafetyPattern(name="placeholder_unsafe", pattern=r"unsafe_test_phrase", severity="medium"),
        ]
    )
    report = build_filter_report(
        safety_filter,
        ["normal educational code sample", "contains api-key marker", "unsafe_test_phrase fixture"],
    )
    payload = {
        "validation_status": "passed" if report["unsafe_count"] == 2 else "failed",
        "report": report,
        "external_api_used": False,
        "network_used": False,
        "modal_used": False,
        "gpu_used": False,
        "training_started": False,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["validation_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
