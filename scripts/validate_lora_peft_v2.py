from __future__ import annotations

import json
import sys
from pathlib import Path

import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.lora import (  # noqa: E402
    LoRAConfig,
    LoRALinear,
    adapter_state_dict,
    count_trainable_parameters,
)
from src.educode.peft import select_lora_targets  # noqa: E402


def main() -> int:
    torch.manual_seed(0)
    base = torch.nn.Linear(4, 3)
    disabled = LoRALinear(base, LoRAConfig(rank=2, alpha=4, enabled=False))
    x = torch.randn(2, 4)
    disabled_equal = bool(torch.allclose(disabled(x), base(x)))
    enabled = LoRALinear(torch.nn.Linear(4, 3), LoRAConfig(rank=2, alpha=4, enabled=True))
    state = adapter_state_dict(enabled)
    trainable = count_trainable_parameters(enabled)
    before = enabled(x)
    enabled.merge()
    merged = enabled(x)
    enabled.unmerge()
    after = enabled(x)
    reversible = bool(torch.allclose(before, merged, atol=1e-6) and torch.allclose(before, after, atol=1e-6))
    blockers = []
    if not disabled_equal:
        blockers.append("disabled_path_not_equal")
    if set(state) != {"lora_a", "lora_b"}:
        blockers.append("adapter_state_dict_has_non_adapter_keys")
    if trainable["trainable_names"] != ["lora_a", "lora_b"]:
        blockers.append("unexpected_trainable_parameters")
    if not reversible:
        blockers.append("merge_unmerge_not_reversible")
    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "disabled_path_equals_base": disabled_equal,
        "adapter_state_keys": sorted(state),
        "trainable_report": trainable,
        "target_modules": select_lora_targets(torch.nn.Sequential(torch.nn.Linear(4, 4), torch.nn.Linear(4, 2))),
        "merge_unmerge_reversible": reversible,
        "modal_gpu_training_run": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
