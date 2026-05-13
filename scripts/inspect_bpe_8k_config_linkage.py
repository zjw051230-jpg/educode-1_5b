from __future__ import annotations

import sys
from pathlib import Path

from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.config_loader import load_json_config
from educode.config_validator import validate_config

CONFIG_PATH = PROJECT_ROOT / "configs" / "windows" / "bpe_8k_formal_placeholder.json"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    config = load_json_config(CONFIG_PATH)
    tokenizer_path = PROJECT_ROOT / config["tokenizer"]["path"]
    loaded_tokenizer = Tokenizer.from_file(str(tokenizer_path))
    loaded_vocab_size = loaded_tokenizer.get_vocab_size()
    errors = validate_config(config, repo_root=PROJECT_ROOT)

    print(f"config path: {CONFIG_PATH}")
    print(f"tokenizer.path: {tokenizer_path}")
    print(f"tokenizer.vocab_size: {config['tokenizer']['vocab_size']}")
    print(f"loaded tokenizer vocab size: {loaded_vocab_size}")
    print(f"model.vocab_size: {config['model']['vocab_size']}")

    if errors:
        print("validation failed")
        print("errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
