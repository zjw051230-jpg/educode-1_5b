from __future__ import annotations

import sys
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from educode.bpe_tokenizer import BPETokenizer
from educode.losses import next_token_cross_entropy
from educode.sequence_dataset import batch_samples, make_next_token_samples
from educode.tiny_model import TinyDecoderOnlyTransformer, TinyModelConfig

TOKENIZER_PATH = PROJECT_ROOT / "tokenizers" / "educode_bpe_toy_512" / "tokenizer.json"
SAMPLE_LINES = [
    "hello world",
    "Transformer models predict the next token.",
    "Python code: print('hello')",
    "loss = F.cross_entropy(logits, targets)",
]


def main() -> int:
    tokenizer = BPETokenizer(TOKENIZER_PATH)
    text = "\n".join(SAMPLE_LINES)
    token_ids = tokenizer.encode(text)
    if len(token_ids) < 2:
        print("failure: not enough token ids for next-token samples")
        return 1

    sequence_length = min(16, len(token_ids) - 1)
    batch_size = 2
    samples = make_next_token_samples(token_ids, sequence_length)
    batches = batch_samples(samples, batch_size)
    if not batches:
        print("failure: no full batches were created")
        return 1

    batch_x, batch_y = batches[0]
    input_ids = torch.tensor(batch_x, dtype=torch.long)
    target_ids = torch.tensor(batch_y, dtype=torch.long)

    model_config = TinyModelConfig(
        vocab_size=tokenizer.get_vocab_size(),
        context_length=max(sequence_length, 16),
        num_layers=2,
        d_model=128,
        num_heads=4,
        d_ff=512,
        attention_backend="sdpa",
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TinyDecoderOnlyTransformer(model_config).to(device)
    model.eval()
    input_ids = input_ids.to(device)
    target_ids = target_ids.to(device)

    with torch.no_grad():
        logits = model(input_ids)
        loss = next_token_cross_entropy(logits, target_ids)

    loss_value = float(loss.item())
    loss_finite = bool(torch.isfinite(loss).item())
    decoded_preview = tokenizer.decode(token_ids[: min(32, len(token_ids))])

    print(f"tokenizer path: {TOKENIZER_PATH}")
    print(f"tokenizer vocab size: {tokenizer.get_vocab_size()}")
    print(f"token count: {len(token_ids)}")
    print(f"sequence_length: {sequence_length}")
    print(f"batch_size: {batch_size}")
    print(f"input_ids shape: {tuple(input_ids.shape)}")
    print(f"target_ids shape: {tuple(target_ids.shape)}")
    print(f"logits shape: {tuple(logits.shape)}")
    print(f"loss value: {loss_value:.6f}")
    print(f"loss finite check: {loss_finite}")
    print(f"decoded preview: {decoded_preview}")
    print("round trip checks:")
    for line in SAMPLE_LINES:
        print(f"- {line!r}: {tokenizer.round_trip_ok(line)}")

    if loss_finite:
        print("success: BPE token ids can enter the model/loss smoke path")
        return 0

    print("failure: loss is not finite")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
