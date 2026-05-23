from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "tokenizers" / "fineweb_edu_public_bpe_16k.json"
MIXED_DOMAIN_TOKENIZER_JSON = PROJECT_ROOT / "tokenizers" / "educode_bpe_mixed_domain_8k" / "tokenizer.json"
VALIDATION_SUMMARY_FILENAME = "validation_summary.json"
TRAIN_SAMPLE_LIMIT = 20
VAL_SAMPLE_LIMIT = 20
SAMPLE_CHAR_LIMIT = 2000


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def resolve_repo_path(path_text: str) -> Path:
    return PROJECT_ROOT / Path(path_text)


def load_samples(path: Path, text_field: str, limit: int) -> list[str]:
    samples: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                raise ValueError(f"line {line_number} is empty in {path}")
            record = json.loads(raw_line)
            text = record.get(text_field)
            if not isinstance(text, str):
                raise ValueError(f"line {line_number} missing string field {text_field!r}")
            if text:
                samples.append(text[:SAMPLE_CHAR_LIMIT])
            if len(samples) >= limit:
                break
    return samples


def validate_round_trip(tokenizer: Tokenizer, samples: list[str], unk_token_id: int | None) -> dict[str, Any]:
    pass_count = 0
    fail_count = 0
    total_chars = 0
    total_tokens = 0
    unk_token_count = 0
    failures: list[dict[str, str]] = []

    for index, text in enumerate(samples):
        encoding = tokenizer.encode(text)
        ids = encoding.ids
        decoded = tokenizer.decode(ids, skip_special_tokens=False)
        total_chars += len(text)
        total_tokens += len(ids)
        if unk_token_id is not None:
            unk_token_count += sum(1 for token_id in ids if token_id == unk_token_id)
        if decoded == text and ids:
            pass_count += 1
        else:
            fail_count += 1
            failures.append(
                {
                    "sample_index": str(index),
                    "original_prefix": text[:160],
                    "decoded_prefix": decoded[:160],
                }
            )

    chars_per_token = round(total_chars / total_tokens, 6) if total_tokens else 0.0
    average_tokens_per_char = round(total_tokens / total_chars, 6) if total_chars else 0.0
    return {
        "round_trip_pass_count": pass_count,
        "round_trip_fail_count": fail_count,
        "unk_token_count_on_samples": unk_token_count,
        "sampled_char_count": total_chars,
        "sampled_public_token_count": total_tokens,
        "chars_per_token": chars_per_token,
        "average_tokens_per_char": average_tokens_per_char,
        "round_trip_failures": failures[:5],
    }


def count_tokens(tokenizer: Tokenizer, samples: list[str]) -> int:
    return sum(len(tokenizer.encode(text).ids) for text in samples)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the FineWeb-Edu public 16k BPE tokenizer.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to tokenizer config JSON.")
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    args = parse_args()
    config = read_json(Path(args.config))
    tokenizer_path = resolve_repo_path(config["output_tokenizer_json"])
    output_dir = resolve_repo_path(config["output_dir"])
    train_path = resolve_repo_path(config["input_train_jsonl"])
    val_path = resolve_repo_path(config["input_val_jsonl"])

    if not tokenizer_path.exists():
        raise FileNotFoundError(f"missing tokenizer: {tokenizer_path}")
    if not MIXED_DOMAIN_TOKENIZER_JSON.exists():
        raise FileNotFoundError(f"missing mixed-domain tokenizer: {MIXED_DOMAIN_TOKENIZER_JSON}")

    public_tokenizer = Tokenizer.from_file(str(tokenizer_path))
    mixed_tokenizer = Tokenizer.from_file(str(MIXED_DOMAIN_TOKENIZER_JSON))
    public_vocab_size = public_tokenizer.get_vocab_size()
    mixed_vocab_size = mixed_tokenizer.get_vocab_size()
    target_vocab_size = int(config["target_vocab_size"])

    if public_vocab_size != target_vocab_size:
        raise ValueError(f"observed vocab size {public_vocab_size} != target {target_vocab_size}")

    special_token_ids = {token: public_tokenizer.token_to_id(token) for token in config["special_tokens"]}
    missing_special_tokens = [token for token, token_id in special_token_ids.items() if token_id is None]
    if missing_special_tokens:
        raise ValueError(f"missing special tokens: {missing_special_tokens}")

    train_samples = load_samples(train_path, config["text_field"], TRAIN_SAMPLE_LIMIT)
    val_samples = load_samples(val_path, config["text_field"], VAL_SAMPLE_LIMIT)
    samples = train_samples + val_samples
    unk_token_id = public_tokenizer.token_to_id("<|unk|>")
    round_trip = validate_round_trip(public_tokenizer, samples, unk_token_id)
    if round_trip["round_trip_fail_count"] != 0:
        raise ValueError(f"round-trip failures detected: {round_trip['round_trip_failures']}")

    sampled_public_token_count = round_trip["sampled_public_token_count"]
    sampled_mixed_token_count = count_tokens(mixed_tokenizer, samples)
    token_count_ratio_public_vs_mixed = (
        round(sampled_public_token_count / sampled_mixed_token_count, 6) if sampled_mixed_token_count else 0.0
    )

    summary = {
        "tokenizer_name": config["tokenizer_name"],
        "target_vocab_size": target_vocab_size,
        "observed_vocab_size": public_vocab_size,
        "mixed_tokenizer_vocab_size": mixed_vocab_size,
        "special_tokens": config["special_tokens"],
        "special_token_ids": special_token_ids,
        "train_samples_checked": len(train_samples),
        "val_samples_checked": len(val_samples),
        "round_trip_pass_count": round_trip["round_trip_pass_count"],
        "round_trip_fail_count": round_trip["round_trip_fail_count"],
        "unk_token_count_on_samples": round_trip["unk_token_count_on_samples"],
        "sampled_char_count": round_trip["sampled_char_count"],
        "sampled_public_token_count": sampled_public_token_count,
        "sampled_mixed_token_count": sampled_mixed_token_count,
        "token_count_ratio_public_vs_mixed": token_count_ratio_public_vs_mixed,
        "chars_per_token": round_trip["chars_per_token"],
        "average_tokens_per_char": round_trip["average_tokens_per_char"],
        "input_train_jsonl": config["input_train_jsonl"],
        "input_val_jsonl": config["input_val_jsonl"],
        "public_tokenizer_json": config["output_tokenizer_json"],
        "mixed_tokenizer_json": "tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json",
        "existing_mixed_domain_tokenizer_unchanged": True,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    summary_path = output_dir / VALIDATION_SUMMARY_FILENAME
    write_json(summary_path, summary)

    print(f"observed_vocab_size={public_vocab_size}")
    print(f"mixed_tokenizer_vocab_size={mixed_vocab_size}")
    print(f"special_token_ids={json.dumps(special_token_ids, ensure_ascii=False, sort_keys=True)}")
    print(f"train_samples_checked={summary['train_samples_checked']}")
    print(f"val_samples_checked={summary['val_samples_checked']}")
    print(f"round_trip_pass_count={summary['round_trip_pass_count']}")
    print(f"round_trip_fail_count={summary['round_trip_fail_count']}")
    print(f"unk_token_count_on_samples={summary['unk_token_count_on_samples']}")
    print(f"sampled_public_token_count={sampled_public_token_count}")
    print(f"sampled_mixed_token_count={sampled_mixed_token_count}")
    print(f"token_count_ratio_public_vs_mixed={token_count_ratio_public_vs_mixed}")
    print(f"validation_summary_path={summary_path.relative_to(PROJECT_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
