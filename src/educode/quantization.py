from __future__ import annotations

import importlib.util
from dataclasses import asdict, dataclass

import torch


@dataclass(frozen=True)
class QuantizationConfig:
    bits: int
    quant_type: str
    quantization_enabled: bool = True
    qlora_enabled: bool = False
    double_quant: bool = True
    experimental_ack: bool = False

    def __post_init__(self) -> None:
        valid = {4: {"nf4", "fp4"}, 8: {"int8"}}
        if self.bits not in valid:
            raise ValueError("bits must be 4 or 8")
        if self.quant_type not in valid[self.bits]:
            raise ValueError("quant_type is invalid for requested bits")
        if self.qlora_enabled and not self.quantization_enabled:
            raise ValueError("QLoRA requires quantization_enabled=True")
        if self.qlora_enabled and not self.experimental_ack:
            raise ValueError("QLoRA requires experimental_ack=True")

    def to_dict(self) -> dict:
        return asdict(self)


def check_bitsandbytes_available() -> dict:
    available = importlib.util.find_spec("bitsandbytes") is not None
    return {
        "available": available,
        "status": "available" if available else "unavailable",
        "reason": "bitsandbytes import spec found" if available else "bitsandbytes not installed locally",
    }


def check_cuda_available() -> dict:
    available = bool(torch.cuda.is_available())
    return {
        "available": available,
        "status": "available" if available else "unavailable",
        "reason": "torch.cuda.is_available() local check only",
    }


def fake_quantize_tensor(tensor: torch.Tensor, bits: int) -> torch.Tensor:
    if bits not in {4, 8}:
        raise ValueError("bits must be 4 or 8")
    if tensor.numel() == 0:
        return tensor.clone()
    qmax = (2 ** (bits - 1)) - 1
    max_abs = tensor.detach().abs().max()
    if max_abs == 0:
        return torch.zeros_like(tensor)
    scale = max_abs / qmax
    return torch.clamp(torch.round(tensor / scale), -qmax, qmax) * scale


def fake_dequantize_tensor(tensor: torch.Tensor) -> torch.Tensor:
    return tensor.to(torch.float32).clone()


def qlora_readiness(config: QuantizationConfig) -> dict:
    bnb = check_bitsandbytes_available()
    cuda = check_cuda_available()
    ready = config.qlora_enabled and bnb["available"] and cuda["available"]
    return {
        "readiness_status": "ready_with_caveats" if ready else "unavailable",
        "config": config.to_dict(),
        "bitsandbytes": bnb,
        "cuda": cuda,
        "modal_gpu_training_run": False,
        "caveats": [
            "No real 4-bit model load was performed.",
            "DoRA and LoftQ remain feasibility documentation topics until separate implementation review.",
        ],
    }
