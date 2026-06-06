from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.eval import checkpoint_metadata_summary, evaluate_next_token_loss
from educode.generation import generate_token_ids, greedy_next_token, sample_next_token
from educode.tiny_model import TinyDecoderOnlyTransformer, TinyModelConfig


class ToyTokenizer:
    def encode(self, text: str) -> list[int]:
        return [ord(ch) % 32 for ch in text] or [0]

    def decode(self, token_ids: list[int]) -> str:
        return " ".join(str(token_id) for token_id in token_ids)


def tiny_model() -> TinyDecoderOnlyTransformer:
    return TinyDecoderOnlyTransformer(
        TinyModelConfig(
            vocab_size=32,
            context_length=8,
            num_layers=1,
            d_model=16,
            num_heads=4,
            d_ff=32,
            dropout=0.0,
        )
    )


class GenerationEvalHarnessTests(unittest.TestCase):
    def test_greedy_and_sampling_helpers_return_valid_token_ids(self) -> None:
        logits = torch.tensor([0.1, 0.2, 3.0, 0.4])

        self.assertEqual(greedy_next_token(logits), 2)
        torch.manual_seed(123)
        sampled = sample_next_token(logits, temperature=1.0, top_k=2, top_p=0.9)
        self.assertIn(sampled, {2, 3})

    def test_generate_token_ids_greedy_smoke(self) -> None:
        model = tiny_model()
        token_ids = generate_token_ids(
            model=model,
            tokenizer=ToyTokenizer(),
            prompt="abc",
            max_new_tokens=3,
            device=torch.device("cpu"),
            strategy="greedy",
        )

        self.assertEqual(len(token_ids), 6)
        self.assertTrue(all(isinstance(token_id, int) for token_id in token_ids))

    def test_eval_harness_returns_finite_loss_and_perplexity(self) -> None:
        model = tiny_model()
        input_ids = torch.tensor([[1, 2, 3, 4]], dtype=torch.long)
        target_ids = torch.tensor([[2, 3, 4, 5]], dtype=torch.long)

        result = evaluate_next_token_loss(model, input_ids, target_ids)

        self.assertGreater(result["loss"], 0.0)
        self.assertGreater(result["perplexity"], 1.0)
        self.assertEqual(result["tokens_evaluated"], 4)

    def test_checkpoint_metadata_summary_does_not_load_weights(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "mock_checkpoint_metadata.json"
            path.write_text(json.dumps({"metadata": {"step": 12}}), encoding="utf-8")

            result = checkpoint_metadata_summary(path)

        self.assertTrue(result["metadata_loaded"])
        self.assertFalse(result["loads_model_weights"])
        self.assertEqual(result["metadata"]["step"], 12)


if __name__ == "__main__":
    unittest.main()
