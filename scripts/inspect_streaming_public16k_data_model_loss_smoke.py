from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch
from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"
SCRIPTS_PATH = PROJECT_ROOT / "scripts"
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_500mb_300m_1000step_public16k_execute.json"
EXPECTED_VOCAB_SIZE = 16384
DEFAULT_SMOKE_SEQUENCE_LENGTH = 128
DEFAULT_SMOKE_BATCH_SIZE = 2

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

for path in (SRC_PATH, SCRIPTS_PATH):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from educode.losses import next_token_cross_entropy
from educode.tiny_model import TinyDecoderOnlyTransformer, model_config_from_dict
from streaming_lm_batch_iterator import create_streaming_batch_iterator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect streaming public16k data/model/loss smoke path.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the streaming public16k A100/A800 config JSON.")
    parser.add_argument("--sequence-length", type=int, default=DEFAULT_SMOKE_SEQUENCE_LENGTH)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_SMOKE_BATCH_SIZE)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_repo_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def repo_relative_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def get_data_loading_mode(config: dict[str, Any]) -> str:
    data_config = config.get("data", {}) if isinstance(config.get("data"), dict) else {}
    return str(data_config.get("data_loading_mode", config.get("data_loading_mode", "precomputed"))).strip().lower()


def get_eos_token_id(config: dict[str, Any]) -> int | None:
    tokenizer_config = config.get("tokenizer", {}) if isinstance(config.get("tokenizer"), dict) else {}
    eos_token_id = tokenizer_config.get("eos_token_id", tokenizer_config.get("endoftext_token_id"))
    return eos_token_id if isinstance(eos_token_id, int) else None


def choose_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def choose_model_dtype(device: torch.device) -> torch.dtype:
    if device.type != "cuda":
        return torch.float32
    if hasattr(torch.cuda, "is_bf16_supported") and torch.cuda.is_bf16_supported():
        return torch.bfloat16
    return torch.float16


def count_model_parameters(model: torch.nn.Module) -> int:
    return sum(int(parameter.numel()) for parameter in model.parameters())


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path
    config = load_json(config_path)

    data_loading_mode = get_data_loading_mode(config)
    if data_loading_mode != "streaming":
        raise ValueError(f"config data_loading_mode must be streaming for this smoke, got {data_loading_mode!r}")
    if bool(config.get("training", {}).get("no_training", False)):
        raise ValueError("execution config should keep training.no_training=false; this smoke still performs no training")

    tokenizer_path = resolve_repo_path(str(config["tokenizer"]["path"]))
    train_path = resolve_repo_path(str(config["data"]["train_path"]))
    val_path = resolve_repo_path(str(config["data"]["val_path"]))
    output_dir = resolve_repo_path(str(config["run"]["output_dir"]))
    summary_path = output_dir / "streaming_public16k_data_model_loss_smoke_summary.json"
    expected_vocab_size = int(config["tokenizer"]["vocab_size"])
    if expected_vocab_size != EXPECTED_VOCAB_SIZE:
        raise ValueError(f"config vocab_size must be {EXPECTED_VOCAB_SIZE}, got {expected_vocab_size}")

    smoke_sequence_length = int(args.sequence_length)
    smoke_batch_size = int(args.batch_size)
    if smoke_sequence_length <= 0 or smoke_sequence_length > int(config["model"]["context_length"]):
        raise ValueError("smoke sequence length must be positive and fit inside model.context_length")
    if smoke_batch_size <= 0 or smoke_batch_size > int(config["training"]["batch_size"]):
        raise ValueError("smoke batch size must be positive and no larger than training.batch_size")

    seed = int(config.get("run", {}).get("seed", 336))
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    tokenizer_vocab_size = tokenizer.get_vocab_size()
    if tokenizer_vocab_size != expected_vocab_size:
        raise ValueError(f"tokenizer vocab mismatch: expected {expected_vocab_size} but loaded {tokenizer_vocab_size}")

    eos_token_id = get_eos_token_id(config)
    train_batch_iter, train_stats = create_streaming_batch_iterator(
        split_name="train",
        split_path=train_path,
        tokenizer=tokenizer,
        sequence_length=smoke_sequence_length,
        batch_size=smoke_batch_size,
        required_batches=1,
        eos_token_id=eos_token_id,
    )
    val_batch_iter, val_stats = create_streaming_batch_iterator(
        split_name="val",
        split_path=val_path,
        tokenizer=tokenizer,
        sequence_length=smoke_sequence_length,
        batch_size=smoke_batch_size,
        required_batches=1,
        eos_token_id=eos_token_id,
    )
    batch_x, batch_y = next(train_batch_iter)
    val_batch_x, val_batch_y = next(val_batch_iter)

    device = choose_device()
    model_dtype = choose_model_dtype(device)
    model_config = model_config_from_dict(config)
    model = TinyDecoderOnlyTransformer(model_config).to(device=device)
    if device.type == "cuda":
        model = model.to(dtype=model_dtype)
    model.eval()
    parameter_count = count_model_parameters(model)

    input_ids = torch.tensor(batch_x, dtype=torch.long, device=device)
    targets = torch.tensor(batch_y, dtype=torch.long, device=device)
    val_input_ids = torch.tensor(val_batch_x, dtype=torch.long, device=device)
    val_targets = torch.tensor(val_batch_y, dtype=torch.long, device=device)

    with torch.no_grad():
        logits = model(input_ids)
        loss = next_token_cross_entropy(logits, targets)
        val_logits = model(val_input_ids)
        val_loss = next_token_cross_entropy(val_logits, val_targets)

    loss_finite = bool(torch.isfinite(loss).item())
    val_loss_finite = bool(torch.isfinite(val_loss).item())
    summary = {
        "run_name": config["run"]["run_name"],
        "config_path": repo_relative_path(config_path),
        "train_path": repo_relative_path(train_path),
        "val_path": repo_relative_path(val_path),
        "tokenizer_path": repo_relative_path(tokenizer_path),
        "tokenizer_vocab_size": tokenizer_vocab_size,
        "data_loading_mode": data_loading_mode,
        "host_ram_efficient_batching": True,
        "batch_precompute_disabled": True,
        "smoke_sequence_length": smoke_sequence_length,
        "smoke_batch_size": smoke_batch_size,
        "config_sequence_length": config["training"].get("sequence_length"),
        "config_batch_size": config["training"].get("batch_size"),
        "input_ids_shape": list(input_ids.shape),
        "targets_shape": list(targets.shape),
        "val_input_ids_shape": list(val_input_ids.shape),
        "val_targets_shape": list(val_targets.shape),
        "logits_shape": list(logits.shape),
        "val_logits_shape": list(val_logits.shape),
        "loss_value": float(loss.item()),
        "val_loss_value": float(val_loss.item()),
        "loss_finite": loss_finite,
        "val_loss_finite": val_loss_finite,
        "device": str(device),
        "model_dtype": str(model_dtype).replace("torch.", ""),
        "parameter_count": parameter_count,
        "train_data_probe": train_stats.to_dict(),
        "val_data_probe": val_stats.to_dict(),
        "no_backward": True,
        "no_optimizer_step": True,
        "no_checkpoint": True,
        "no_training": True,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(summary_path, summary)

    print(f"run_name={summary['run_name']}")
    print(f"data_loading_mode={summary['data_loading_mode']}")
    print(f"tokenizer_vocab_size={summary['tokenizer_vocab_size']}")
    print(f"input_ids_shape={tuple(summary['input_ids_shape'])}")
    print(f"targets_shape={tuple(summary['targets_shape'])}")
    print(f"logits_shape={tuple(summary['logits_shape'])}")
    print(f"parameter_count={summary['parameter_count']}")
    print(f"loss_value={summary['loss_value']:.6f}")
    print(f"val_loss_value={summary['val_loss_value']:.6f}")
    print(f"loss_finite={summary['loss_finite']}")
    print(f"val_loss_finite={summary['val_loss_finite']}")
    print(f"summary_path={repo_relative_path(summary_path)}")

    if not loss_finite or not val_loss_finite:
        print("failure: streaming public16k smoke loss is not finite")
        return 1
    print("success: streaming public16k data/model/loss smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
