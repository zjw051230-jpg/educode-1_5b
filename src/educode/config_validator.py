from __future__ import annotations

from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL_SECTIONS = [
    "run",
    "hardware",
    "tokenizer",
    "data",
    "model",
    "training",
    "optimizer",
    "scheduler",
    "checkpoint",
    "evaluation",
    "generation",
    "profiling",
    "logging",
]

ALLOWED_HARDWARE_TARGETS = {
    "windows_cuda",
    "mac_mps",
    "a100_cuda",
    "b200_cuda",
}

ALLOWED_ATTENTION_BACKENDS = {
    "naive",
    "sdpa",
    "flash_attention_2",
}

ALLOWED_TOKENIZER_TYPES = {
    "byte",
    "bpe",
}


def get_nested(config: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = config
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def validate_tokenizer_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    tokenizer_type = get_nested(config, "tokenizer.type")
    tokenizer_vocab_size = get_nested(config, "tokenizer.vocab_size")
    model_vocab_size = get_nested(config, "model.vocab_size")

    if tokenizer_type not in ALLOWED_TOKENIZER_TYPES:
        errors.append("tokenizer.type must be one of: byte, bpe")
        return errors

    if tokenizer_type == "byte":
        if tokenizer_vocab_size != 256:
            errors.append("byte tokenizer requires tokenizer.vocab_size == 256")
        if tokenizer_vocab_size != model_vocab_size:
            errors.append("tokenizer.vocab_size must match model.vocab_size")
        return errors

    tokenizer_path_value = get_nested(config, "tokenizer.path")
    if not isinstance(tokenizer_path_value, str) or not tokenizer_path_value.strip():
        errors.append("bpe tokenizer requires tokenizer.path")
    else:
        tokenizer_path = Path(tokenizer_path_value)
        if not tokenizer_path.is_absolute():
            tokenizer_path = Path.cwd() / tokenizer_path
        if not tokenizer_path.exists():
            errors.append("tokenizer.path must exist")
        elif not tokenizer_path.is_file():
            errors.append("tokenizer.path must be a file")
        elif tokenizer_path.suffix.lower() != ".json":
            errors.append("tokenizer.path should point to a .json tokenizer artifact")

    artifact_dir_value = get_nested(config, "tokenizer.artifact_dir")
    if artifact_dir_value is not None:
        if not isinstance(artifact_dir_value, str) or not artifact_dir_value.strip():
            errors.append("tokenizer.artifact_dir must be a non-empty string when provided")
        else:
            artifact_dir = Path(artifact_dir_value)
            if not artifact_dir.is_absolute():
                artifact_dir = Path.cwd() / artifact_dir
            if not artifact_dir.exists():
                errors.append("tokenizer.artifact_dir must exist")
            elif not artifact_dir.is_dir():
                errors.append("tokenizer.artifact_dir must be a directory")

    if tokenizer_vocab_size != model_vocab_size:
        errors.append("tokenizer.vocab_size must match model.vocab_size")

    if isinstance(tokenizer_path_value, str) and tokenizer_path_value.strip():
        try:
            from tokenizers import Tokenizer
        except ImportError:
            errors.append("tokenizers package is required to validate bpe tokenizer.path")
        else:
            tokenizer_path = Path(tokenizer_path_value)
            if not tokenizer_path.is_absolute():
                tokenizer_path = Path.cwd() / tokenizer_path
            if tokenizer_path.exists() and tokenizer_path.is_file():
                try:
                    loaded_tokenizer = Tokenizer.from_file(str(tokenizer_path))
                except Exception as exc:
                    errors.append(f"failed to load tokenizer.path: {exc}")
                else:
                    loaded_vocab_size = loaded_tokenizer.get_vocab_size()
                    if tokenizer_vocab_size != loaded_vocab_size:
                        errors.append("tokenizer.vocab_size must match loaded tokenizer vocab size")

    return errors


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for section in REQUIRED_TOP_LEVEL_SECTIONS:
        if section not in config or not isinstance(config.get(section), dict):
            errors.append(f"missing required top-level section: {section}")

    hardware_target = get_nested(config, "hardware.target")
    if hardware_target not in ALLOWED_HARDWARE_TARGETS:
        errors.append("hardware.target must be one of: windows_cuda, mac_mps, a100_cuda, b200_cuda")

    attention_backend = get_nested(config, "profiling.attention_backend")
    if attention_backend not in ALLOWED_ATTENTION_BACKENDS:
        errors.append("profiling.attention_backend must be one of: naive, sdpa, flash_attention_2")

    errors.extend(validate_tokenizer_config(config))

    architecture = get_nested(config, "model.architecture")
    if architecture != "dense_decoder_only":
        errors.append("model.architecture must be dense_decoder_only")

    ffn_type = get_nested(config, "model.ffn_type")
    if ffn_type == "moe":
        errors.append("model.ffn_type must not be moe")

    d_model = get_nested(config, "model.d_model")
    num_heads = get_nested(config, "model.num_heads")
    head_dim = get_nested(config, "model.head_dim")
    d_ff = get_nested(config, "model.d_ff")

    if not isinstance(d_model, int) or d_model <= 0:
        errors.append("model.d_model must be a positive integer")
    if not isinstance(num_heads, int) or num_heads <= 0:
        errors.append("model.num_heads must be a positive integer")

    if isinstance(d_model, int) and isinstance(num_heads, int) and num_heads > 0:
        if d_model % num_heads != 0:
            errors.append("d_model must be divisible by num_heads")
        expected_head_dim = d_model // num_heads if d_model % num_heads == 0 else None
        if head_dim is not None and expected_head_dim is not None and head_dim != expected_head_dim:
            errors.append("model.head_dim must equal d_model / num_heads")

    if not isinstance(d_ff, int) or not isinstance(d_model, int) or d_ff <= d_model:
        errors.append("model.d_ff must exist and be greater than model.d_model")

    max_steps = get_nested(config, "training.max_steps")
    batch_size = get_nested(config, "training.batch_size")
    grad_accum = get_nested(config, "training.gradient_accumulation_steps")

    if not isinstance(max_steps, int) or max_steps <= 0:
        errors.append("training.max_steps must be greater than 0")
    if not isinstance(batch_size, int) or batch_size <= 0:
        errors.append("training.batch_size must be greater than 0")
    if not isinstance(grad_accum, int) or grad_accum <= 0:
        errors.append("training.gradient_accumulation_steps must be greater than 0")

    if hardware_target == "windows_cuda":
        context_length = get_nested(config, "model.context_length")
        num_layers = get_nested(config, "model.num_layers")

        if not isinstance(context_length, int) or context_length > 256:
            errors.append("windows_cuda config requires model.context_length <= 256")
        if not isinstance(batch_size, int) or batch_size > 8:
            errors.append("windows_cuda config requires training.batch_size <= 8")
        if attention_backend not in {"sdpa", "naive"}:
            errors.append("windows_cuda config requires profiling.attention_backend to be sdpa or naive")
        if not isinstance(num_layers, int) or num_layers > 8:
            errors.append("windows_cuda config requires model.num_layers <= 8")
        if not isinstance(d_model, int) or d_model > 512:
            errors.append("windows_cuda config requires model.d_model <= 512")

    return errors
