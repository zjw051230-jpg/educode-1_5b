from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "experiments" / "a100" / "fineweb_edu_500mb_300m_1000step_public16k_execute"
EXPECTED_TOKENIZER_VOCAB_SIZE = 16384
MIN_VALIDATION_ROWS = 10
SUPPORTED_MAX_STEPS = {1000, 3000, 5000}
BOUNDED_PROFILE_MODE = "bounded_sdpa_profile"
BOUNDED_PROFILE_MAX_STEPS = 50
BOUNDED_PROFILE_ATTENTION_BACKEND = "sdpa"
BOUNDED_MEMORY_PREFLIGHT_MODE = "bounded_seq1024_sdpa_memory_preflight"
BOUNDED_MEMORY_PREFLIGHT_MAX_STEPS = 10
BOUNDED_MEMORY_PREFLIGHT_CONTEXT_LENGTH = 1024
BOUNDED_MEMORY_PREFLIGHT_BATCH_SIZE = 4
BOUNDED_MEMORY_PREFLIGHT_ATTENTION_BACKEND = "sdpa"


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


def load_jsonl_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            if isinstance(payload, dict):
                rows.append(payload)
    return rows


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


def warn_unless(condition: bool, message: str, caveats: list[str]) -> None:
    if not condition:
        caveats.append(message)


def is_finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def is_bounded_profile_config(run_config: dict[str, Any], summary: dict[str, Any]) -> bool:
    profiling_config = run_config.get("profiling")
    if not isinstance(profiling_config, dict):
        return False
    run_name = str(summary.get("run_name") or run_config.get("run", {}).get("run_name", ""))
    return (
        str(profiling_config.get("profile_mode", "")).strip().lower() == BOUNDED_PROFILE_MODE
        and profiling_config.get("enabled") is True
        and str(profiling_config.get("attention_backend", "")).strip().lower() == BOUNDED_PROFILE_ATTENTION_BACKEND
        and run_name.endswith("_sdpa_profile")
    )


def is_bounded_memory_preflight_config(run_config: dict[str, Any], summary: dict[str, Any]) -> bool:
    profiling_config = run_config.get("profiling")
    if not isinstance(profiling_config, dict):
        return False
    run_name = str(summary.get("run_name") or run_config.get("run", {}).get("run_name", ""))
    return (
        str(profiling_config.get("profile_mode", "")).strip().lower() == BOUNDED_MEMORY_PREFLIGHT_MODE
        and profiling_config.get("enabled") is True
        and str(profiling_config.get("attention_backend", "")).strip().lower()
        == BOUNDED_MEMORY_PREFLIGHT_ATTENTION_BACKEND
        and run_name.endswith("_seq1024_sdpa_memory_preflight")
    )


def expected_validation_rows_for_config(run_config: dict[str, Any], max_steps: int) -> int | None:
    training_config = run_config.get("training", {}) if isinstance(run_config.get("training"), dict) else {}
    eval_interval = training_config.get("eval_interval")
    if not isinstance(eval_interval, int) or eval_interval <= 0:
        return None
    return max_steps // eval_interval


def validate_training_execution_artifact(
    summary: dict[str, Any],
    metrics_rows_actual: int,
    validation_rows_actual: int,
    validation_rows_summary: Any,
    max_steps: Any,
    blockers: list[str],
) -> None:
    require(isinstance(max_steps, int) and max_steps in SUPPORTED_MAX_STEPS, "summary max_steps must be one of: 1000, 3000, 5000", blockers)
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
    require(summary.get("checkpoint_reload_match") is True, "checkpoint_reload_match must be true", blockers)


def validate_bounded_profile_artifact(
    summary: dict[str, Any],
    run_config: dict[str, Any],
    metrics_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    metrics_rows_actual: int,
    validation_rows_actual: int,
    validation_rows_summary: Any,
    max_steps: Any,
    blockers: list[str],
    caveats: list[str],
) -> None:
    profiling_config = run_config.get("profiling", {}) if isinstance(run_config.get("profiling"), dict) else {}
    expected_validation_rows = expected_validation_rows_for_config(run_config, int(max_steps)) if isinstance(max_steps, int) else None

    require(max_steps == BOUNDED_PROFILE_MAX_STEPS, "bounded profile summary max_steps must be 50", blockers)
    require(summary.get("metrics_rows") == BOUNDED_PROFILE_MAX_STEPS, "bounded profile summary metrics_rows must equal 50", blockers)
    require(metrics_rows_actual == BOUNDED_PROFILE_MAX_STEPS, "bounded profile metrics.jsonl actual rows must equal 50", blockers)
    require(isinstance(validation_rows_summary, int), "bounded profile summary validation_rows must be an integer", blockers)
    if isinstance(validation_rows_summary, int):
        require(validation_rows_summary >= 1, "bounded profile validation_rows must be at least 1", blockers)
        require(validation_rows_actual == validation_rows_summary, "bounded profile validation rows actual must match summary", blockers)
    if expected_validation_rows is not None:
        require(
            validation_rows_actual == expected_validation_rows,
            f"bounded profile validation rows must equal config-derived expected rows {expected_validation_rows}",
            blockers,
        )

    require(profiling_config.get("profile_mode") == BOUNDED_PROFILE_MODE, "bounded profile run_config profiling.profile_mode mismatch", blockers)
    require(profiling_config.get("attention_backend") == BOUNDED_PROFILE_ATTENTION_BACKEND, "bounded profile attention_backend must be sdpa", blockers)
    require(profiling_config.get("record_tokens_per_sec") is True, "bounded profile must enable record_tokens_per_sec", blockers)
    require(profiling_config.get("record_memory") is True, "bounded profile must enable record_memory", blockers)
    require(profiling_config.get("record_mfu") is True, "bounded profile must enable record_mfu", blockers)
    require(max_steps != 10000, "bounded profile must not be a 10000-step run", blockers)

    require(is_finite_number(summary.get("final_train_loss")), "bounded profile final_train_loss must be finite", blockers)
    final_val_loss = summary.get("final_val_loss", summary.get("final_validation_loss"))
    if final_val_loss is not None:
        require(is_finite_number(final_val_loss), "bounded profile final validation loss must be finite when present", blockers)

    warn_unless(any("tokens_per_sec" in row for row in metrics_rows), "bounded profile metrics do not include tokens_per_sec rows", caveats)
    warn_unless(
        any("gpu_memory_allocated_gib" in row or "gpu_memory_reserved_gib" in row for row in metrics_rows),
        "bounded profile metrics do not include GPU memory rows",
        caveats,
    )
    warn_unless(any("mfu" in row for row in metrics_rows), "bounded profile metrics do not include MFU rows", caveats)
    warn_unless(bool(validation_rows), "bounded profile validation metrics are empty", caveats)


def validate_bounded_memory_preflight_artifact(
    summary: dict[str, Any],
    run_config: dict[str, Any],
    metrics_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    metrics_rows_actual: int,
    validation_rows_actual: int,
    validation_rows_summary: Any,
    max_steps: Any,
    blockers: list[str],
    caveats: list[str],
) -> None:
    profiling_config = run_config.get("profiling", {}) if isinstance(run_config.get("profiling"), dict) else {}
    training_config = run_config.get("training", {}) if isinstance(run_config.get("training"), dict) else {}
    model_config = run_config.get("model", {}) if isinstance(run_config.get("model"), dict) else {}
    data_config = run_config.get("data", {}) if isinstance(run_config.get("data"), dict) else {}
    expected_validation_rows = expected_validation_rows_for_config(run_config, int(max_steps)) if isinstance(max_steps, int) else None

    require(max_steps == BOUNDED_MEMORY_PREFLIGHT_MAX_STEPS, "bounded seq1024 memory preflight summary max_steps must be 10", blockers)
    require(summary.get("metrics_rows") == BOUNDED_MEMORY_PREFLIGHT_MAX_STEPS, "bounded seq1024 memory preflight summary metrics_rows must equal 10", blockers)
    require(metrics_rows_actual == BOUNDED_MEMORY_PREFLIGHT_MAX_STEPS, "bounded seq1024 memory preflight metrics.jsonl actual rows must equal 10", blockers)
    require(isinstance(validation_rows_summary, int), "bounded seq1024 memory preflight summary validation_rows must be an integer", blockers)
    if isinstance(validation_rows_summary, int):
        require(validation_rows_summary >= 1, "bounded seq1024 memory preflight validation_rows must be at least 1", blockers)
        require(validation_rows_actual == validation_rows_summary, "bounded seq1024 memory preflight validation rows actual must match summary", blockers)
    if expected_validation_rows is not None:
        require(
            validation_rows_actual == expected_validation_rows,
            f"bounded seq1024 memory preflight validation rows must equal config-derived expected rows {expected_validation_rows}",
            blockers,
        )

    require(profiling_config.get("profile_mode") == BOUNDED_MEMORY_PREFLIGHT_MODE, "bounded seq1024 memory preflight run_config profiling.profile_mode mismatch", blockers)
    require(profiling_config.get("attention_backend") == BOUNDED_MEMORY_PREFLIGHT_ATTENTION_BACKEND, "bounded seq1024 memory preflight attention_backend must be sdpa", blockers)
    require(profiling_config.get("record_tokens_per_sec") is True, "bounded seq1024 memory preflight must enable record_tokens_per_sec", blockers)
    require(profiling_config.get("record_memory") is True, "bounded seq1024 memory preflight must enable record_memory", blockers)
    require(profiling_config.get("record_mfu") is True, "bounded seq1024 memory preflight must enable record_mfu", blockers)
    require(model_config.get("context_length") == BOUNDED_MEMORY_PREFLIGHT_CONTEXT_LENGTH, "bounded seq1024 memory preflight model.context_length must be 1024", blockers)
    require(data_config.get("sequence_length") == BOUNDED_MEMORY_PREFLIGHT_CONTEXT_LENGTH, "bounded seq1024 memory preflight data.sequence_length must be 1024", blockers)
    require(training_config.get("sequence_length") == BOUNDED_MEMORY_PREFLIGHT_CONTEXT_LENGTH, "bounded seq1024 memory preflight training.sequence_length must be 1024", blockers)
    require(training_config.get("batch_size") == BOUNDED_MEMORY_PREFLIGHT_BATCH_SIZE, "bounded seq1024 memory preflight batch_size must be 4", blockers)
    require(max_steps != 10000, "bounded seq1024 memory preflight must not be a 10000-step run", blockers)

    require(is_finite_number(summary.get("final_train_loss")), "bounded seq1024 memory preflight final_train_loss must be finite", blockers)
    final_val_loss = summary.get("final_val_loss", summary.get("final_validation_loss"))
    if final_val_loss is not None:
        require(is_finite_number(final_val_loss), "bounded seq1024 memory preflight final validation loss must be finite when present", blockers)

    warn_unless(any("tokens_per_sec" in row for row in metrics_rows), "bounded seq1024 memory preflight metrics do not include tokens_per_sec rows", caveats)
    warn_unless(
        any("gpu_memory_allocated_gib" in row or "gpu_memory_reserved_gib" in row for row in metrics_rows),
        "bounded seq1024 memory preflight metrics do not include GPU memory rows",
        caveats,
    )
    warn_unless(any("mfu" in row for row in metrics_rows), "bounded seq1024 memory preflight metrics do not include MFU rows", caveats)
    warn_unless(bool(validation_rows), "bounded seq1024 memory preflight validation metrics are empty", caveats)


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
    caveats: list[str] = []

    for required_path in [summary_path, metrics_path, validation_metrics_path, run_config_path, run_metadata_path]:
        require(required_path.exists(), f"missing artifact: {repo_relative_path(required_path)}", blockers)

    summary: dict[str, Any] = {}
    if summary_path.exists():
        summary = load_json(summary_path)
    run_config: dict[str, Any] = {}
    if run_config_path.exists():
        run_config = load_json(run_config_path)

    metrics_rows_actual = count_jsonl_rows(metrics_path)
    validation_rows_actual = count_jsonl_rows(validation_metrics_path)
    metrics_rows = load_jsonl_rows(metrics_path)
    validation_rows = load_jsonl_rows(validation_metrics_path)
    max_steps = summary.get("max_steps") if summary else None
    validation_rows_summary = summary.get("validation_rows") if summary else None
    data_loading_mode = summary.get("data_loading_mode") if summary else None
    checkpoint_path_value = summary.get("checkpoint_path") if summary else None
    checkpoint_path = resolve_repo_path(checkpoint_path_value) if isinstance(checkpoint_path_value, str) else None
    checkpoint_path_starts_with_output_dir = bool(checkpoint_path and path_is_under(checkpoint_path, output_dir))
    if summary and run_config and is_bounded_profile_config(run_config, summary):
        artifact_validation_gate_type = "bounded_sdpa_profile"
    elif summary and run_config and is_bounded_memory_preflight_config(run_config, summary):
        artifact_validation_gate_type = "bounded_seq1024_sdpa_memory_preflight"
    else:
        artifact_validation_gate_type = "training_execution"

    if summary:
        require(summary.get("success") is True, "summary success must be true", blockers)
        if data_loading_mode is not None:
            require(data_loading_mode == "streaming", "summary data_loading_mode must be streaming when present", blockers)
        require(summary.get("loss_all_finite") is True, "loss_all_finite must be true", blockers)
        require(summary.get("val_loss_all_finite") is True, "val_loss_all_finite must be true", blockers)
        require(summary.get("grad_all_finite") is True, "grad_all_finite must be true", blockers)
        require(summary.get("tokenizer_vocab_size") == EXPECTED_TOKENIZER_VOCAB_SIZE, "tokenizer_vocab_size must be 16384", blockers)
        require(summary.get("exact_parameter_count") is not None, "exact_parameter_count must be present", blockers)
        if artifact_validation_gate_type == "bounded_sdpa_profile":
            validate_bounded_profile_artifact(
                summary=summary,
                run_config=run_config,
                metrics_rows=metrics_rows,
                validation_rows=validation_rows,
                metrics_rows_actual=metrics_rows_actual,
                validation_rows_actual=validation_rows_actual,
                validation_rows_summary=validation_rows_summary,
                max_steps=max_steps,
                blockers=blockers,
                caveats=caveats,
            )
        elif artifact_validation_gate_type == "bounded_seq1024_sdpa_memory_preflight":
            validate_bounded_memory_preflight_artifact(
                summary=summary,
                run_config=run_config,
                metrics_rows=metrics_rows,
                validation_rows=validation_rows,
                metrics_rows_actual=metrics_rows_actual,
                validation_rows_actual=validation_rows_actual,
                validation_rows_summary=validation_rows_summary,
                max_steps=max_steps,
                blockers=blockers,
                caveats=caveats,
            )
        else:
            validate_training_execution_artifact(
                summary=summary,
                metrics_rows_actual=metrics_rows_actual,
                validation_rows_actual=validation_rows_actual,
                validation_rows_summary=validation_rows_summary,
                max_steps=max_steps,
                blockers=blockers,
            )
        if checkpoint_path is None:
            if artifact_validation_gate_type == "bounded_sdpa_profile":
                caveats.append("checkpoint_path is absent for bounded profile artifact")
            else:
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
        "artifact_validation_gate_type": artifact_validation_gate_type,
        "metrics_rows_summary": summary.get("metrics_rows") if summary else None,
        "metrics_rows_actual": metrics_rows_actual,
        "validation_rows_summary": validation_rows_summary,
        "validation_rows_actual": validation_rows_actual,
        "expected_validation_rows": expected_validation_rows_for_config(run_config, max_steps)
        if run_config and isinstance(max_steps, int)
        else None,
        "loss_all_finite": summary.get("loss_all_finite") if summary else None,
        "val_loss_all_finite": summary.get("val_loss_all_finite") if summary else None,
        "grad_all_finite": summary.get("grad_all_finite") if summary else None,
        "checkpoint_reload_match": summary.get("checkpoint_reload_match") if summary else None,
        "checkpoint_path": checkpoint_path_value,
        "checkpoint_path_starts_with_output_dir": checkpoint_path_starts_with_output_dir if summary else None,
        "tokenizer_vocab_size": summary.get("tokenizer_vocab_size") if summary else None,
        "data_loading_mode": data_loading_mode,
        "exact_parameter_count": summary.get("exact_parameter_count") if summary else None,
        "attention_backend": run_config.get("profiling", {}).get("attention_backend") if isinstance(run_config.get("profiling"), dict) else None,
        "profiling_record_tokens_per_sec": run_config.get("profiling", {}).get("record_tokens_per_sec")
        if isinstance(run_config.get("profiling"), dict)
        else None,
        "profiling_record_memory": run_config.get("profiling", {}).get("record_memory")
        if isinstance(run_config.get("profiling"), dict)
        else None,
        "profiling_record_mfu": run_config.get("profiling", {}).get("record_mfu")
        if isinstance(run_config.get("profiling"), dict)
        else None,
        "blockers": blockers,
        "blocker_count": len(blockers),
        "caveats": caveats,
        "caveat_count": len(caveats),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "ready_for_review": not blockers,
    }
    write_json(validation_summary_path, result)

    print(f"status={result['status']}")
    print(f"output_dir={result['output_dir']}")
    print(f"max_steps={result['max_steps']}")
    print(f"artifact_validation_gate_type={result['artifact_validation_gate_type']}")
    print(f"metrics_rows_actual={result['metrics_rows_actual']}")
    print(f"validation_rows_actual={result['validation_rows_actual']}")
    print(f"caveats={len(caveats)}")
    print(f"blockers={len(blockers)}")
    print(f"summary_path={repo_relative_path(validation_summary_path)}")
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
