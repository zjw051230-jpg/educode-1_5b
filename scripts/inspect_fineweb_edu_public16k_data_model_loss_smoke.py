from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import torch
from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "windows" / "fineweb_edu_500mb_public16k_data_model_loss_smoke.json"
SUMMARY_PATH = (
    PROJECT_ROOT
    / "data"
    / "public_corpus"
    / "fineweb_edu_sample10bt_500mb"
    / "fineweb_edu_public16k_data_model_loss_smoke_summary.json"
)
EXPECTED_VOCAB_SIZE = 16384

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.losses import next_token_cross_entropy
from educode.sequence_dataset import batch_samples, make_next_token_samples
from educode.tiny_model import TinyDecoderOnlyTransformer, TinyModelConfig


def repo_relative_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def resolve_repo_path(path_value: str) -> Path:
    return PROJECT_ROOT / Path(path_value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect FineWeb-Edu 500MB public16k data/model/loss smoke path.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the public16k smoke config JSON.")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def choose_device(config: dict[str, Any]) -> torch.device:
    preference = str(config.get("device_preference", "cuda_if_available_else_cpu"))
    if preference == "cuda_if_available_else_cpu" and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def choose_model_dtype(device: torch.device) -> torch.dtype:
    if device.type != "cuda":
        return torch.float32
    if hasattr(torch.cuda, "is_bf16_supported") and torch.cuda.is_bf16_supported():
        return torch.bfloat16
    return torch.float16


def collect_split_batch(
    split_name: str,
    split_path: Path,
    tokenizer: Tokenizer,
    sequence_length: int,
    batch_size: int,
) -> tuple[int, int, tuple[list[list[int]], list[list[int]]]]:
    required_token_count = batch_size * sequence_length + 1
    token_ids: list[int] = []
    docs_seen = 0
    docs_used = 0

    with split_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                raise ValueError(f"{split_name} line {line_number} is empty in {split_path}")
            record = json.loads(raw_line)
            text = record.get("text")
            if not isinstance(text, str) or not text:
                raise ValueError(f"{split_name} line {line_number} is missing non-empty text in {split_path}")

            docs_seen += 1
            if len(token_ids) < required_token_count:
                encoded_ids = tokenizer.encode(text).ids
                if not encoded_ids:
                    raise ValueError(f"{split_name} line {line_number} encoded to no token IDs")
                token_ids.extend(encoded_ids)
                docs_used += 1

    samples = make_next_token_samples(token_ids, sequence_length)
    batches = batch_samples(samples, batch_size)
    if not batches:
        raise ValueError(f"{split_name} did not produce a full batch")
    return docs_seen, docs_used, batches[0]


def build_300m_class_model_config(vocab_size: int) -> TinyModelConfig:
    return TinyModelConfig(
        vocab_size=vocab_size,
        context_length=512,
        num_layers=18,
        d_model=1024,
        num_heads=16,
        d_ff=4096,
        dropout=0.0,
        attention_backend="sdpa",
    )


def count_model_parameters(model: torch.nn.Module) -> int:
    return sum(int(parameter.numel()) for parameter in model.parameters())


def write_summary(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path
    config = load_json(config_path)

    run_name = str(config["run_name"])
    train_path = resolve_repo_path(str(config["train_path"]))
    val_path = resolve_repo_path(str(config["val_path"]))
    tokenizer_path = resolve_repo_path(str(config["tokenizer_path"]))
    expected_vocab_size = int(config["vocab_size"])
    sequence_length = int(config["sequence_length"])
    batch_size = int(config["batch_size"])
    seed = int(config.get("seed", 336))

    if expected_vocab_size != EXPECTED_VOCAB_SIZE:
        raise ValueError(f"config vocab_size must be {EXPECTED_VOCAB_SIZE}, got {expected_vocab_size}")
    if sequence_length != 128:
        raise ValueError(f"sequence_length must be 128 for this smoke, got {sequence_length}")
    if batch_size != 4:
        raise ValueError(f"batch_size must be 4 for this smoke, got {batch_size}")
    if config.get("no_training") is not True:
        raise ValueError("config no_training must be true")

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    tokenizer_vocab_size = tokenizer.get_vocab_size()
    if tokenizer_vocab_size != expected_vocab_size:
        raise ValueError(f"tokenizer vocab mismatch: expected {expected_vocab_size} but loaded {tokenizer_vocab_size}")

    train_docs, train_docs_used, train_batch = collect_split_batch("train", train_path, tokenizer, sequence_length, batch_size)
    val_docs, val_docs_used, val_batch = collect_split_batch("val", val_path, tokenizer, sequence_length, batch_size)
    batch_x, batch_y = train_batch

    device = choose_device(config)
    model_dtype = choose_model_dtype(device)
    model_config = build_300m_class_model_config(tokenizer_vocab_size)
    model = TinyDecoderOnlyTransformer(model_config).to(device=device)
    if device.type == "cuda":
        model = model.to(dtype=model_dtype)
    model.eval()
    parameter_count = count_model_parameters(model)

    input_ids = torch.tensor(batch_x, dtype=torch.long, device=device)
    targets = torch.tensor(batch_y, dtype=torch.long, device=device)

    with torch.no_grad():
        logits = model(input_ids)
        loss = next_token_cross_entropy(logits, targets)

    loss_value = float(loss.item())
    loss_finite = bool(torch.isfinite(loss).item())
    summary = {
        "run_name": run_name,
        "config_path": repo_relative_path(config_path),
        "train_path": repo_relative_path(train_path),
        "val_path": repo_relative_path(val_path),
        "train_docs": train_docs,
        "val_docs": val_docs,
        "train_docs_used_for_batch": train_docs_used,
        "val_docs_used_for_batch": val_docs_used,
        "tokenizer_path": repo_relative_path(tokenizer_path),
        "tokenizer_vocab_size": tokenizer_vocab_size,
        "sequence_length": sequence_length,
        "batch_size": batch_size,
        "input_ids_shape": list(input_ids.shape),
        "targets_shape": list(targets.shape),
        "logits_shape": list(logits.shape),
        "loss_value": loss_value,
        "loss_finite": loss_finite,
        "device": str(device),
        "model_dtype": str(model_dtype).replace("torch.", ""),
        "parameter_count": parameter_count,
        "no_backward": True,
        "no_optimizer_step": True,
        "no_checkpoint": True,
        "no_training": True,
    }
    write_summary(SUMMARY_PATH, summary)

    print(f"run_name={summary['run_name']}")
    print(f"train_docs={summary['train_docs']}")
    print(f"val_docs={summary['val_docs']}")
    print(f"tokenizer_path={summary['tokenizer_path']}")
    print(f"tokenizer_vocab_size={summary['tokenizer_vocab_size']}")
    print(f"input_ids_shape={tuple(summary['input_ids_shape'])}")
    print(f"targets_shape={tuple(summary['targets_shape'])}")
    print(f"logits_shape={tuple(summary['logits_shape'])}")
    print(f"parameter_count={summary['parameter_count']}")
    print(f"loss_value={summary['loss_value']:.6f}")
    print(f"loss_finite={summary['loss_finite']}")
    print(f"device={summary['device']}")
    print(f"summary_path={repo_relative_path(SUMMARY_PATH)}")

    if not loss_finite:
        print("failure: loss is not finite")
        return 1
    print("success: FineWeb-Edu public16k data/model/loss smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
