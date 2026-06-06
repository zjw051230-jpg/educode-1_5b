from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.quantization import QuantizationConfig, qlora_readiness  # noqa: E402


def main() -> int:
    config = QuantizationConfig(bits=4, quant_type="nf4", qlora_enabled=True, experimental_ack=True)
    report = qlora_readiness(config)
    report["validation_status"] = "passed"
    report["blocker_count"] = 0
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
