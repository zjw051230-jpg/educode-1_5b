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
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "windows" / "fineweb_edu_50mb_mixed_tokenizer_smoke.json"
SUMMARY_PATH = (
    PROJECT_ROOT
    / "data"
    / "public_corpus"
    / "fineweb_edu_sample10bt_50mb"
    / "fineweb_edu_data_model_loss_smoke_summary.json"
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.config_loader import load_json_config
from educode.config_validator import validate_config
from educode.losses import next_token_cross_entropy
from educode.sequence_dataset import batch_samples, make_next_token_samples
from educode.tiny_model import TinyDecoderOnlyTransformer, model_config_from_dict


def resolve_repo_path(path_value: str) -> Path:
    return PROJECT_ROOT / Path(path_value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect FineWeb-Edu data/tokenizer/model/loss smoke path.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the smoke config JSON.")
    return parser.parse_args()


def choose_device(config: dict[str, Any]) -> torch.device:
    hardware = config.get("hardware", {}) if isinstance(config.get("hardware"), dict) else {}
    device_preference = str(hardware.get("device_preference", "cuda_if_available_else_cpu"))
    if device_preference == "cuda_if_available_else_cpu":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    requested_device = str(hardware.get("device", "cpu"))
    if requested_device == "cuda" and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def count_docs(path: Path) -> int:
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                raise ValueError(f"line {line_number} is empty in {path}")
            record = json.loads(raw_line)
            text = record.get("text")
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"line {line_number} is missing non-empty text in {path}")
            count += 1
    return count


def collect_train_token_ids(train_path: Path, tokenizer: Tokenizer, sequence_length: int, batch_size: int, eos_token_id: int | None) -> tuple[int, list[int]]:
    required_token_count = sequence_length + batch_size
    train_docs = 0
    token_ids: list[int] = []

    with train_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                raise ValueError(f"line {line_number} is empty in {train_path}")
            record = json.loads(raw_line)
            text = record.get("text")
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"line {line_number} is missing non-empty text in {train_path}")
            train_docs += 1
            if len(token_ids) >= required_token_count:
                continue

            encoded_ids = tokenizer.encode(text).ids
            token_ids.extend(encoded_ids)
            if eos_token_id is not None:
                token_ids.append(eos_token_id)

    return train_docs, token_ids


def write_summary(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    config = load_json_config(args.config)
    errors = validate_config(config, repo_root=PROJECT_ROOT)
    if errors:
        print("validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    seed = int(config.get("run", {}).get("seed", 42))
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    train_path = resolve_repo_path(config["data"]["train_path"])
    val_path = resolve_repo_path(config["data"]["val_path"])
    tokenizer_path = resolve_repo_path(config["tokenizer"]["path"])
    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    tokenizer_vocab_size = tokenizer.get_vocab_size()
    sequence_length = int(config["data"]["sequence_length"])
    batch_size = int(config["training"]["batch_size"])
    eos_token_id_value = config.get("tokenizer", {}).get("eos_token_id")
    eos_token_id = int(eos_token_id_value) if isinstance(eos_token_id_value, int) else None

    train_docs, token_ids = collect_train_token_ids(train_path, tokenizer, sequence_length, batch_size, eos_token_id)
    val_docs = count_docs(val_path)
    if train_docs <= 0:
        print("failure: no train documents found")
        return 1
    if val_docs <= 0:
        print("failure: no val documents found")
        return 1
    if len(token_ids) < sequence_length + batch_size:
        print("failure: not enough token ids for a full next-token batch")
        return 1

    samples = make_next_token_samples(token_ids, sequence_length)
    batches = batch_samples(samples, batch_size)
    if not batches:
        print("failure: no full batch could be created from FineWeb-Edu train tokens")
        return 1

    batch_x, batch_y = batches[0]
    input_ids = torch.tensor(batch_x, dtype=torch.long)
    target_ids = torch.tensor(batch_y, dtype=torch.long)

    device = choose_device(config)
    model = TinyDecoderOnlyTransformer(model_config_from_dict(config)).to(device)
    model.eval()
    input_ids = input_ids.to(device)
    target_ids = target_ids.to(device)

    with torch.no_grad():
        logits = model(input_ids)
        loss = next_token_cross_entropy(logits, target_ids)

    loss_value = float(loss.item())
    loss_finite = bool(torch.isfinite(loss).item())
    summary = {
        "train_docs": train_docs,
        "val_docs": val_docs,
        "tokenizer_path": config["tokenizer"]["path"],
        "tokenizer_vocab_size": tokenizer_vocab_size,
        "sequence_length": sequence_length,
        "batch_size": batch_size,
        "input_ids_shape": list(input_ids.shape),
        "targets_shape": list(target_ids.shape),
        "logits_shape": list(logits.shape),
        "loss_value": loss_value,
        "loss_finite": loss_finite,
        "device": str(device),
        "no_backward": True,
        "no_optimizer_step": True,
        "no_checkpoint": True,
        "no_training": True
    }
    write_summary(SUMMARY_PATH, summary)

    print(f"train_docs={summary['train_docs']}")
    print(f"val_docs={summary['val_docs']}")
    print(f"tokenizer_path={summary['tokenizer_path']}")
    print(f"tokenizer_vocab_size={summary['tokenizer_vocab_size']}")
    print(f"input_ids_shape={tuple(summary['input_ids_shape'])}")
    print(f"targets_shape={tuple(summary['targets_shape'])}")
    print(f"logits_shape={tuple(summary['logits_shape'])}")
    print(f"loss_value={summary['loss_value']:.6f}")
    print(f"loss_finite={summary['loss_finite']}")
    print(f"device={summary['device']}")
    print(f"summary_path={SUMMARY_PATH.relative_to(PROJECT_ROOT).as_posix()}")

    if loss_finite:
        print("success: FineWeb-Edu public corpus data/model/loss smoke passed")
        return 0

    print("failure: loss is not finite")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
