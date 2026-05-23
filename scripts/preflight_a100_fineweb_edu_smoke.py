from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch
from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_50mb_300m_10step_smoke.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_repo_path(path_text: str) -> Path:
    return PROJECT_ROOT / Path(path_text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preflight checks for future A100 FineWeb-Edu smoke.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the A100 smoke config JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    config = load_json(config_path)

    train_path = resolve_repo_path(config["data"]["train_path"])
    val_path = resolve_repo_path(config["data"]["val_path"])
    tokenizer_path = resolve_repo_path(config["tokenizer"]["path"])
    expected_vocab_size = int(config["tokenizer"]["vocab_size"])
    output_dir = resolve_repo_path(config["run"]["output_dir"])

    if not train_path.exists():
        raise FileNotFoundError(f"missing train_path: {train_path}")
    if not val_path.exists():
        raise FileNotFoundError(f"missing val_path: {val_path}")
    if not tokenizer_path.exists():
        raise FileNotFoundError(f"missing tokenizer_path: {tokenizer_path}")
    if not output_dir.relative_to(PROJECT_ROOT).as_posix().startswith("experiments/a100/"):
        raise ValueError("output_dir must stay under experiments/a100/")

    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    loaded_vocab_size = tokenizer.get_vocab_size()
    if loaded_vocab_size != expected_vocab_size:
        raise ValueError(
            f"tokenizer vocab mismatch: expected {expected_vocab_size} but loaded {loaded_vocab_size}"
        )

    cuda_available = torch.cuda.is_available()
    device_count = torch.cuda.device_count() if cuda_available else 0
    gpu_name = torch.cuda.get_device_name(0) if cuda_available and device_count > 0 else "no cuda"
    cuda_version = torch.version.cuda
    bf16_supported = bool(torch.cuda.is_bf16_supported()) if cuda_available else False

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "preflight_summary.json"
    summary = {
        "config_path": config_path.relative_to(PROJECT_ROOT).as_posix(),
        "run_name": config["run"]["run_name"],
        "train_path": train_path.relative_to(PROJECT_ROOT).as_posix(),
        "val_path": val_path.relative_to(PROJECT_ROOT).as_posix(),
        "tokenizer_path": tokenizer_path.relative_to(PROJECT_ROOT).as_posix(),
        "tokenizer_vocab_size": loaded_vocab_size,
        "torch_cuda_available": cuda_available,
        "gpu_name": gpu_name,
        "device_count": device_count,
        "cuda_version": cuda_version,
        "bf16_supported": bf16_supported,
        "expected_gpu": config["hardware"].get("gpu", "A100"),
        "output_dir": output_dir.relative_to(PROJECT_ROOT).as_posix(),
        "no_training": True,
        "no_checkpoint": True,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"config_path={summary['config_path']}")
    print(f"train_path={summary['train_path']}")
    print(f"val_path={summary['val_path']}")
    print(f"tokenizer_path={summary['tokenizer_path']}")
    print(f"tokenizer_vocab_size={summary['tokenizer_vocab_size']}")
    print(f"torch_cuda_available={summary['torch_cuda_available']}")
    print(f"gpu_name={summary['gpu_name']}")
    print(f"device_count={summary['device_count']}")
    print(f"cuda_version={summary['cuda_version']}")
    print(f"bf16_supported={summary['bf16_supported']}")
    print(f"output_dir={summary['output_dir']}")
    print(f"summary_path={summary_path.relative_to(PROJECT_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
