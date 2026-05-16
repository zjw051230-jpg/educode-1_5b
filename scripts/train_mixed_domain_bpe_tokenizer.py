from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from tokenizers import Tokenizer
from tokenizers.decoders import ByteLevel as ByteLevelDecoder
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import ByteLevel
from tokenizers.trainers import BpeTrainer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = PROJECT_ROOT / "data" / "real_corpus" / "processed" / "mixed_domain_external.processed.jsonl"
ARTIFACT_DIR = PROJECT_ROOT / "tokenizers" / "educode_bpe_mixed_domain_8k"
TOKENIZER_NAME = "educode_bpe_mixed_domain_8k"
TARGET_VOCAB_SIZE = 8192
TRAIN_SPLIT = "train"
SPECIAL_TOKENS = ["<pad>", "<bos>", "<eos>", "<unk>"]
PROJECT_BACKBONE = "CS / ML / Python / Transformer training systems education"


def load_train_texts() -> tuple[int, int, list[str], dict[str, int], dict[str, int]]:
    if not CORPUS_PATH.exists():
        raise FileNotFoundError(f"missing processed corpus: {CORPUS_PATH}")

    input_docs = 0
    train_docs_used = 0
    train_texts: list[str] = []
    all_source_category_counts: dict[str, int] = {}
    train_source_category_counts: dict[str, int] = {}

    with CORPUS_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue

            record = json.loads(line)
            input_docs += 1

            source_category = record.get("source_category")
            if not isinstance(source_category, str) or not source_category:
                raise ValueError(f"record missing valid source_category: {record}")
            all_source_category_counts[source_category] = all_source_category_counts.get(source_category, 0) + 1

            if record.get("split") != TRAIN_SPLIT:
                continue

            text = record.get("text")
            if not isinstance(text, str) or not text.strip():
                continue

            train_docs_used += 1
            train_texts.append(text)
            train_source_category_counts[source_category] = train_source_category_counts.get(source_category, 0) + 1

    return input_docs, train_docs_used, train_texts, all_source_category_counts, train_source_category_counts



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



def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")



def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    input_docs, train_docs_used, train_texts, all_source_category_counts, train_source_category_counts = load_train_texts()
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
        "artifact_path": "tokenizers/educode_bpe_mixed_domain_8k",
        "tokenizer_json": "tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json",
        "corpus_path": "data/real_corpus/processed/mixed_domain_external.processed.jsonl",
        "splits_used": [TRAIN_SPLIT],
        "input_docs": input_docs,
        "train_docs_used": train_docs_used,
        "input_source_category_counts": all_source_category_counts,
        "train_source_category_counts": train_source_category_counts,
        "external_general_text_is_supplement_only": True,
        "project_backbone": PROJECT_BACKBONE,
        "is_production_tokenizer": False,
        "notes": "Mixed/domain BPE tokenizer artifact trained on the approved mixed_domain_external corpus train split only. external_general_text remains supplement only.",
    }
    write_json(ARTIFACT_DIR / "tokenizer_config.json", tokenizer_config)

    special_tokens_map = {
        "pad_token": "<pad>",
        "bos_token": "<bos>",
        "eos_token": "<eos>",
        "unk_token": "<unk>",
    }
    write_json(ARTIFACT_DIR / "special_tokens_map.json", special_tokens_map)

    readme_text = f"""# EduCode Mixed Domain BPE 8k

This directory stores the `educode_bpe_mixed_domain_8k` tokenizer artifact trained on the approved `mixed_domain_external` corpus.
It is a tokenizer-only artifact for later smoke validation work.
It does not replace the D9 domain tokenizer artifact and does not imply model-quality claims.
The `external_general_text` portion remains supplement only.

Observed vocab size: {observed_vocab_size}
Target vocab size: {TARGET_VOCAB_SIZE}
Corpus path: `data/real_corpus/processed/mixed_domain_external.processed.jsonl`
Train split used: `{TRAIN_SPLIT}` only
Train docs used: {train_docs_used}
Train source_category counts: `{json.dumps(train_source_category_counts, ensure_ascii=False, sort_keys=True)}`
"""
    (ARTIFACT_DIR / "README.md").write_text(readme_text, encoding="utf-8", newline="\n")

    print(f"train docs used: {train_docs_used}")
    print(f"source_category counts: {json.dumps(train_source_category_counts, ensure_ascii=False, sort_keys=True)}")
    print(f"target vocab size: {TARGET_VOCAB_SIZE}")
    print(f"observed vocab size: {observed_vocab_size}")
    print("special token ids:")
    for token in SPECIAL_TOKENS:
        print(f"- {token}: {special_token_ids[token]}")
    print(f"artifact path: {ARTIFACT_DIR.relative_to(PROJECT_ROOT).as_posix()}")
    if observed_vocab_size < TARGET_VOCAB_SIZE:
        print("warning: observed vocab size is below target because the current corpus remains small")
    print(f"tokenizer.json exists: {tokenizer_json_path.exists()}")
    print(f"tokenizer_config.json exists: {(ARTIFACT_DIR / 'tokenizer_config.json').exists()}")
    print(f"special_tokens_map.json exists: {(ARTIFACT_DIR / 'special_tokens_map.json').exists()}")
    print(f"README.md exists: {(ARTIFACT_DIR / 'README.md').exists()}")
    print(f"vocab.json exists: {(ARTIFACT_DIR / 'vocab.json').exists()}")
    print(f"merges.txt exists: {(ARTIFACT_DIR / 'merges.txt').exists()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
