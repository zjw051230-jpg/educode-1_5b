from __future__ import annotations

import json
import sys
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from educode.kv_cache import KVCache  # noqa: E402
from educode.paged_cache import PagedBlockTable  # noqa: E402
from educode.sampling import sample_token, validate_sampling_args  # noqa: E402
from educode.speculative import NgramProposer, speculative_decode_skeleton  # noqa: E402


def build_summary() -> dict[str, object]:
    blockers: list[str] = []
    logits = torch.tensor([0.1, 0.2, 5.0, 0.3])
    token = sample_token(logits, temperature=1.0, top_k=2, top_p=0.95, generator=torch.Generator().manual_seed(1))
    if int(token.item()) not in range(4):
        blockers.append("sampled token is out of vocab range")

    bad_generation_config_rejected = False
    try:
        validate_sampling_args(temperature=0.0)
    except ValueError:
        bad_generation_config_rejected = True
    if not bad_generation_config_rejected:
        blockers.append("bad generation config was not rejected")

    cache = KVCache(num_layers=1)
    key = torch.zeros(1, 2, 1, 4)
    cache.append(0, key, key)
    cache.append(0, key, key)
    if cache.sequence_length() != 2:
        blockers.append("KV cache append/read length failed")
    cache.reset()
    if cache.sequence_length() != 0:
        blockers.append("KV cache reset failed")

    table = PagedBlockTable(block_size=4)
    blocks = table.allocate(sequence_id=7, token_count=9)
    if len(blocks) != 3 or table.lookup(7) != blocks:
        blockers.append("PagedAttention block table skeleton failed")

    speculative = speculative_decode_skeleton([1, 2, 1, 2], NgramProposer(), max_draft_tokens=3)
    if len(speculative["draft_tokens"]) != 3:
        blockers.append("fake speculative proposer failed")

    return {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "sampling_valid": not blockers,
        "bad_generation_config_rejected": bad_generation_config_rejected,
        "kv_cache_append_read_reset_passed": cache.sequence_length() == 0,
        "paged_block_table_passed": len(blocks) == 3,
        "speculative_interface_passed": len(speculative["draft_tokens"]) == 3,
        "loads_real_checkpoint": False,
        "runs_gpu": False,
        "starts_training": False,
    }


def main() -> int:
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
