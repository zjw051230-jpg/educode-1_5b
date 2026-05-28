from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPO_ROOT / "scripts" / "modal_a100_streaming_runner.py"
CONFIG_PATH = REPO_ROOT / "configs" / "a100" / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"
MODE_NAME = "train_5gb_3000"
EXPECTED_CONFIG_PATH = "configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json"
EXPECTED_PACKAGE_PATH = "/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz"
EXPECTED_RESULT_PACKAGE = "/vol/results/mvp26_a100_5gb_3000step_public16k_streaming_results.tar.gz"
EXPECTED_TRAIN_TOKENS = 49_152_000


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


def main() -> None:
    blockers: list[str] = []
    mode_spec = find_mode_spec(RUNNER_PATH, MODE_NAME)
    config = load_json(CONFIG_PATH) if CONFIG_PATH.exists() else {}

    if mode_spec is None:
        blockers.append(f"{MODE_NAME} mode is missing from MODE_SPECS")
        mode_spec = {}

    config_path = mode_spec.get("config_path")
    if config_path != EXPECTED_CONFIG_PATH:
        blockers.append(f"config_path expected {EXPECTED_CONFIG_PATH!r}, got {config_path!r}")
    if "1000step" in str(config_path):
        blockers.append(f"{MODE_NAME} must not use a 1000-step config: {config_path!r}")

    package_path = mode_spec.get("package_path")
    if package_path != EXPECTED_PACKAGE_PATH:
        blockers.append(f"package_path expected {EXPECTED_PACKAGE_PATH!r}, got {package_path!r}")

    result_package = mode_spec.get("result_package")
    if result_package != EXPECTED_RESULT_PACKAGE:
        blockers.append(f"result_package expected {EXPECTED_RESULT_PACKAGE!r}, got {result_package!r}")

    if mode_spec.get("train") is not True:
        blockers.append(f"{MODE_NAME} must be a training mode")
    if mode_spec.get("cpu_only") is True:
        blockers.append(f"{MODE_NAME} must use the GPU Modal path, not cpu_only")

    max_steps = config.get("training", {}).get("max_steps")
    batch_size = config.get("training", {}).get("batch_size")
    sequence_length = config.get("training", {}).get("sequence_length", config.get("model", {}).get("context_length"))
    grad_accum = config.get("training", {}).get("gradient_accumulation_steps")
    expected_tokens_seen = None
    if all(isinstance(value, int) for value in [max_steps, batch_size, sequence_length, grad_accum]):
        expected_tokens_seen = int(max_steps) * int(batch_size) * int(sequence_length) * int(grad_accum)
    if max_steps != 3000:
        blockers.append(f"max_steps expected 3000, got {max_steps!r}")
    if expected_tokens_seen != EXPECTED_TRAIN_TOKENS:
        blockers.append(f"expected train tokens expected {EXPECTED_TRAIN_TOKENS}, got {expected_tokens_seen!r}")

    validation_sampling = config.get("validation_sampling", {})
    validation_sampling_policy = validation_sampling.get("policy")
    if validation_sampling_policy != "shuffle_buffer":
        blockers.append(f"validation_sampling.policy expected 'shuffle_buffer', got {validation_sampling_policy!r}")
    if validation_sampling.get("shuffle_seed") != 7331:
        blockers.append(f"validation_sampling.shuffle_seed expected 7331, got {validation_sampling.get('shuffle_seed')!r}")
    if validation_sampling.get("shuffle_buffer_size") != 64:
        blockers.append(
            f"validation_sampling.shuffle_buffer_size expected 64, got {validation_sampling.get('shuffle_buffer_size')!r}"
        )
    if validation_sampling.get("max_blocks_per_document") != 8:
        blockers.append(
            "validation_sampling.max_blocks_per_document expected 8, "
            f"got {validation_sampling.get('max_blocks_per_document')!r}"
        )

    summary = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "mode_name": MODE_NAME,
        "config_path": config_path,
        "max_steps": max_steps,
        "expected_tokens_seen": expected_tokens_seen,
        "expected_result_package": result_package,
        "validation_sampling_policy": validation_sampling_policy,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if blockers:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
