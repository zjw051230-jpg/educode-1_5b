from __future__ import annotations

import importlib.util
from dataclasses import asdict, dataclass

import torch


@dataclass(frozen=True)
class QuantizationConfig:
    bits: int
    quant_type: str
    double_quant: bool = True

    def __post_init__(self) -> None:
        valid = {
            4: {"nf4", "fp4"},
            8: {"int8"},
        }
        if self.bits not in valid:
            raise ValueError("bits must be 4 or 8")
        if self.quant_type not in valid[self.bits]:
            raise ValueError(f"quant_type {self.quant_type!r} is invalid for {self.bits}-bit")

    def to_dict(self) -> dict:
        return asdict(self)


def check_bitsandbytes_available() -> dict:
    spec = importlib.util.find_spec("bitsandbytes")
    if spec is None:
        return {
            "available": False,
            "status": "unavailable",
            "reason": "bitsandbytes is not installed in this local environment",
        }
    return {
        "available": True,
        "status": "available",
        "reason": "bitsandbytes import spec found; CUDA/runtime compatibility still requires a separate gated check",
    }


def fake_quantize_tensor(tensor: torch.Tensor, bits: int = 4) -> torch.Tensor:
    if bits not in {4, 8}:
        raise ValueError("bits must be 4 or 8")
    if tensor.numel() == 0:
        return tensor.clone()
    qmax = (2 ** (bits - 1)) - 1
    max_abs = tensor.detach().abs().max()
    if max_abs == 0:
        return torch.zeros_like(tensor)
    scale = max_abs / qmax
    quantized = torch.clamp(torch.round(tensor / scale), -qmax, qmax)
    return quantized * scale


def qlora_readiness(config: QuantizationConfig) -> dict:
    bnb = check_bitsandbytes_available()
    ready = config.bits == 4 and bnb["available"]
    return {
        "readiness_status": "ready_with_caveats" if ready else "unavailable",
        "requested_bits": config.bits,
        "quant_type": config.quant_type,
        "double_quant": config.double_quant,
        "bitsandbytes": bnb,
        "modal_gpu_training_run": False,
        "caveats": [
            "This is a local feasibility check only.",
            "CUDA, Modal image compatibility, optimizer paging, and adapter training must be validated in a separate cost-gated branch.",
        ],
    }
