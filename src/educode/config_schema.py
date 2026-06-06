from __future__ import annotations

from pathlib import Path
from typing import Any

from educode.config_validator import get_nested, validate_config

ALLOWED_RUN_TYPES = {"training_execution", "bounded_profile", "memory_preflight"}
ALLOWED_ATTENTION_BACKENDS = {"sdpa", "naive", "flash_attention_2"}
ALLOWED_OPTIMIZERS = {"adamw", "muon_experimental"}
MAX_CONTEXT_LENGTH = 2048
MAX_TRAINING_EXECUTION_STEPS = 5000
MAX_BOUNDED_PROFILE_STEPS = 50
MAX_MEMORY_PREFLIGHT_STEPS = 10


def infer_run_type(config: dict[str, Any]) -> str:
    explicit = get_nested(config, "run.run_type")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip().lower()

    run_name = str(get_nested(config, "run.run_name", "")).lower()
    max_steps = get_nested(config, "training.max_steps", 0)
    if "memory_preflight" in run_name or "preflight" in run_name:
        return "memory_preflight"
    if "profile" in run_name or (isinstance(max_steps, int) and max_steps <= MAX_BOUNDED_PROFILE_STEPS):
        return "bounded_profile"
    return "training_execution"


def _path_escapes_repo(path_value: Any) -> bool:
    if not isinstance(path_value, str) or not path_value.strip():
        return True
    path = Path(path_value)
    if path.is_absolute():
        return True
    return any(part == ".." for part in path.parts)


def validate_hardened_config(config: dict[str, Any], repo_root: str | Path | None = None) -> list[str]:
    errors = validate_config(config, repo_root=repo_root)

    run_type = infer_run_type(config)
    if run_type not in ALLOWED_RUN_TYPES:
        errors.append("run.run_type must be one of: training_execution, bounded_profile, memory_preflight")

    max_steps = get_nested(config, "training.max_steps")
    context_length = get_nested(config, "model.context_length")
    batch_size = get_nested(config, "training.batch_size")
    grad_accum = get_nested(config, "training.gradient_accumulation_steps")
    attention_backend = str(get_nested(config, "profiling.attention_backend", "")).strip().lower()
    optimizer_name = str(get_nested(config, "optimizer.name", "adamw")).strip().lower()

    if attention_backend not in ALLOWED_ATTENTION_BACKENDS:
        errors.append("profiling.attention_backend must be one of: naive, sdpa, flash_attention_2")
    if optimizer_name not in ALLOWED_OPTIMIZERS:
        errors.append("optimizer.name must be one of: adamw, muon_experimental")
    if optimizer_name == "muon_experimental":
        errors.append("optimizer.name=muon_experimental is experimental and must not be used without a dedicated gate")

    if not isinstance(context_length, int) or context_length <= 0 or context_length > MAX_CONTEXT_LENGTH:
        errors.append(f"model.context_length must be in [1, {MAX_CONTEXT_LENGTH}]")

    if run_type == "training_execution":
        if isinstance(max_steps, int) and max_steps > MAX_TRAINING_EXECUTION_STEPS:
            errors.append(f"training_execution max_steps must be <= {MAX_TRAINING_EXECUTION_STEPS}")
    elif run_type == "bounded_profile":
        if not isinstance(max_steps, int) or max_steps > MAX_BOUNDED_PROFILE_STEPS:
            errors.append(f"bounded_profile max_steps must be <= {MAX_BOUNDED_PROFILE_STEPS}")
        if attention_backend == "flash_attention_2":
            errors.append("bounded_profile flash_attention_2 requires a dedicated dependency/runtime gate")
    elif run_type == "memory_preflight":
        if not isinstance(max_steps, int) or max_steps > MAX_MEMORY_PREFLIGHT_STEPS:
            errors.append(f"memory_preflight max_steps must be <= {MAX_MEMORY_PREFLIGHT_STEPS}")
        if get_nested(config, "profiling.record_memory") is not True:
            errors.append("memory_preflight requires profiling.record_memory=true")

    if not isinstance(batch_size, int) or batch_size <= 0:
        errors.append("training.batch_size must be positive")
    if not isinstance(grad_accum, int) or grad_accum <= 0:
        errors.append("training.gradient_accumulation_steps must be positive")

    moe_config = config.get("moe")
    if isinstance(moe_config, dict) and moe_config.get("enabled") is True:
        errors.append("moe.enabled=true requires a dedicated MoE gate")

    checkpoint_save_dir = get_nested(config, "checkpoint.save_dir")
    if _path_escapes_repo(checkpoint_save_dir):
        errors.append("checkpoint.save_dir must be a repo-relative path that does not escape the repository")

    result_package_name = get_nested(config, "modal.result_package_name")
    if result_package_name is not None:
        package_name = str(result_package_name)
        if not package_name.endswith("_results.tar.gz"):
            errors.append("modal.result_package_name must end with _results.tar.gz")

    return errors
