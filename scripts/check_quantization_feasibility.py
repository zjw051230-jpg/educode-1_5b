from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.quantization import (  # noqa: E402
    QuantizationConfig,
    fake_quantize_tensor,
    qlora_readiness,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a local quantization/QLoRA feasibility guard."
    )
    parser.add_argument("--bits", type=int, default=4)
    parser.add_argument("--quant-type", default="nf4")
    args = parser.parse_args()

    blockers = []
    try:
        config = QuantizationConfig(bits=args.bits, quant_type=args.quant_type)
    except ValueError as exc:
        config = None
        blockers.append(str(exc))

    fake_quant_finite = False
    readiness = None
    if config is not None:
        quantized = fake_quantize_tensor(torch.tensor([-1.0, -0.5, 0.0, 0.5, 1.0]), bits=config.bits)
        fake_quant_finite = bool(torch.isfinite(quantized).all())
        readiness = qlora_readiness(config)
        if not fake_quant_finite:
            blockers.append("fake_quant_output_non_finite")

    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "config": config.to_dict() if config else None,
        "fake_quant_finite": fake_quant_finite,
        "qlora_readiness": readiness,
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
