from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMPORT_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_500mb_300m_1000step_public16k_execute"
    / "results_imported_streaming"
)
EXPECTED_PARAMETER_COUNT = 336106496
EXPECTED_TOKENIZER_VOCAB_SIZE = 16384
EXPECTED_MAX_STEPS = 1000
EXPECTED_BATCH_SIZE = 8
EXPECTED_GRADIENT_ACCUMULATION_STEPS = 4
EXPECTED_METRICS_ROWS = 1000
EXPECTED_VALIDATION_ROWS = 10


def repo_relative_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def count_jsonl_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def add_blocker(blockers: list[str], condition: bool, message: str) -> None:
    if not condition:
        blockers.append(message)


def main() -> int:
    summary_path = IMPORT_DIR / "summary.json"
    metrics_path = IMPORT_DIR / "metrics.jsonl"
    validation_metrics_path = IMPORT_DIR / "validation_metrics.jsonl"
    post_run_validation_path = IMPORT_DIR / "post_run_artifact_validation_summary.json"
    validation_summary_path = IMPORT_DIR / "import_validation_summary.json"

    required_paths = [
        summary_path,
        IMPORT_DIR / "summary.md",
        metrics_path,
        validation_metrics_path,
        IMPORT_DIR / "run_config.json",
        IMPORT_DIR / "run_metadata.json",
        post_run_validation_path,
    ]
    blockers: list[str] = []
    for path in required_paths:
        add_blocker(blockers, path.exists(), f"missing required artifact: {repo_relative_path(path)}")

    summary: dict[str, Any] = {}
    post_run_validation: dict[str, Any] = {}
    metrics_rows_actual: int | None = None
    validation_rows_actual: int | None = None

    if summary_path.exists():
        summary = load_json(summary_path)
    if post_run_validation_path.exists():
        post_run_validation = load_json(post_run_validation_path)
    if metrics_path.exists():
        metrics_rows_actual = count_jsonl_rows(metrics_path)
    if validation_metrics_path.exists():
        validation_rows_actual = count_jsonl_rows(validation_metrics_path)

    if summary:
        checks = {
            "success": summary.get("success") is True,
            "runtime_device": summary.get("runtime_device") == "cuda",
            "runtime_dtype": summary.get("runtime_dtype") == "bf16",
            "exact_parameter_count": summary.get("exact_parameter_count") == EXPECTED_PARAMETER_COUNT,
            "max_steps": summary.get("max_steps") == EXPECTED_MAX_STEPS,
            "batch_size": summary.get("batch_size") == EXPECTED_BATCH_SIZE,
            "gradient_accumulation_steps": summary.get("gradient_accumulation_steps")
            == EXPECTED_GRADIENT_ACCUMULATION_STEPS,
            "data_loading_mode": summary.get("data_loading_mode") == "streaming",
            "host_ram_efficient_batching": summary.get("host_ram_efficient_batching") is True,
            "batch_precompute_disabled": summary.get("batch_precompute_disabled") is True,
            "tokenizer_vocab_size": summary.get("tokenizer_vocab_size") == EXPECTED_TOKENIZER_VOCAB_SIZE,
            "metrics_rows": summary.get("metrics_rows") == EXPECTED_METRICS_ROWS,
            "validation_rows": summary.get("validation_rows") == EXPECTED_VALIDATION_ROWS,
            "loss_all_finite": summary.get("loss_all_finite") is True,
            "val_loss_all_finite": summary.get("val_loss_all_finite") is True,
            "grad_all_finite": summary.get("grad_all_finite") is True,
            "checkpoint_reload_match": summary.get("checkpoint_reload_match") is True,
            "checkpoint_path_starts_with_output_dir": summary.get("checkpoint_path_starts_with_output_dir") is True,
        }
        for field_name, passed in checks.items():
            add_blocker(blockers, passed, f"summary check failed: {field_name}")

    add_blocker(blockers, metrics_rows_actual == EXPECTED_METRICS_ROWS, "metrics.jsonl actual row count != 1000")
    add_blocker(
        blockers,
        validation_rows_actual == EXPECTED_VALIDATION_ROWS,
        "validation_metrics.jsonl actual row count != 10",
    )

    summary_post_run_validation = summary.get("post_run_artifact_validation") if isinstance(summary, dict) else None
    summary_post_run_passed = (
        isinstance(summary_post_run_validation, dict) and summary_post_run_validation.get("passed") is True
    )
    standalone_post_run_passed = post_run_validation.get("passed") is True or (
        post_run_validation.get("status") == "success"
        and post_run_validation.get("blocker_count") == 0
        and post_run_validation.get("ready_for_review") is True
    )
    add_blocker(blockers, summary_post_run_passed, "summary.post_run_artifact_validation.passed is not true")
    if post_run_validation:
        add_blocker(blockers, standalone_post_run_passed, "standalone post-run artifact validation did not pass")

    validation_summary = {
        "validation_status": "passed" if not blockers else "failed",
        "blockers": blockers,
        "blocker_count": len(blockers),
        "import_dir": repo_relative_path(IMPORT_DIR),
        "summary_path": repo_relative_path(summary_path),
        "metrics_path": repo_relative_path(metrics_path),
        "validation_metrics_path": repo_relative_path(validation_metrics_path),
        "post_run_artifact_validation_path": repo_relative_path(post_run_validation_path),
        "run_id": summary.get("run_id"),
        "run_name": summary.get("run_name"),
        "runtime_device": summary.get("runtime_device"),
        "runtime_dtype": summary.get("runtime_dtype"),
        "exact_parameter_count": summary.get("exact_parameter_count"),
        "max_steps": summary.get("max_steps"),
        "batch_size": summary.get("batch_size"),
        "gradient_accumulation_steps": summary.get("gradient_accumulation_steps"),
        "sequence_length": summary.get("sequence_length"),
        "data_loading_mode": summary.get("data_loading_mode"),
        "host_ram_efficient_batching": summary.get("host_ram_efficient_batching"),
        "batch_precompute_disabled": summary.get("batch_precompute_disabled"),
        "tokenizer_vocab_size": summary.get("tokenizer_vocab_size"),
        "first_train_loss": summary.get("first_train_loss"),
        "final_train_loss": summary.get("final_train_loss"),
        "final_val_loss": summary.get("final_val_loss"),
        "metrics_rows_summary": summary.get("metrics_rows"),
        "validation_rows_summary": summary.get("validation_rows"),
        "metrics_rows_actual": metrics_rows_actual,
        "validation_rows_actual": validation_rows_actual,
        "tokens_seen": summary.get("tokens_seen"),
        "elapsed_seconds": summary.get("elapsed_seconds"),
        "approximate_tokens_per_sec": summary.get("approximate_tokens_per_sec"),
        "checkpoint_reload_match": summary.get("checkpoint_reload_match"),
        "checkpoint_path_starts_with_output_dir": summary.get("checkpoint_path_starts_with_output_dir"),
        "summary_post_run_artifact_validation_passed": summary_post_run_passed,
        "standalone_post_run_artifact_validation_passed": standalone_post_run_passed,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    validation_summary_path.write_text(
        json.dumps(validation_summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"validation_status={validation_summary['validation_status']}")
    print(f"blockers={len(blockers)}")
    print(f"run_id={validation_summary['run_id']}")
    print(f"data_loading_mode={validation_summary['data_loading_mode']}")
    print(f"batch_size={validation_summary['batch_size']}")
    print(f"gradient_accumulation_steps={validation_summary['gradient_accumulation_steps']}")
    print(f"metrics_rows_actual={metrics_rows_actual}")
    print(f"validation_rows_actual={validation_rows_actual}")
    print(f"summary_path={repo_relative_path(validation_summary_path)}")
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
