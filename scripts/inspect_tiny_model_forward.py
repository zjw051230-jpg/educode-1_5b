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
from educode.sequence_dataset import batch_samples, make_next_token_samples
from educode.tiny_model import TinyDecoderOnlyTransformer, model_config_from_dict
from educode.toy_data import get_toy_corpus, join_corpus


def main() -> int:
    config_path = PROJECT_ROOT / "configs" / "windows" / "smoke_cuda_10m.json"
    config = load_json_config(config_path)

    errors = validate_config(config)
    if errors:
        print("validation: failed")
        for error in errors:
            print(f"- {error}")
        return 1

    model_config = model_config_from_dict(config)

    model_context_length = config["model"].get("context_length")
    data_sequence_length = config["data"].get("sequence_length")
    training_sequence_length = config["training"].get("sequence_length")
    if not (
        isinstance(model_context_length, int)
        and model_context_length == data_sequence_length
        and model_context_length == training_sequence_length
    ):
        print("validation: failed")
        print("- model.context_length, data.sequence_length, and training.sequence_length must match")
        return 1

    tokenizer = ByteTokenizer()
    text = join_corpus(get_toy_corpus())
    token_ids = tokenizer.encode(text)

    context_length_used = min(model_context_length, 16)
    batch_size = min(config["training"].get("batch_size", 1), 4)

    samples = make_next_token_samples(token_ids, context_length_used)
    batches = batch_samples(samples, batch_size)
    if not batches:
        print("failure: no full batch could be created from the toy corpus")
        return 1

    batch_x, _ = batches[0]
    input_ids = torch.tensor(batch_x, dtype=torch.long)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TinyDecoderOnlyTransformer(model_config)
    model.to(device)
    input_ids = input_ids.to(device)

    model.eval()
    with torch.no_grad():
        logits = model(input_ids)

    expected_shape = (input_ids.shape[0], input_ids.shape[1], model_config.vocab_size)
    parameter_count = sum(parameter.numel() for parameter in model.parameters())
    finite_check = bool(torch.isfinite(logits).all().item())
    success = tuple(logits.shape) == expected_shape and finite_check

    print(f"device: {device}")
    print(f"input_ids shape: {tuple(input_ids.shape)}")
    print(f"logits shape: {tuple(logits.shape)}")
    print(f"expected logits shape: {expected_shape}")
    print(f"vocab_size: {model_config.vocab_size}")
    print(f"context length used: {context_length_used}")
    print(f"parameter count: {parameter_count}")
    print(f"logits finite check: {finite_check}")
    print(f"success: {success}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
