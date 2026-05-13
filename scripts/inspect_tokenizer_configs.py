from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.config_loader import load_json_config
from educode.config_validator import validate_config

CONFIG_PATHS = [
    PROJECT_ROOT / "configs" / "windows" / "byte_smoke_10m.json",
    PROJECT_ROOT / "configs" / "windows" / "bpe_toy_512_smoke.json",
    PROJECT_ROOT / "configs" / "windows" / "bpe_8k_formal_placeholder.json",
    PROJECT_ROOT / "configs" / "windows" / "smoke_cuda_10m.json",
]


def get_nested(config: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = config
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def inspect_config(config_path: Path) -> tuple[str, bool]:
    config = load_json_config(config_path)
    errors = validate_config(config, repo_root=PROJECT_ROOT)
    status = config.get("status")

    print(f"config path: {config_path}")
    print(f"run_name: {get_nested(config, 'run.run_name')}")
    if status is not None:
        print(f"status: {status}")
    print(f"tokenizer.type: {get_nested(config, 'tokenizer.type')}")
    print(f"tokenizer.vocab_size: {get_nested(config, 'tokenizer.vocab_size')}")
    print(f"model.vocab_size: {get_nested(config, 'model.vocab_size')}")

    tokenizer_path = get_nested(config, "tokenizer.path")
    if tokenizer_path is not None:
        print(f"tokenizer.path: {tokenizer_path}")

    if errors:
        print("validation: failed")
        print("errors:")
        for error in errors:
            print(f"- {error}")
        return str(config_path), False

    print("validation: passed")
    return str(config_path), True


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    results: list[tuple[str, bool]] = []
    for config_path in CONFIG_PATHS:
        print("===")
        results.append(inspect_config(config_path))

    print("=== summary ===")
    for config_path, passed in results:
        print(f"{config_path}: {'passed' if passed else 'failed'}")

    expected_results = {
        str(PROJECT_ROOT / "configs" / "windows" / "byte_smoke_10m.json"): True,
        str(PROJECT_ROOT / "configs" / "windows" / "bpe_toy_512_smoke.json"): True,
        str(PROJECT_ROOT / "configs" / "windows" / "bpe_8k_formal_placeholder.json"): False,
        str(PROJECT_ROOT / "configs" / "windows" / "smoke_cuda_10m.json"): False,
    }

    if any(expected_results[path] != passed for path, passed in results):
        print("result: unexpected validation state")
        return 1

    print("result: validation states match expectations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
