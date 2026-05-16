# draft_status: candidate
# topic_id: COD-012
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Tokenizer path resolution example using pathlib joins."""

from pathlib import Path


def resolve_tokenizer_dir(repo_root: Path, tokenizer_name: str) -> Path:
    return repo_root / "tokenizers" / tokenizer_name


def main() -> None:
    repo_root = Path("/example/repo")
    resolved = resolve_tokenizer_dir(repo_root, "toy_bpe")

    print(resolved)
    assert resolved.as_posix().endswith("tokenizers/toy_bpe")


if __name__ == "__main__":
    main()
