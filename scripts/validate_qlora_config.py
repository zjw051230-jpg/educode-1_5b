from __future__ import annotations

import json
import sys
from pathlib import Path

import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.quantization import QuantizationConfig, fake_dequantize_tensor, fake_quantize_tensor  # noqa: E402


def main() -> int:
    config = QuantizationConfig(bits=4, quant_type="nf4", qlora_enabled=True, experimental_ack=True)
    q = fake_quantize_tensor(torch.tensor([-1.0, 0.0, 1.0]), bits=config.bits)
    y = fake_dequantize_tensor(q)
    finite = bool(torch.isfinite(y).all())
    result = {
        "validation_status": "passed" if finite else "failed",
        "blocker_count": 0 if finite else 1,
        "config": config.to_dict(),
        "fake_quant_dequant_finite": finite,
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if finite else 1


if __name__ == "__main__":
    raise SystemExit(main())
