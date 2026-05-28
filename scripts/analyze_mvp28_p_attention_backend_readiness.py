from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "src" / "educode" / "tiny_model.py"
CONFIG_VALIDATOR_PATH = PROJECT_ROOT / "src" / "educode" / "config_validator.py"
TRAINING_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "run_a100_300m_fineweb_edu_10step_training.py"
A100_CONFIG_DIR = PROJECT_ROOT / "configs" / "a100"
FIVE_GB_3000_CONFIG = A100_CONFIG_DIR / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_a100_configs() -> list[Path]:
    return sorted(A100_CONFIG_DIR.glob("*.json"))


def main() -> int:
    blockers: list[str] = []

    required_files = [MODEL_PATH, CONFIG_VALIDATOR_PATH, TRAINING_SCRIPT_PATH, FIVE_GB_3000_CONFIG]
    for path in required_files:
        if not path.exists():
            blockers.append(f"missing required file: {path.relative_to(PROJECT_ROOT).as_posix()}")

    model_text = read_text(MODEL_PATH) if MODEL_PATH.exists() else ""
    validator_text = read_text(CONFIG_VALIDATOR_PATH) if CONFIG_VALIDATOR_PATH.exists() else ""
    training_text = read_text(TRAINING_SCRIPT_PATH) if TRAINING_SCRIPT_PATH.exists() else ""
    config = load_json(FIVE_GB_3000_CONFIG) if FIVE_GB_3000_CONFIG.exists() else {}
    a100_configs = find_a100_configs()

    uses_sdpa = "scaled_dot_product_attention" in model_text
    sdpa_is_causal = "is_causal=True" in model_text
    rejects_non_sdpa = 'attention_backend != "sdpa"' in model_text or "attention_backend must be sdpa" in model_text
    validator_allows_flash = "flash_attention_2" in validator_text
    validator_allows_naive = '"naive"' in validator_text
    model_has_flash_import = "flash_attn" in model_text.lower() or "flashattention" in model_text.lower()
    model_has_naive_branch = "attention_backend == \"naive\"" in model_text or "attention_backend == 'naive'" in model_text

    profiling = config.get("profiling", {}) if isinstance(config.get("profiling"), dict) else {}
    current_backend = profiling.get("attention_backend")
    backend_config_present = isinstance(current_backend, str)
    throughput_fields_present = all(
        token in training_text
        for token in [
            "tokens_per_sec",
            "elapsed_seconds",
            "memory_allocated",
            "memory_reserved",
        ]
    )
    summary_fields_present = all(
        token in training_text
        for token in [
            "approximate_tokens_per_sec",
            "last_gpu_memory_allocated_gib",
            "last_gpu_memory_reserved_gib",
        ]
    )
    cuda_only_training = "non-dry-run training requires cuda" in training_text
    autocast_cuda_only = "torch.autocast(device_type=\"cuda\"" in training_text

    if not uses_sdpa:
        blockers.append("core model does not use torch.nn.functional.scaled_dot_product_attention")
    if not sdpa_is_causal:
        blockers.append("core model SDPA path does not declare is_causal=True")
    if not backend_config_present:
        blockers.append("5GB 3000-step config is missing profiling.attention_backend")
    if not a100_configs:
        blockers.append("no A100 configs found")
    if not throughput_fields_present:
        blockers.append("training script does not expose per-step throughput/timing/memory fields")

    result = {
        "analysis_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "current_attention_backend": "sdpa" if uses_sdpa and current_backend == "sdpa" else current_backend,
        "attention_implementation_file": MODEL_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "uses_torch_scaled_dot_product_attention": uses_sdpa,
        "uses_causal_sdpa": sdpa_is_causal,
        "sdpa_ready": uses_sdpa and sdpa_is_causal and current_backend == "sdpa",
        "flashattention_ready": False,
        "flashattention_readiness_note": (
            "config validator allows flash_attention_2, but the core model has no FlashAttention implementation/import yet"
        ),
        "naive_backend_ready": model_has_naive_branch,
        "backend_config_present": backend_config_present,
        "validator_allows_naive": validator_allows_naive,
        "validator_allows_flash_attention_2": validator_allows_flash,
        "profiling_requires_gpu": True,
        "a100_config_count": len(a100_configs),
        "five_gb_3000_attention_backend": current_backend,
        "record_tokens_per_sec": profiling.get("record_tokens_per_sec"),
        "record_memory": profiling.get("record_memory"),
        "record_mfu": profiling.get("record_mfu"),
        "throughput_timing_metadata_present": throughput_fields_present,
        "summary_throughput_memory_fields_present": summary_fields_present,
        "cuda_only_training": cuda_only_training,
        "cuda_autocast_supported": autocast_cuda_only,
        "mps_training_path_supported": False,
        "recommended_next_mvp": "MVP-28.I: implement bounded attention profiling harness/configs before any profiling run",
        "blockers": blockers,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["analysis_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
