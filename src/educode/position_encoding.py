from __future__ import annotations

from typing import Any

SUPPORTED_POSITION_ENCODINGS = {"learned", "learned_position_embedding", "rope"}
DEFAULT_POSITION_ENCODING = "learned_position_embedding"


def get_position_encoding_type(model_config: dict[str, Any]) -> str:
    value = model_config.get("position_encoding", DEFAULT_POSITION_ENCODING)
    if isinstance(value, dict):
        value = value.get("type", DEFAULT_POSITION_ENCODING)
    position_type = str(value).strip().lower()
    if position_type not in SUPPORTED_POSITION_ENCODINGS:
        allowed = ", ".join(sorted(SUPPORTED_POSITION_ENCODINGS))
        raise ValueError(f"model.position_encoding.type must be one of: {allowed}")
    return position_type


def validate_position_encoding_config(model_config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        position_type = get_position_encoding_type(model_config)
    except ValueError as exc:
        return [str(exc)]
    if position_type != "rope":
        return errors
    value = model_config.get("position_encoding")
    rope_config = value if isinstance(value, dict) else model_config
    theta = rope_config.get("rope_theta", model_config.get("rope_theta", 10000.0))
    scaling_factor = rope_config.get("scaling_factor", 1.0)
    if not isinstance(theta, (int, float)) or float(theta) <= 0:
        errors.append("model.position_encoding.rope_theta must be positive")
    if not isinstance(scaling_factor, (int, float)) or float(scaling_factor) <= 0:
        errors.append("model.position_encoding.scaling_factor must be positive")
    scaling_type = rope_config.get("scaling_type")
    if scaling_type not in {None, "none", "placeholder"}:
        errors.append("NTK/YaRN/LongRoPE scaling algorithms are feasibility placeholders only")
    return errors
