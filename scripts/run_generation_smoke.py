from __future__ import annotations

import json
import sys
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.eval import evaluate_next_token_loss  # noqa: E402
from educode.generation import generate_token_ids  # noqa: E402
from educode.inference import decode_one, prefill  # noqa: E402
from educode.kv_cache import KVCache  # noqa: E402
from educode.speculative import NgramProposer, speculative_decode_skeleton  # noqa: E402
from educode.tiny_model import TinyDecoderOnlyTransformer, TinyModelConfig  # noqa: E402


class ToyTokenizer:
    def encode(self, prompt: str) -> list[int]:
        return [min(ord(char), 31) for char in prompt] or [1]

    def decode(self, token_ids: list[int]) -> str:
        return "".join(chr(token_id % 32 + 65) for token_id in token_ids)


def main() -> int:
    torch.manual_seed(123)
    config = TinyModelConfig(vocab_size=32, context_length=16, num_layers=1, d_model=16, num_heads=4, d_ff=64)
    model = TinyDecoderOnlyTransformer(config)
    tokenizer = ToyTokenizer()
    generated = generate_token_ids(
        model,
        tokenizer,
        "abc",
        max_new_tokens=4,
        device=torch.device("cpu"),
        strategy="greedy",
        eos_token_id=None,
        seed=123,
    )
    input_ids = torch.tensor([[1, 2, 3, 4]], dtype=torch.long)
    target_ids = torch.tensor([[2, 3, 4, 5]], dtype=torch.long)
    eval_result = evaluate_next_token_loss(model, input_ids, target_ids)
    cache = KVCache(num_layers=1)
    prefill_logits, _ = prefill(model, input_ids, cache)
    decode_logits, _ = decode_one(model, input_ids[:, -1:], cache)
    speculative = speculative_decode_skeleton([1, 2, 1, 2], NgramProposer(), max_draft_tokens=3)
    summary = {
        "smoke_status": "passed",
        "generated_token_count": len(generated),
        "eval_loss": round(eval_result["loss"], 6),
        "eval_perplexity": round(eval_result["perplexity"], 6),
        "prefill_shape": list(prefill_logits.shape),
        "decode_shape": list(decode_logits.shape),
        "draft_token_count": len(speculative["draft_tokens"]),
        "loads_real_checkpoint": False,
        "runs_gpu": False,
        "starts_training": False,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
