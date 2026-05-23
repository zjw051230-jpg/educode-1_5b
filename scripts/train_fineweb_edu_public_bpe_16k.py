from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from tokenizers import Tokenizer
from tokenizers.decoders import ByteLevel as ByteLevelDecoder
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import ByteLevel
from tokenizers.trainers import BpeTrainer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "tokenizers" / "fineweb_edu_public_bpe_16k.json"
MIXED_DOMAIN_TOKENIZER_DIR = PROJECT_ROOT / "tokenizers" / "educode_bpe_mixed_domain_8k"


class JsonlTextIterator:
    def __init__(self, path: Path, text_field: str) -> None:
        self.path = path
        self.text_field = text_field
        self.records_seen = 0

    def __iter__(self) -> Iterator[str]:
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                if not raw_line.strip():
                    raise ValueError(f"line {line_number} is empty in {self.path}")
                record = json.loads(raw_line)
                text = record.get(self.text_field)
                if not isinstance(text, str):
                    raise ValueError(f"line {line_number} missing string field {self.text_field!r}")
                self.records_seen += 1
                if text:
                    yield text


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def resolve_repo_path(path_text: str) -> Path:
    return PROJECT_ROOT / Path(path_text)


def build_tokenizer(config: dict[str, Any], train_texts: JsonlTextIterator) -> Tokenizer:
    special_tokens = config["special_tokens"]
    unk_token = "<|unk|>"
    if unk_token not in special_tokens:
        raise ValueError(f"special_tokens must include {unk_token}")

    tokenizer = Tokenizer(BPE(unk_token=unk_token))
    tokenizer.pre_tokenizer = ByteLevel(add_prefix_space=False)
    tokenizer.decoder = ByteLevelDecoder()

    trainer = BpeTrainer(
        vocab_size=int(config["target_vocab_size"]),
        min_frequency=1,
        special_tokens=special_tokens,
        initial_alphabet=ByteLevel.alphabet(),
        show_progress=True,
    )
    tokenizer.train_from_iterator(train_texts, trainer=trainer)
    return tokenizer


def build_tokenizer_config(config: dict[str, Any], observed_vocab_size: int, special_token_ids: dict[str, int | None]) -> dict[str, Any]:
    return {
        "name": config["tokenizer_name"],
        "type": config["tokenizer_type"].upper(),
        "library": "tokenizers",
        "vocab_size_target": config["target_vocab_size"],
        "vocab_size_observed": observed_vocab_size,
        "special_tokens": config["special_tokens"],
        "special_token_ids": special_token_ids,
        "artifact_path": config["output_dir"],
        "tokenizer_json": config["output_tokenizer_json"],
        "input_train_jsonl": config["input_train_jsonl"],
        "input_val_jsonl": config["input_val_jsonl"],
        "text_field": config["text_field"],
        "dataset_id": config["dataset_id"],
        "dataset_config": config["dataset_config"],
        "source_slice": config["source_slice"],
        "license": config["license"],
        "seed": config["seed"],
        "existing_mixed_domain_tokenizer_unchanged": True,
        "is_production_tokenizer": False,
        "notes": config["notes"],
    }


def write_readme(output_dir: Path, config: dict[str, Any], observed_vocab_size: int, train_records_seen: int) -> None:
    readme_text = f"""# FineWeb-Edu Public BPE 16k

This directory stores the `{config['tokenizer_name']}` tokenizer artifact trained on the reviewed FineWeb-Edu 500MB public corpus train split.

Observed vocab size: {observed_vocab_size}
Target vocab size: {config['target_vocab_size']}
Input train split: `{config['input_train_jsonl']}`
Train records seen: {train_records_seen}
Dataset: `{config['dataset_id']}` / `{config['dataset_config']}`
License: `{config['license']}`

This is a new public-corpus tokenizer artifact. It does not overwrite or modify `tokenizers/educode_bpe_mixed_domain_8k/`.
"""
    (output_dir / "README.md").write_text(readme_text, encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the FineWeb-Edu public 16k BPE tokenizer.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to tokenizer config JSON.")
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    args = parse_args()
    config_path = Path(args.config)
    config = read_json(config_path)
    train_path = resolve_repo_path(config["input_train_jsonl"])
    output_dir = resolve_repo_path(config["output_dir"])
    output_tokenizer_json = resolve_repo_path(config["output_tokenizer_json"])

    if not train_path.exists():
        raise FileNotFoundError(f"missing train JSONL: {train_path}")
    if output_dir.resolve() == MIXED_DOMAIN_TOKENIZER_DIR.resolve():
        raise ValueError("output_dir must not point at the mixed-domain tokenizer artifact")
    if str(output_dir.resolve()).startswith(str(MIXED_DOMAIN_TOKENIZER_DIR.resolve())):
        raise ValueError("output_dir must not be inside the mixed-domain tokenizer artifact")

    output_dir.mkdir(parents=True, exist_ok=True)
    train_texts = JsonlTextIterator(train_path, config["text_field"])
    tokenizer = build_tokenizer(config, train_texts)
    tokenizer.save(str(output_tokenizer_json))

    observed_vocab_size = tokenizer.get_vocab_size()
    special_token_ids = {token: tokenizer.token_to_id(token) for token in config["special_tokens"]}
    if any(token_id is None for token_id in special_token_ids.values()):
        raise ValueError(f"missing special token ids: {special_token_ids}")

    tokenizer_config = build_tokenizer_config(config, observed_vocab_size, special_token_ids)
    write_json(output_dir / "tokenizer_config.json", tokenizer_config)

    training_summary = {
        "tokenizer_name": config["tokenizer_name"],
        "target_vocab_size": config["target_vocab_size"],
        "observed_vocab_size": observed_vocab_size,
        "train_records_seen": train_texts.records_seen,
        "text_field": config["text_field"],
        "input_train_jsonl": config["input_train_jsonl"],
        "output_tokenizer_json": config["output_tokenizer_json"],
        "special_tokens": config["special_tokens"],
        "special_token_ids": special_token_ids,
        "license": config["license"],
        "dataset_id": config["dataset_id"],
        "dataset_config": config["dataset_config"],
        "source_slice": config["source_slice"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "existing_mixed_domain_tokenizer_unchanged": True,
    }
    write_json(output_dir / "training_summary.json", training_summary)
    write_readme(output_dir, config, observed_vocab_size, train_texts.records_seen)

    print(f"tokenizer_name={training_summary['tokenizer_name']}")
    print(f"target_vocab_size={training_summary['target_vocab_size']}")
    print(f"observed_vocab_size={training_summary['observed_vocab_size']}")
    print(f"train_records_seen={training_summary['train_records_seen']}")
    print(f"special_token_ids={json.dumps(special_token_ids, ensure_ascii=False, sort_keys=True)}")
    print(f"output_tokenizer_json={training_summary['output_tokenizer_json']}")
    print("existing_mixed_domain_tokenizer_unchanged=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
