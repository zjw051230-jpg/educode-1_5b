from __future__ import annotations

import importlib
import platform
import sys
from typing import Any


def import_module(name: str) -> tuple[bool, str | None, str | None, Any | None]:
    try:
        module = importlib.import_module(name)
    except Exception as exc:
        return False, None, f"{type(exc).__name__}: {exc}", None

    version = getattr(module, "__version__", None)
    if version is None and name == "sentencepiece":
        version = getattr(module, "VERSION", None)
    return True, str(version) if version is not None else None, None, module


def print_result(label: str, available: bool, version: str | None = None, error: str | None = None) -> None:
    status = "available" if available else "missing"
    print(f"{label}: {status}")
    if version:
        print(f"{label} version: {version}")
    if error:
        print(f"{label} error: {error}")


def main() -> int:
    print("EduCode-1.5B Tokenizer Environment Check")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {platform.python_version()}")

    tokenizers_ok, tokenizers_version, tokenizers_error, _ = import_module("tokenizers")
    print_result("tokenizers", tokenizers_ok, tokenizers_version, tokenizers_error)

    sentencepiece_ok, sentencepiece_version, sentencepiece_error, _ = import_module("sentencepiece")
    print_result("sentencepiece", sentencepiece_ok, sentencepiece_version, sentencepiece_error)

    transformers_ok, transformers_version, transformers_error, _ = import_module("transformers")
    print_result("transformers", transformers_ok, transformers_version, transformers_error)

    auto_tokenizer_ok = False
    auto_tokenizer_error = None
    if transformers_ok:
        try:
            from transformers import AutoTokenizer  # type: ignore

            auto_tokenizer_ok = AutoTokenizer is not None
        except Exception as exc:
            auto_tokenizer_error = f"{type(exc).__name__}: {exc}"
    else:
        auto_tokenizer_error = "transformers unavailable"

    print_result("transformers.AutoTokenizer", auto_tokenizer_ok, error=auto_tokenizer_error)

    datasets_ok, datasets_version, datasets_error, _ = import_module("datasets")
    print_result("datasets", datasets_ok, datasets_version, datasets_error)

    print("decision:")
    if tokenizers_ok:
        print("- Hugging Face tokenizers is available; BPE can prioritize this route.")
    elif transformers_ok:
        print("- tokenizers is unavailable but transformers is available; dependency details still need confirmation.")
    else:
        print("- Hugging Face tokenizer route is not ready yet because tokenizers is unavailable.")

    if not sentencepiece_ok:
        print("- sentencepiece is unavailable; do not prioritize the sentencepiece route for now.")
    else:
        print("- sentencepiece is available as an alternative option if explicitly chosen later.")

    print("- No packages were installed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
