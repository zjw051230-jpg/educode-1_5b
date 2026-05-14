from __future__ import annotations

import json
import sys
from pathlib import Path

from tokenizers import Tokenizer
from tokenizers.decoders import ByteLevel as ByteLevelDecoder
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import ByteLevel
from tokenizers.trainers import BpeTrainer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = PROJECT_ROOT / "data" / "real_corpus" / "processed" / "synthetic_expanded.processed.jsonl"
ARTIFACT_DIR = PROJECT_ROOT / "tokenizers" / "educode_bpe_expanded_8k"
TOKENIZER_NAME = "educode_bpe_expanded_8k"
TARGET_VOCAB_SIZE = 8192
TRAIN_SPLIT = "train"
SPECIAL_TOKENS = ["<pad>", "<bos>", "<eos>", "<unk>"]


def load_train_texts() -> tuple[int, int, list[str]]:
    if not CORPUS_PATH.exists():
        raise FileNotFoundError(f"missing processed corpus: {CORPUS_PATH}")

    input_docs = 0
    train_docs_used = 0
    train_texts: list[str] = []

    with CORPUS_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            input_docs += 1
            if record.get("split") != TRAIN_SPLIT:
                continue
            text = record.get("text")
            if not isinstance(text, str) or not text.strip():
                continue
            train_docs_used += 1
            train_texts.append(text)

    return input_docs, train_docs_used, train_texts


def build_tokenizer(train_texts: list[str]) -> Tokenizer:
    tokenizer = Tokenizer(BPE(unk_token="<unk>"))
    tokenizer.pre_tokenizer = ByteLevel(add_prefix_space=False)
    tokenizer.decoder = ByteLevelDecoder()

    trainer = BpeTrainer(
        vocab_size=TARGET_VOCAB_SIZE,
        min_frequency=1,
        special_tokens=SPECIAL_TOKENS,
        initial_alphabet=ByteLevel.alphabet(),
        show_progress=False,
    )

    tokenizer.train_from_iterator(train_texts, trainer=trainer)
    return tokenizer


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    input_docs, train_docs_used, train_texts = load_train_texts()
    if not train_texts:
        print(f"No train texts found in {CORPUS_PATH}")
        return 1

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    tokenizer = build_tokenizer(train_texts)
    tokenizer_json_path = ARTIFACT_DIR / "tokenizer.json"
    tokenizer.save(str(tokenizer_json_path))
    tokenizer.model.save(str(ARTIFACT_DIR))

    observed_vocab_size = tokenizer.get_vocab_size()
    special_token_ids = {token: tokenizer.token_to_id(token) for token in SPECIAL_TOKENS}

    tokenizer_config = {
        "name": TOKENIZER_NAME,
        "type": "BPE",
        "library": "tokenizers",
        "vocab_size_target": TARGET_VOCAB_SIZE,
        "vocab_size_observed": observed_vocab_size,
        "special_tokens": SPECIAL_TOKENS,
        "special_token_ids": special_token_ids,
        "artifact_path": "tokenizers/educode_bpe_expanded_8k",
        "tokenizer_json": "tokenizers/educode_bpe_expanded_8k/tokenizer.json",
        "corpus_path": "data/real_corpus/processed/synthetic_expanded.processed.jsonl",
        "splits_used": [TRAIN_SPLIT],
        "input_docs": input_docs,
        "train_docs_used": train_docs_used,
        "is_production_tokenizer": False,
        "notes": "Expanded-corpus BPE tokenizer artifact trained only on the processed synthetic expanded corpus train split.",
    }
    (ARTIFACT_DIR / "tokenizer_config.json").write_text(
        json.dumps(tokenizer_config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    special_tokens_map = {
        "pad_token": "<pad>",
        "bos_token": "<bos>",
        "eos_token": "<eos>",
        "unk_token": "<unk>",
    }
    (ARTIFACT_DIR / "special_tokens_map.json").write_text(
        json.dumps(special_tokens_map, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    readme_text = f"""# EduCode Expanded BPE 8k

This directory stores the `educode_bpe_expanded_8k` tokenizer artifact trained only on the processed expanded synthetic corpus.
It is a tokenizer-only artifact for later data/model smoke work.
It is not a production tokenizer and does not imply real-data readiness.

Observed vocab size: {observed_vocab_size}
Target vocab size: {TARGET_VOCAB_SIZE}
Corpus path: `data/real_corpus/processed/synthetic_expanded.processed.jsonl`
Train split used: `{TRAIN_SPLIT}` only
"""
    (ARTIFACT_DIR / "README.md").write_text(readme_text, encoding="utf-8", newline="\n")

    print(f"input docs: {input_docs}")
    print(f"train docs used: {train_docs_used}")
    print(f"target vocab size: {TARGET_VOCAB_SIZE}")
    print(f"observed vocab size: {observed_vocab_size}")
    print("special token ids:")
    for token in SPECIAL_TOKENS:
        print(f"- {token}: {special_token_ids[token]}")
    print(f"artifact path: {ARTIFACT_DIR.relative_to(PROJECT_ROOT).as_posix()}")
    if observed_vocab_size < TARGET_VOCAB_SIZE:
        print("warning: observed vocab size is below target because the current corpus is still small")
    print(f"tokenizer.json exists: {tokenizer_json_path.exists()}")
    print(f"tokenizer_config.json exists: {(ARTIFACT_DIR / 'tokenizer_config.json').exists()}")
    print(f"special_tokens_map.json exists: {(ARTIFACT_DIR / 'special_tokens_map.json').exists()}")
    print(f"README.md exists: {(ARTIFACT_DIR / 'README.md').exists()}")
    print(f"vocab.json exists: {(ARTIFACT_DIR / 'vocab.json').exists()}")
    print(f"merges.txt exists: {(ARTIFACT_DIR / 'merges.txt').exists()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
