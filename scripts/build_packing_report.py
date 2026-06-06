from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.packing import PackingConfig, build_loss_mask, estimate_padding_waste, pack_documents  # noqa: E402


def build_report() -> dict:
    docs = [[1, 2, 3], [4, 5], [6, 7, 8]]
    config = PackingConfig(context_length=6, allow_cross_document_attention=False)
    packs = pack_documents(docs, config)
    return {
        "report_status": "generated",
        "packing": [pack.__dict__ for pack in packs],
        "loss_masks": [build_loss_mask(pack, config.context_length) for pack in packs],
        "padding_waste": estimate_padding_waste(docs, config),
        "raw_data_touched": False,
        "modal_gpu_training_run": False,
    }


def main() -> int:
    print(json.dumps(build_report(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
