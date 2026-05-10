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
from educode.losses import next_token_cross_entropy
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

    sequence_length = min(model_context_length, 16)
    batch_size = min(config["training"].get("batch_size", 1), 4)

    samples = make_next_token_samples(token_ids, sequence_length)
    batches = batch_samples(samples, batch_size)
    if not batches:
        print("failure: no full batch could be created from the toy corpus")
        return 1

    batch_x, batch_y = batches[0]
    input_ids = torch.tensor(batch_x, dtype=torch.long)
    target_ids = torch.tensor(batch_y, dtype=torch.long)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TinyDecoderOnlyTransformer(model_config_from_dict(config))
    model.to(device)
    input_ids = input_ids.to(device)
    target_ids = target_ids.to(device)

    optimizer_config = config.get("optimizer") if isinstance(config.get("optimizer"), dict) else {}
    learning_rate = optimizer_config.get("learning_rate", 3e-4)
    weight_decay = optimizer_config.get("weight_decay", 0.0)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    chosen_parameter_name = ""
    chosen_parameter = None
    for name, parameter in model.named_parameters():
        if parameter.requires_grad:
            chosen_parameter_name = name
            chosen_parameter = parameter
            break

    if chosen_parameter is None:
        print("failure: no trainable parameter found")
        return 1

    parameter_before = chosen_parameter.detach().clone()

    model.train()
    optimizer.zero_grad(set_to_none=True)
    logits = model(input_ids)
    loss = next_token_cross_entropy(logits, target_ids)
    loss.backward()

    grad = chosen_parameter.grad
    grad_exists = grad is not None
    grad_finite_check = bool(torch.isfinite(grad).all().item()) if grad_exists else False

    optimizer.step()

    parameter_after = chosen_parameter.detach()
    parameter_delta = (parameter_after - parameter_before).abs()
    parameter_changed = bool(torch.any(parameter_delta > 0).item())
    max_abs_param_delta = float(parameter_delta.max().item()) if parameter_delta.numel() > 0 else 0.0
    loss_finite_check = bool(torch.isfinite(loss).item())
    success = loss_finite_check and grad_exists and grad_finite_check and parameter_changed and max_abs_param_delta > 0.0

    print(f"device: {device}")
    print(f"input_ids shape: {tuple(input_ids.shape)}")
    print(f"target_ids shape: {tuple(target_ids.shape)}")
    print(f"logits shape: {tuple(logits.shape)}")
    print(f"loss value: {loss.item():.6f}")
    print(f"loss finite check: {loss_finite_check}")
    print(f"chosen parameter name: {chosen_parameter_name}")
    print(f"grad exists: {grad_exists}")
    print(f"grad finite check: {grad_finite_check}")
    print(f"parameter changed after optimizer step: {parameter_changed}")
    print(f"max_abs_param_delta: {max_abs_param_delta:.10f}")
    print(f"success: {success}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
