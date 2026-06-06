from __future__ import annotations

import json
import sys
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.attention_backends import (
    SUPPORTED_ATTENTION_BACKENDS,
    attention_backend_availability,
    causal_attention,
    normalize_attention_backend,
)


def synthetic_forward_passes(backend: str) -> bool:
    q = torch.randn(1, 2, 4, 8)
    k = torch.randn(1, 2, 4, 8)
    v = torch.randn(1, 2, 4, 8)
    output = causal_attention(q, k, v, backend=backend, dropout_p=0.0, training=False)
    return output.shape == v.shape and torch.isfinite(output).all().item()


def main() -> int:
    blockers: list[str] = []
    backend_rows = []
    for backend in SUPPORTED_ATTENTION_BACKENDS:
        availability = attention_backend_availability(backend)
        forward_passed = False
        if backend in {"sdpa", "naive"}:
            try:
                forward_passed = synthetic_forward_passes(backend)
            except Exception as exc:  # pragma: no cover - diagnostic path
                blockers.append(f"{backend} synthetic forward failed: {exc}")
        backend_rows.append(
            {
                "name": availability.name,
                "supported_by_config": availability.supported_by_config,
                "available": availability.available,
                "reason": availability.reason,
                "cpu_synthetic_forward_passed": forward_passed,
            }
        )

    bad_backend_rejected = False
    try:
        normalize_attention_backend("not_a_backend")
        blockers.append("bad backend name was not rejected")
    except ValueError:
        bad_backend_rejected = True

    result = {
        "availability_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "backends": backend_rows,
        "default_backend": "sdpa",
        "bad_backend_rejected": bad_backend_rejected,
        "modal_gpu_training_executed": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
