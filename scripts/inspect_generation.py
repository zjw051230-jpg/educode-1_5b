from __future__ import annotations

import sys
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.byte_tokenizer import ByteTokenizer
from educode.config_loader import load_json_config
from educode.config_validator import validate_config
from educode.generation import generate_text, generate_token_ids, safe_decode_token_ids
from educode.tiny_model import TinyDecoderOnlyTransformer, model_config_from_dict


def main() -> int:
    config_path = PROJECT_ROOT / "configs" / "windows" / "smoke_cuda_10m.json"
    config = load_json_config(config_path)

    errors = validate_config(config)
    if errors:
        print("validation: failed")
        for error in errors:
            print(f"- {error}")
        return 1

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = ByteTokenizer()
    model = TinyDecoderOnlyTransformer(model_config_from_dict(config))
    model.to(device)

    prompt = "hello"
    max_new_tokens = 16
    temperature = 1.0
    top_k = 64

    prompt_token_ids = tokenizer.encode(prompt)
    generated_token_ids = generate_token_ids(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        device=device,
        temperature=temperature,
        top_k=top_k,
    )
    generated_text = generate_text(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        device=device,
        temperature=temperature,
        top_k=top_k,
    )

    generated_text_preview = generated_text[:120]
    fallback_used = "�" in generated_text_preview
    new_token_count = len(generated_token_ids) - len(prompt_token_ids)
    success = len(generated_token_ids) > len(prompt_token_ids) and len(generated_text_preview) >= 0

    print(f"device: {device}")
    print(f"prompt: {prompt}")
    print(f"prompt token ids: {prompt_token_ids}")
    print(f"generated token ids length: {len(generated_token_ids)}")
    print(f"max_new_tokens: {max_new_tokens}")
    print(f"new token count: {new_token_count}")
    print(f"generated text preview: {generated_text_preview}")
    print(f"fallback decode used: {fallback_used}")
    print(f"success: {success}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
