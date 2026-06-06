from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.eval import checkpoint_metadata_summary, evaluate_next_token_loss
from educode.generation import generate_token_ids
from educode.tiny_model import TinyDecoderOnlyTransformer, TinyModelConfig


class TinyTokenizer:
    vocab_size = 32

    def encode(self, text: str) -> list[int]:
        return [min(ord(ch), self.vocab_size - 1) for ch in text] or [0]

    def decode(self, token_ids: list[int]) -> str:
        return "".join(chr(token_id) for token_id in token_ids if 0 <= token_id < self.vocab_size)


def main() -> int:
    torch.manual_seed(123)
    config = TinyModelConfig(
        vocab_size=32,
        context_length=8,
        num_layers=1,
        d_model=16,
        num_heads=4,
        d_ff=32,
        dropout=0.0,
    )
    model = TinyDecoderOnlyTransformer(config)
    tokenizer = TinyTokenizer()
    generated_ids = generate_token_ids(
        model=model,
        tokenizer=tokenizer,
        prompt="abc",
        max_new_tokens=4,
        device=torch.device("cpu"),
        strategy="greedy",
    )
    input_ids = torch.tensor([[1, 2, 3, 4]], dtype=torch.long)
    target_ids = torch.tensor([[2, 3, 4, 5]], dtype=torch.long)
    eval_summary = evaluate_next_token_loss(model, input_ids, target_ids)

    with tempfile.TemporaryDirectory(prefix="generation_smoke_") as temp_dir:
        metadata_path = Path(temp_dir) / "mock_checkpoint_metadata.json"
        metadata_path.write_text(
            json.dumps({"metadata": {"step": 0, "kind": "mock_metadata_only"}}, indent=2) + "\n",
            encoding="utf-8",
        )
        metadata_summary = checkpoint_metadata_summary(metadata_path)

    result = {
        "smoke_status": "passed",
        "generated_token_count": len(generated_ids),
        "eval_loss": round(eval_summary["loss"], 6),
        "eval_perplexity": round(eval_summary["perplexity"], 6),
        "checkpoint_metadata_loaded": metadata_summary["metadata_loaded"],
        "loads_model_weights": metadata_summary["loads_model_weights"],
        "modal_gpu_training_executed": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
