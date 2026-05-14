from __future__ import annotations

from pathlib import Path


def validate_config_shape(config: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(config.get("model"), dict):
        errors.append("model section missing")
    if not isinstance(config.get("training"), dict):
        errors.append("training section missing")
    if not isinstance(config.get("tokenizer"), dict):
        errors.append("tokenizer section missing")
    return errors


def validate_tokenizer_path(config: dict, repo_root: Path) -> list[str]:
    tokenizer = config.get("tokenizer", {})
    path_value = tokenizer.get("path")
    if not isinstance(path_value, str):
        return ["tokenizer.path missing"]
    resolved = repo_root / path_value
    return [] if resolved.exists() else [f"missing tokenizer path: {resolved}"]


def main() -> None:
    example = {
        "model": {"vocab_size": 1846},
        "training": {"max_steps": 100},
        "tokenizer": {"path": "tokenizers/example/tokenizer.json"},
    }
    print(validate_config_shape(example))


if __name__ == "__main__":
    main()
