from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPO_ROOT / "scripts" / "modal_a100_streaming_runner.py"
CONFIG_PATH = REPO_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile.json"
MODE_NAME = "profile_5gb_50step_sdpa"
EXPECTED_CONFIG_PATH = "configs/a100/fineweb_edu_5gb_300m_50step_public16k_sdpa_profile.json"
FORBIDDEN_CONFIG_PATH = "configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json"
EXPECTED_PACKAGE_PATH = "/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz"
EXPECTED_RESULT_PACKAGE = "/vol/results/mvp28_a100_5gb_50step_sdpa_profile_results.tar.gz"
EXPECTED_FLAGS = ("record_tokens_per_sec", "record_memory", "record_mfu")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def literal_value(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Tuple):
        return tuple(literal_value(element) for element in node.elts)
    if isinstance(node, ast.Name):
        return {"name_ref": node.id}
    raise ValueError(f"unsupported AST literal: {ast.dump(node)}")


def find_mode_spec(path: Path, mode_name: str) -> dict[str, Any] | None:
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "MODE_SPECS" for target in node.targets):
            continue
        if not isinstance(node.value, ast.Dict):
            continue
        for key_node, value_node in zip(node.value.keys, node.value.values):
            if not isinstance(key_node, ast.Constant) or key_node.value != mode_name:
                continue
            if not isinstance(value_node, ast.Call):
                raise ValueError(f"{mode_name} registry entry is not a ModeSpec call")
            return {keyword.arg: literal_value(keyword.value) for keyword in value_node.keywords if keyword.arg}
    return None


def main() -> int:
    blockers: list[str] = []

    mode_spec = find_mode_spec(RUNNER_PATH, MODE_NAME)
    config = load_json(CONFIG_PATH) if CONFIG_PATH.exists() else {}

    if mode_spec is None:
        blockers.append(f"{MODE_NAME} mode is missing from MODE_SPECS")
        mode_spec = {}

    config_path = mode_spec.get("config_path")
    if config_path != EXPECTED_CONFIG_PATH:
        blockers.append(f"config_path expected {EXPECTED_CONFIG_PATH!r}, got {config_path!r}")
    if config_path == FORBIDDEN_CONFIG_PATH or "3000step" in str(config_path):
        blockers.append(f"{MODE_NAME} must not use the 3000-step config: {config_path!r}")
    if not CONFIG_PATH.exists():
        blockers.append(f"missing profiling config: {CONFIG_PATH.relative_to(REPO_ROOT).as_posix()}")

    package_path = mode_spec.get("package_path")
    if package_path != EXPECTED_PACKAGE_PATH:
        blockers.append(f"package_path expected {EXPECTED_PACKAGE_PATH!r}, got {package_path!r}")

    result_package = mode_spec.get("result_package")
    if result_package != EXPECTED_RESULT_PACKAGE:
        blockers.append(f"result_package expected {EXPECTED_RESULT_PACKAGE!r}, got {result_package!r}")

    if mode_spec.get("train") is not True:
        blockers.append(f"{MODE_NAME} must be a bounded training/profiling mode")
    if mode_spec.get("cpu_only") is True:
        blockers.append(f"{MODE_NAME} must use the A100 GPU Modal path, not cpu_only")

    training = config.get("training", {}) if isinstance(config.get("training"), dict) else {}
    data = config.get("data", {}) if isinstance(config.get("data"), dict) else {}
    model = config.get("model", {}) if isinstance(config.get("model"), dict) else {}
    sampling = config.get("sampling", {}) if isinstance(config.get("sampling"), dict) else {}
    validation_sampling = (
        config.get("validation_sampling", {}) if isinstance(config.get("validation_sampling"), dict) else {}
    )
    profiling = config.get("profiling", {}) if isinstance(config.get("profiling"), dict) else {}

    max_steps = training.get("max_steps")
    attention_backend = profiling.get("attention_backend")
    profiling_flags = {flag: profiling.get(flag) for flag in EXPECTED_FLAGS}

    if max_steps != 50:
        blockers.append(f"training.max_steps expected 50, got {max_steps!r}")
    if training.get("batch_size") != 8:
        blockers.append(f"training.batch_size expected 8, got {training.get('batch_size')!r}")
    if training.get("gradient_accumulation_steps") != 4:
        blockers.append(
            "training.gradient_accumulation_steps expected 4, "
            f"got {training.get('gradient_accumulation_steps')!r}"
        )
    if training.get("sequence_length") != 512 or data.get("sequence_length") != 512 or model.get("context_length") != 512:
        blockers.append("sequence/context length must be 512 across training, data, and model")
    if data.get("data_loading_mode") != "streaming" or data.get("streaming") is not True:
        blockers.append("data loading must be streaming")
    if sampling.get("policy") != "shuffle_buffer":
        blockers.append(f"sampling.policy expected 'shuffle_buffer', got {sampling.get('policy')!r}")
    if validation_sampling.get("policy") != "shuffle_buffer":
        blockers.append(
            f"validation_sampling.policy expected 'shuffle_buffer', got {validation_sampling.get('policy')!r}"
        )
    if attention_backend != "sdpa":
        blockers.append(f"profiling.attention_backend expected 'sdpa', got {attention_backend!r}")
    for flag, value in profiling_flags.items():
        if value is not True:
            blockers.append(f"profiling.{flag} expected true, got {value!r}")

    summary = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "mode_name": MODE_NAME,
        "config_path": config_path,
        "max_steps": max_steps,
        "attention_backend": attention_backend,
        "expected_result_package": result_package,
        "profiling_flags": profiling_flags,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
