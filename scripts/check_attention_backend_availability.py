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
    SUPPORTED_ATTENTION_BACKENDS,
    backend_availability,
    causal_attention,
    normalize_attention_backend,
)
from educode.attention_utils import repeat_kv_for_gqa  # noqa: E402


def synthetic_result(backend: str) -> dict[str, object]:
    availability = backend_availability(backend)
    if not availability.available:
        return {"backend": backend, "available": False, "forward": "skipped", "reason": availability.reason}
    if backend == "flash_attention_2":
        return {
            "backend": backend,
            "available": True,
            "forward": "skipped",
            "reason": "optional backend present, GPU validation intentionally not run",
        }
    q = torch.randn(2, 4, 5, 8)
    k = torch.randn(2, 4, 5, 8)
    v = torch.randn(2, 4, 5, 8)
    out = causal_attention(q, k, v, backend=backend)
    return {"backend": backend, "available": True, "forward": "passed", "shape": list(out.shape), "reason": availability.reason}


def build_summary() -> dict[str, object]:
    blockers: list[str] = []
    results = [synthetic_result(backend) for backend in SUPPORTED_ATTENTION_BACKENDS]
    for result in results:
        if result["backend"] in {"sdpa", "naive"} and result["forward"] != "passed":
            blockers.append(f"{result['backend']} synthetic forward failed")
    q = torch.randn(2, 4, 5, 8)
    k = torch.randn(2, 4, 5, 8)
    v = torch.randn(2, 4, 5, 8)
    if not torch.allclose(causal_attention(q, k, v, backend="sdpa"), causal_attention(q, k, v, backend="naive"), atol=1e-5, rtol=1e-5):
        blockers.append("SDPA and naive outputs are not close on small tensor")
    gqa = repeat_kv_for_gqa(torch.randn(2, 2, 5, 8), num_query_heads=4)
    if tuple(gqa.shape) != (2, 4, 5, 8):
        blockers.append("GQA repeat helper returned wrong shape")
    bad_backend_rejected = False
    try:
        normalize_attention_backend("bad_backend")
    except ValueError:
        bad_backend_rejected = True
    if not bad_backend_rejected:
        blockers.append("bad backend was not rejected")
    return {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "backends": results,
        "bad_backend_rejected": bad_backend_rejected,
        "gqa_shape": list(gqa.shape),
        "flexattention_status": "documented_feasibility_only",
        "flashattention3_status": "documented_feasibility_only",
        "runs_gpu": False,
        "starts_training": False,
    }


def main() -> int:
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
