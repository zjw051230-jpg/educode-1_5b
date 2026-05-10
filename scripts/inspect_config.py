from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.config_loader import load_json_config, pretty_print_summary, summarize_config
from educode.config_validator import validate_config


def main() -> int:
    if len(sys.argv) > 1:
        config_arg = sys.argv[1]
    else:
        config_arg = "configs/windows/smoke_cuda_10m.json"

    config_path = (PROJECT_ROOT / config_arg).resolve() if not Path(config_arg).is_absolute() else Path(config_arg)

    print(f"Config path: {config_path}")
    config = load_json_config(config_path)
    print("JSON loaded successfully")

    summary = summarize_config(config)
    pretty_print_summary(summary)

    errors = validate_config(config)
    if errors:
        print("Validation: failed")
        for error in errors:
            print(f"- {error}")
    else:
        print("Validation: passed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
