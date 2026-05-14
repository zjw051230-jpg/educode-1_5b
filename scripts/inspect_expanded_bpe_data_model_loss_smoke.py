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

CONFIG_PATH = PROJECT_ROOT / "configs" / "windows" / "bpe_expanded_8k_smoke.json"
PROCESSED_PATH = PROJECT_ROOT / "data" / "real_corpus" / "processed" / "synthetic_expanded.processed.jsonl"
TRAIN_SPLIT = "train"


def load_train_texts() -> list[str]:
    train_texts: list[str] = []
    with PROCESSED_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get("split") != TRAIN_SPLIT:
                continue
            text = record.get("text")
            if isinstance(text, str) and text.strip():
                train_texts.append(text)
    return train_texts


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
    train_texts = load_train_texts()
    if not train_texts:
        print("failure: no train texts found in processed expanded synthetic corpus")
        return 1

    combined_text = "\n\n".join(train_texts)
    encoding = tokenizer.encode(combined_text)
    token_ids = encoding.ids
    if len(token_ids) < 2:
        print("failure: not enough token ids for next-token samples")
        return 1

    sequence_length = min(config["model"]["context_length"], 128)
    batch_size = min(config["training"].get("batch_size", 1), 4)

    samples = make_next_token_samples(token_ids, sequence_length)
    batches = batch_samples(samples, batch_size)
    if not batches:
        print("failure: no full batch could be created from the expanded BPE train corpus")
        return 1

    batch_x, batch_y = batches[0]
    input_ids = torch.tensor(batch_x, dtype=torch.long)
    target_ids = torch.tensor(batch_y, dtype=torch.long)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TinyDecoderOnlyTransformer(model_config_from_dict(config)).to(device)
    model.eval()
    input_ids = input_ids.to(device)
    target_ids = target_ids.to(device)

    with torch.no_grad():
        logits = model(input_ids)
        loss = next_token_cross_entropy(logits, target_ids)

    loss_value = float(loss.item())
    loss_finite = bool(torch.isfinite(loss).item())
    decoded_preview = tokenizer.decode(token_ids[: min(64, len(token_ids))])

    print(f"config path: {CONFIG_PATH.relative_to(PROJECT_ROOT).as_posix()}")
    print(f"tokenizer vocab size: {tokenizer.get_vocab_size()}")
    print(f"train docs: {len(train_texts)}")
    print(f"total token count: {len(token_ids)}")
    print(f"sequence_length: {sequence_length}")
    print(f"batch_size: {batch_size}")
    print(f"input_ids shape: {tuple(input_ids.shape)}")
    print(f"logits shape: {tuple(logits.shape)}")
    print(f"loss value: {loss_value:.6f}")
    print(f"loss finite: {loss_finite}")
    print(f"decoded preview: {decoded_preview}")
    print(f"device: {device}")

    if loss_finite:
        print("success: expanded BPE processed-data model/loss smoke passed")
        return 0

    print("failure: loss is not finite")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
