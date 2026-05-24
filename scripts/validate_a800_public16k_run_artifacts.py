from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "experiments" / "a100" / "fineweb_edu_500mb_300m_1000step_public16k_execute"
EXPECTED_TOKENIZER_VOCAB_SIZE = 16384
MIN_VALIDATION_ROWS = 10


def resolve_repo_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def repo_relative_path(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_jsonl_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def path_is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate A800/A100 public16k run artifacts after execution.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Run output directory to validate.")
    return parser.parse_args()


def require(condition: bool, message: str, blockers: list[str]) -> None:
    if not condition:
        blockers.append(message)


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir

    summary_path = output_dir / "summary.json"
    metrics_path = output_dir / "metrics.jsonl"
    validation_metrics_path = output_dir / "validation_metrics.jsonl"
    run_config_path = output_dir / "run_config.json"
    run_metadata_path = output_dir / "run_metadata.json"
    validation_summary_path = output_dir / "post_run_artifact_validation_summary.json"
    blockers: list[str] = []

    for required_path in [summary_path, metrics_path, validation_metrics_path, run_config_path, run_metadata_path]:
        require(required_path.exists(), f"missing artifact: {repo_relative_path(required_path)}", blockers)

    summary: dict[str, Any] = {}
    if summary_path.exists():
        summary = load_json(summary_path)

    metrics_rows_actual = count_jsonl_rows(metrics_path)
    validation_rows_actual = count_jsonl_rows(validation_metrics_path)
    max_steps = summary.get("max_steps") if summary else None
    validation_rows_summary = summary.get("validation_rows") if summary else None
    data_loading_mode = summary.get("data_loading_mode") if summary else None
    checkpoint_path_value = summary.get("checkpoint_path") if summary else None
    checkpoint_path = resolve_repo_path(checkpoint_path_value) if isinstance(checkpoint_path_value, str) else None
    checkpoint_path_starts_with_output_dir = bool(checkpoint_path and path_is_under(checkpoint_path, output_dir))

    if summary:
        require(summary.get("success") is True, "summary success must be true", blockers)
        require(isinstance(max_steps, int) and max_steps > 0, "summary max_steps must be a positive integer", blockers)
        if data_loading_mode is not None:
            require(data_loading_mode == "streaming", "summary data_loading_mode must be streaming when present", blockers)
        if isinstance(max_steps, int):
            require(summary.get("metrics_rows") == max_steps, "summary metrics_rows must equal max_steps", blockers)
            require(metrics_rows_actual == max_steps, "metrics.jsonl actual rows must equal max_steps", blockers)
        require(isinstance(validation_rows_summary, int), "summary validation_rows must be an integer", blockers)
        if isinstance(validation_rows_summary, int):
            require(validation_rows_summary >= MIN_VALIDATION_ROWS, "summary validation_rows must be at least 10", blockers)
            require(
                validation_rows_actual == validation_rows_summary,
                "validation_metrics.jsonl actual rows must equal summary validation_rows",
                blockers,
            )
        require(summary.get("loss_all_finite") is True, "loss_all_finite must be true", blockers)
        require(summary.get("val_loss_all_finite") is True, "val_loss_all_finite must be true", blockers)
        require(summary.get("grad_all_finite") is True, "grad_all_finite must be true", blockers)
        require(summary.get("checkpoint_reload_match") is True, "checkpoint_reload_match must be true", blockers)
        require(summary.get("tokenizer_vocab_size") == EXPECTED_TOKENIZER_VOCAB_SIZE, "tokenizer_vocab_size must be 16384", blockers)
        require(summary.get("exact_parameter_count") is not None, "exact_parameter_count must be present", blockers)
        if checkpoint_path is None:
            blockers.append("checkpoint_path must be present")
        else:
            require(checkpoint_path_starts_with_output_dir, "checkpoint_path must start with output_dir", blockers)

    result = {
        "status": "success" if not blockers else "failed",
        "output_dir": repo_relative_path(output_dir),
        "summary_path": repo_relative_path(summary_path),
        "metrics_path": repo_relative_path(metrics_path),
        "validation_metrics_path": repo_relative_path(validation_metrics_path),
        "run_config_path": repo_relative_path(run_config_path),
        "run_metadata_path": repo_relative_path(run_metadata_path),
        "max_steps": max_steps,
        "metrics_rows_summary": summary.get("metrics_rows") if summary else None,
        "metrics_rows_actual": metrics_rows_actual,
        "validation_rows_summary": validation_rows_summary,
        "validation_rows_actual": validation_rows_actual,
        "loss_all_finite": summary.get("loss_all_finite") if summary else None,
        "val_loss_all_finite": summary.get("val_loss_all_finite") if summary else None,
        "grad_all_finite": summary.get("grad_all_finite") if summary else None,
        "checkpoint_reload_match": summary.get("checkpoint_reload_match") if summary else None,
        "checkpoint_path": checkpoint_path_value,
        "checkpoint_path_starts_with_output_dir": checkpoint_path_starts_with_output_dir if summary else None,
        "tokenizer_vocab_size": summary.get("tokenizer_vocab_size") if summary else None,
        "data_loading_mode": data_loading_mode,
        "exact_parameter_count": summary.get("exact_parameter_count") if summary else None,
        "blockers": blockers,
        "blocker_count": len(blockers),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "ready_for_review": not blockers,
    }
    write_json(validation_summary_path, result)

    print(f"status={result['status']}")
    print(f"output_dir={result['output_dir']}")
    print(f"max_steps={result['max_steps']}")
    print(f"metrics_rows_actual={result['metrics_rows_actual']}")
    print(f"validation_rows_actual={result['validation_rows_actual']}")
    print(f"blockers={len(blockers)}")
    print(f"summary_path={repo_relative_path(validation_summary_path)}")
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
