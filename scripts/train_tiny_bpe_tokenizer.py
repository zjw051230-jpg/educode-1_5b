from __future__ import annotations

import json
from pathlib import Path

from tokenizers import Tokenizer
from tokenizers.decoders import ByteLevel as ByteLevelDecoder
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import ByteLevel
from tokenizers.trainers import BpeTrainer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = PROJECT_ROOT / "data" / "tokenizer_samples" / "tiny_educode_corpus.txt"
ARTIFACT_DIR = PROJECT_ROOT / "tokenizers" / "educode_bpe_toy_512"
SPECIAL_TOKENS = ["<pad>", "<bos>", "<eos>", "<unk>"]
VOCAB_SIZE = 512
MIN_FREQUENCY = 1


def main() -> int:
    if not CORPUS_PATH.exists():
        print(f"Missing corpus: {CORPUS_PATH}")
        return 1

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    tokenizer = Tokenizer(BPE(unk_token="<unk>"))
    tokenizer.pre_tokenizer = ByteLevel(add_prefix_space=False)
    tokenizer.decoder = ByteLevelDecoder()

    trainer = BpeTrainer(
        vocab_size=VOCAB_SIZE,
        min_frequency=MIN_FREQUENCY,
        special_tokens=SPECIAL_TOKENS,
        show_progress=False,
    )

    tokenizer.train([str(CORPUS_PATH)], trainer)

    tokenizer_json_path = ARTIFACT_DIR / "tokenizer.json"
    tokenizer.save(str(tokenizer_json_path))
    tokenizer.model.save(str(ARTIFACT_DIR))

    tokenizer_config = {
        "name": "educode_bpe_toy_512",
        "type": "BPE",
        "library": "tokenizers",
        "vocab_size_target": VOCAB_SIZE,
        "min_frequency": MIN_FREQUENCY,
        "special_tokens": SPECIAL_TOKENS,
        "artifact_path": "tokenizers/educode_bpe_toy_512",
        "corpus_path": "data/tokenizer_samples/tiny_educode_corpus.txt",
        "is_formal_tokenizer": False,
    }
    (ARTIFACT_DIR / "tokenizer_config.json").write_text(
        json.dumps(tokenizer_config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
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
    )

    readme_text = """# EduCode BPE Toy 512

This directory stores a tiny local BPE tokenizer artifact trained only on the repository sample corpus.
It is for tokenizer artifact-path validation only.
It is not the formal Windows 8k tokenizer and does not replace ByteTokenizer in the current smoke path.
"""
    (ARTIFACT_DIR / "README.md").write_text(readme_text, encoding="utf-8")

    print(f"Corpus path: {CORPUS_PATH}")
    print(f"Artifact dir: {ARTIFACT_DIR}")
    print(f"Tokenizer vocab size: {tokenizer.get_vocab_size()}")
    for token in SPECIAL_TOKENS:
        print(f"{token} id: {tokenizer.token_to_id(token)}")
    print(f"tokenizer.json exists: {tokenizer_json_path.exists()}")
    print(f"tokenizer_config.json exists: {(ARTIFACT_DIR / 'tokenizer_config.json').exists()}")
    print(f"special_tokens_map.json exists: {(ARTIFACT_DIR / 'special_tokens_map.json').exists()}")
    print(f"README.md exists: {(ARTIFACT_DIR / 'README.md').exists()}")
    print(f"vocab.json exists: {(ARTIFACT_DIR / 'vocab.json').exists()}")
    print(f"merges.txt exists: {(ARTIFACT_DIR / 'merges.txt').exists()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
