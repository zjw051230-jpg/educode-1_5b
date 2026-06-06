from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.distributed_config import DistributedConfig  # noqa: E402
from src.educode.grad_accum import training_tokens_accounting  # noqa: E402


def main() -> int:
    blockers = []
    valid = DistributedConfig().validate()
    fsdp = DistributedConfig(strategy="fsdp", world_size=2, experimental_ack=True).validate()
    accounting = training_tokens_accounting(4, 4, 1024, 1, 10)
    try:
        DistributedConfig(strategy="fsdp", world_size=2)
        blockers.append("fsdp_without_ack_was_not_rejected")
    except ValueError:
        pass

    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "single_gpu": valid,
        "fsdp_guarded": fsdp,
        "grad_accum_accounting": accounting,
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
