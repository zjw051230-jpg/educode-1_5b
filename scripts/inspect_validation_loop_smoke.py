from __future__ import annotations

import json
import sys
from pathlib import Path

import torch
from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.config_loader import load_json_config
from educode.config_validator import validate_config
from educode.losses import next_token_cross_entropy
from educode.sequence_dataset import batch_samples, make_next_token_samples
from educode.tiny_model import TinyDecoderOnlyTransformer, model_config_from_dict

CONFIG_PATH = PROJECT_ROOT / "configs" / "windows" / "bpe_8k_formal_placeholder.json"
TRAIN_SPLIT_PATH = PROJECT_ROOT / "data" / "real_corpus" / "splits" / "synthetic_seed.train.jsonl"
VAL_SPLIT_PATH = PROJECT_ROOT / "data" / "real_corpus" / "splits" / "synthetic_seed.val.jsonl"


def load_split_texts(split_path: Path) -> list[str]:
    texts: list[str] = []
    with split_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            text = record.get("text")
            if isinstance(text, str) and text.strip():
                texts.append(text)
    return texts


def build_batch(tokenizer: Tokenizer, texts: list[str], sequence_length: int, batch_size: int) -> tuple[torch.Tensor, torch.Tensor, int]:
    combined_text = "\n\n".join(texts)
    token_ids = tokenizer.encode(combined_text).ids
    if len(token_ids) < 2:
        raise ValueError("not enough token ids for next-token samples")

    samples = make_next_token_samples(token_ids, sequence_length)
    batches = batch_samples(samples, batch_size)
    if not batches:
        raise ValueError("no full batch could be created")

    batch_x, batch_y = batches[0]
    input_ids = torch.tensor(batch_x, dtype=torch.long)
    target_ids = torch.tensor(batch_y, dtype=torch.long)
    return input_ids, target_ids, len(token_ids)


def parameter_snapshots(model: torch.nn.Module) -> list[torch.Tensor]:
    return [parameter.detach().cpu().clone() for parameter in model.parameters()]


def main() -> int:
    config = load_json_config(CONFIG_PATH)
    errors = validate_config(config, repo_root=PROJECT_ROOT)
    if errors:
        print("validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    tokenizer_path = PROJECT_ROOT / config["tokenizer"]["path"]
    tokenizer = Tokenizer.from_file(str(tokenizer_path))

    train_texts = load_split_texts(TRAIN_SPLIT_PATH)
    val_texts = load_split_texts(VAL_SPLIT_PATH)
    if not train_texts:
        print("failure: no train texts found")
        return 1
    if not val_texts:
        print("failure: no val texts found")
        return 1

    sequence_length = min(config["model"]["context_length"], 64)
    batch_size = min(config["training"].get("batch_size", 1), 4)

    train_input_ids, train_target_ids, train_tokens = build_batch(tokenizer, train_texts, sequence_length, batch_size)
    val_input_ids, val_target_ids, val_tokens = build_batch(tokenizer, val_texts, sequence_length, batch_size)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TinyDecoderOnlyTransformer(model_config_from_dict(config)).to(device)
    model.eval()

    parameters_before = parameter_snapshots(model)

    train_input_ids = train_input_ids.to(device)
    train_target_ids = train_target_ids.to(device)
    val_input_ids = val_input_ids.to(device)
    val_target_ids = val_target_ids.to(device)

    with torch.no_grad():
        train_logits = model(train_input_ids)
        train_loss = next_token_cross_entropy(train_logits, train_target_ids)
        val_logits = model(val_input_ids)
        val_loss = next_token_cross_entropy(val_logits, val_target_ids)

    parameters_after = parameter_snapshots(model)
    parameters_unchanged = all(torch.equal(before, after) for before, after in zip(parameters_before, parameters_after))

    train_loss_value = float(train_loss.item())
    val_loss_value = float(val_loss.item())
    train_loss_finite = bool(torch.isfinite(train_loss).item())
    val_loss_finite = bool(torch.isfinite(val_loss).item())
    both_finite = train_loss_finite and val_loss_finite

    print(f"train docs: {len(train_texts)}")
    print(f"val docs: {len(val_texts)}")
    print(f"train tokens: {train_tokens}")
    print(f"val tokens: {val_tokens}")
    print(f"input shape: {tuple(train_input_ids.shape)}")
    print(f"logits shape: {tuple(train_logits.shape)}")
    print(f"train_loss: {train_loss_value:.6f}")
    print(f"val_loss: {val_loss_value:.6f}")
    print(f"both finite: {both_finite}")
    print(f"parameters unchanged: {parameters_unchanged}")
    print(f"device: {device}")

    if both_finite and parameters_unchanged:
        print("success: one-batch train/val validation smoke passed")
        return 0

    print("failure: validation smoke checks did not pass")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
