from __future__ import annotations

import json
import sys
from pathlib import Path

import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.lora import LoRAConfig, LoRALinear, adapter_state_dict  # noqa: E402
from src.educode.peft import find_target_linear_modules  # noqa: E402


def main() -> int:
    torch.manual_seed(0)
    base = torch.nn.Linear(4, 3)
    disabled = LoRALinear(base, LoRAConfig(rank=2, alpha=4.0, enabled=False))
    x = torch.randn(2, 4)
    disabled_matches_base = torch.allclose(disabled(x), base(x))

    enabled = LoRALinear(torch.nn.Linear(4, 3), LoRAConfig(rank=2, alpha=4.0, enabled=True))
    trainable = [name for name, p in enabled.named_parameters() if p.requires_grad]
    targets = find_target_linear_modules(torch.nn.Sequential(torch.nn.Linear(4, 4), torch.nn.Linear(4, 2)))
    state = adapter_state_dict({"adapter": enabled})

    blockers = []
    if not disabled_matches_base:
        blockers.append("disabled_path_does_not_match_base")
    if trainable != ["lora_a", "lora_b"]:
        blockers.append("unexpected_trainable_parameters")
    if targets != ["0", "1"]:
        blockers.append("target_linear_selection_failed")
    if set(state) != {"adapter.lora_a", "adapter.lora_b"}:
        blockers.append("adapter_state_filter_failed")

    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "disabled_path_equals_base": bool(disabled_matches_base),
        "trainable_parameters": trainable,
        "target_modules": targets,
        "adapter_state_keys": sorted(state),
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
