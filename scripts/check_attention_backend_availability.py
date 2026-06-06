from __future__ import annotations

import json
import sys
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.attention_backends import (  # noqa: E402
    DEFAULT_ATTENTION_BACKEND,
    SUPPORTED_ATTENTION_BACKENDS,
    backend_availability,
    causal_attention,
    normalize_attention_backend,
)


def run_synthetic_forward(backend: str) -> dict[str, object]:
    availability = backend_availability(backend)
    if not availability.available:
        return {
            "backend": backend,
            "available": False,
            "synthetic_forward": "skipped",
            "reason": availability.reason,
        }

    if backend == "flash_attention_2":
        return {
            "backend": backend,
            "available": True,
            "synthetic_forward": "skipped",
            "reason": "optional backend import is available, but GPU validation is not run locally",
        }

    q = torch.randn(2, 4, 8, 16)
    k = torch.randn(2, 4, 8, 16)
    v = torch.randn(2, 4, 8, 16)
    out = causal_attention(q, k, v, backend=backend)
    return {
        "backend": backend,
        "available": True,
        "synthetic_forward": "passed",
        "output_shape": list(out.shape),
        "reason": availability.reason,
    }


def build_summary() -> dict[str, object]:
    backend_results = [run_synthetic_forward(backend) for backend in SUPPORTED_ATTENTION_BACKENDS]
    blockers: list[str] = []

    for result in backend_results:
        backend = result["backend"]
        if backend in {"sdpa", "naive"} and result.get("synthetic_forward") != "passed":
            blockers.append(f"{backend} synthetic forward did not pass")

    bad_backend_rejected = False
    try:
        normalize_attention_backend("unknown_backend")
    except ValueError:
        bad_backend_rejected = True
    if not bad_backend_rejected:
        blockers.append("bad backend name was not rejected")

    return {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "default_backend": DEFAULT_ATTENTION_BACKEND,
        "supported_backends": list(SUPPORTED_ATTENTION_BACKENDS),
        "bad_backend_rejected": bad_backend_rejected,
        "runs_gpu": False,
        "runs_training": False,
        "backends": backend_results,
    }


def main() -> int:
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
