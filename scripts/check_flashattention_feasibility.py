from __future__ import annotations

import importlib.util
import json
import platform
import sys
from pathlib import Path
from typing import Any

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SUPPORTED_FLASH_DTYPES = ("float16", "bfloat16")


def flash_attn_installed() -> bool:
    return importlib.util.find_spec("flash_attn") is not None


def collect_environment() -> dict[str, Any]:
    cuda_available = bool(torch.cuda.is_available())
    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "torch_version": torch.__version__,
        "torch_cuda_version": torch.version.cuda,
        "cuda_available": cuda_available,
        "cuda_device_count": torch.cuda.device_count() if cuda_available else 0,
        "bf16_supported": bool(torch.cuda.is_bf16_supported()) if cuda_available else False,
        "flash_attn_installed": flash_attn_installed(),
    }


def validate_future_flashattention_config(config: dict[str, Any], *, flash_available: bool) -> list[str]:
    blockers: list[str] = []
    profiling = config.get("profiling")
    flash = config.get("flash_attention")
    if not isinstance(profiling, dict):
        return ["missing profiling section"]
    if not isinstance(flash, dict):
        return ["missing flash_attention section"]

    backend = str(profiling.get("attention_backend", "")).strip().lower()
    if backend not in {"sdpa", "flash_attention_2"}:
        blockers.append("profiling.attention_backend must be sdpa or flash_attention_2")

    enabled = flash.get("enabled", False)
    if not isinstance(enabled, bool):
        blockers.append("flash_attention.enabled must be a boolean")
    if enabled and backend != "flash_attention_2":
        blockers.append("flash_attention.enabled requires profiling.attention_backend=flash_attention_2")
    if enabled and not flash_available:
        blockers.append("flash_attention.enabled requires flash_attn to be installed")

    dtype = str(flash.get("dtype", "")).strip().lower()
    if dtype and dtype not in SUPPORTED_FLASH_DTYPES:
        blockers.append("flash_attention.dtype must be float16 or bfloat16")

    return blockers


def default_future_config() -> dict[str, Any]:
    return {
        "profiling": {
            "attention_backend": "flash_attention_2",
        },
        "flash_attention": {
            "enabled": False,
            "dtype": "bfloat16",
            "notes": "Prepared optional path only; requires separate install/runtime validation before enabling.",
        },
    }


def build_summary() -> dict[str, Any]:
    environment = collect_environment()
    installed = bool(environment["flash_attn_installed"])
    future_config = default_future_config()
    config_blockers = validate_future_flashattention_config(future_config, flash_available=installed)

    bad_configs = [
        {
            "profiling": {"attention_backend": "unknown_backend"},
            "flash_attention": {"enabled": False, "dtype": "bfloat16"},
        },
        {
            "profiling": {"attention_backend": "sdpa"},
            "flash_attention": {"enabled": True, "dtype": "bfloat16"},
        },
        {
            "profiling": {"attention_backend": "flash_attention_2"},
            "flash_attention": {"enabled": False, "dtype": "float32"},
        },
    ]
    bad_config_rejected = all(
        validate_future_flashattention_config(config, flash_available=installed) for config in bad_configs
    )

    blockers = list(config_blockers)
    if not bad_config_rejected:
        blockers.append("bad FlashAttention configs were not rejected")

    caveats: list[str] = []
    if not installed:
        caveats.append("flash_attn package is not installed")
    if not environment["cuda_available"]:
        caveats.append("CUDA is not available in this local check")
    if "windows" in str(environment["platform"]).lower():
        caveats.append("local Windows environment may differ from Modal Linux/CUDA runtime")

    return {
        "feasibility_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "caveat_count": len(caveats),
        "caveats": caveats,
        "flash_attn_installed": installed,
        "flashattention_available_for_local_run": bool(installed and environment["cuda_available"]),
        "bad_config_rejected": bad_config_rejected,
        "future_enable_config": future_config,
        "environment": environment,
        "runs_gpu": False,
        "runs_modal": False,
        "starts_training": False,
    }


def main() -> int:
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
