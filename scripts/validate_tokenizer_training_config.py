from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.tokenizer_training import TokenizerTrainingConfig, ToyByteTokenizer, vocab_stats


def main() -> int:
    config = TokenizerTrainingConfig(vocab_size=256, min_frequency=2, sample_limit=100)
    tokenizer = ToyByteTokenizer()
    text = "EduCode tokenizer toy fixture"
    round_trip_ok = tokenizer.decode(tokenizer.encode(text)) == text
    payload = {
        "validation_status": "passed" if round_trip_ok else "failed",
        "algorithm": config.algorithm,
        "planned_vocab_size": config.vocab_size,
        "toy_vocab_stats": vocab_stats(tokenizer),
        "round_trip_ok": round_trip_ok,
        "real_tokenizer_trained": False,
        "raw_data_processed": False,
        "modal_used": False,
        "gpu_used": False,
        "training_started": False,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["validation_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
