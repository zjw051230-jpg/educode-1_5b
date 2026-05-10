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
from educode.checkpoint import compare_model_parameters, load_checkpoint, save_checkpoint
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
    model_config = model_config_from_dict(config)

    model_a = TinyDecoderOnlyTransformer(model_config)
    model_a.to(device)
    input_ids = input_ids.to(device)
    target_ids = target_ids.to(device)

    optimizer_config = config.get("optimizer") if isinstance(config.get("optimizer"), dict) else {}
    learning_rate = optimizer_config.get("learning_rate", 3e-4)
    weight_decay = optimizer_config.get("weight_decay", 0.0)
    optimizer_a = torch.optim.AdamW(model_a.parameters(), lr=learning_rate, weight_decay=weight_decay)

    model_a.train()
    optimizer_a.zero_grad(set_to_none=True)
    logits = model_a(input_ids)
    loss = next_token_cross_entropy(logits, target_ids)
    loss.backward()
    optimizer_a.step()

    checkpoint_path = PROJECT_ROOT / "experiments" / "windows_cuda" / "checkpoint_inspect_tmp" / "checkpoint.pt"
    step = 1
    metadata = {
        "source": "inspect_checkpoint.py",
        "purpose": "W10.9 checkpoint save/load only",
    }
    save_checkpoint(checkpoint_path, model_a, optimizer_a, step=step, config=config, metadata=metadata)

    model_b = TinyDecoderOnlyTransformer(model_config)
    model_b.to(device)
    optimizer_b = torch.optim.AdamW(model_b.parameters(), lr=learning_rate, weight_decay=weight_decay)

    checkpoint = load_checkpoint(checkpoint_path, model_b, optimizer=optimizer_b, map_location=device)
    compare_result = compare_model_parameters(model_a, model_b)

    checkpoint_file_exists = checkpoint_path.exists()
    optimizer_state_loaded = len(optimizer_b.state_dict().get("state", {})) > 0
    config_loaded = checkpoint.get("config") == config
    metadata_loaded = checkpoint.get("metadata") == metadata
    success = (
        checkpoint_file_exists
        and compare_result["all_match"]
        and compare_result["max_abs_diff"] == 0.0
        and optimizer_state_loaded
        and config_loaded
        and metadata_loaded
    )

    print(f"device: {device}")
    print(f"checkpoint path: {checkpoint_path}")
    print(f"step: {checkpoint.get('step')}")
    print(f"checkpoint file exists: {checkpoint_file_exists}")
    print(f"model parameter all_match: {compare_result['all_match']}")
    print(f"max_abs_diff: {compare_result['max_abs_diff']:.10f}")
    print(f"optimizer state loaded: {optimizer_state_loaded}")
    print(f"config loaded: {config_loaded}")
    print(f"metadata loaded: {metadata_loaded}")
    print(f"success: {success}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
