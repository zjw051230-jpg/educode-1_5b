from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = (
    REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile"
    / "results_imported_modal_streaming"
)
ANALYSIS_SUMMARY_PATH = IMPORT_DIR / "mvp28_a_sdpa_profile_analysis_summary.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def round_float(value: Any, digits: int = 6) -> Any:
    if isinstance(value, float):
        return round(value, digits)
    return value


def rounded_mean(values: list[float]) -> float | None:
    if not values:
        return None
    return round(mean(values), 6)


def rounded_min(values: list[float]) -> float | None:
    if not values:
        return None
    return round(min(values), 6)


def rounded_max(values: list[float]) -> float | None:
    if not values:
        return None
    return round(max(values), 6)


def build_interpretation(blockers: list[str], mfu_available: bool) -> str:
    if blockers:
        return "Analysis blockers remain; do not use this artifact as a profiling baseline yet."
    mfu_note = (
        "MFU is available for interpretation."
        if mfu_available
        else "MFU is unavailable because the imported metrics emit null MFU values."
    )
    return (
        "The run is a successful bounded A100 SDPA systems baseline: 50 profiling steps completed, "
        "artifact validation passed, throughput and memory fields are present, and loss values are "
        f"finite sanity signals only. {mfu_note} It is not a model-quality claim and it does not compare "
        "SDPA against naive attention or FlashAttention."
    )


def analyze() -> dict[str, Any]:
    blockers: list[str] = []
    required_files = [
        IMPORT_DIR / "summary.json",
        IMPORT_DIR / "metrics.jsonl",
        IMPORT_DIR / "validation_metrics.jsonl",
        IMPORT_DIR / "run_config.json",
        IMPORT_DIR / "run_metadata.json",
        IMPORT_DIR / "post_run_artifact_validation_summary.json",
    ]
    for path in required_files:
        if not path.exists():
            blockers.append(f"missing required artifact: {path.relative_to(REPO_ROOT).as_posix()}")

    if blockers:
        result = {
            "analysis_status": "failed",
            "blocker_count": len(blockers),
            "blockers": blockers,
        }
        write_analysis(result)
        return result

    summary = load_json(IMPORT_DIR / "summary.json")
    metrics = load_jsonl(IMPORT_DIR / "metrics.jsonl")
    validation_metrics = load_jsonl(IMPORT_DIR / "validation_metrics.jsonl")
    run_config = load_json(IMPORT_DIR / "run_config.json")
    post_run = load_json(IMPORT_DIR / "post_run_artifact_validation_summary.json")

    profiling_config = run_config.get("profiling", {}) if isinstance(run_config.get("profiling"), dict) else {}
    declared_features = (
        summary.get("declared_model_features", {})
        if isinstance(summary.get("declared_model_features"), dict)
        else {}
    )
    attention_backend = profiling_config.get("attention_backend") or declared_features.get("attention_backend")
    final_validation_loss = summary.get("final_val_loss", summary.get("final_validation_loss"))

    tokens_per_sec_values = [
        float(row["tokens_per_sec"]) for row in metrics if finite_number(row.get("tokens_per_sec"))
    ]
    step_time_values = [float(row["elapsed_seconds"]) for row in metrics if finite_number(row.get("elapsed_seconds"))]
    allocated_memory_values = [
        float(row["gpu_memory_allocated_gib"])
        for row in metrics
        if finite_number(row.get("gpu_memory_allocated_gib"))
    ]
    reserved_memory_values = [
        float(row["gpu_memory_reserved_gib"])
        for row in metrics
        if finite_number(row.get("gpu_memory_reserved_gib"))
    ]
    mfu_values = [float(row["mfu"]) for row in metrics if finite_number(row.get("mfu"))]

    if summary.get("success") is not True:
        blockers.append(f"summary.success expected true, got {summary.get('success')!r}")
    if post_run.get("blocker_count") != 0:
        blockers.append(f"post-run blocker_count expected 0, got {post_run.get('blocker_count')!r}")
    if post_run.get("artifact_validation_gate_type") != "bounded_sdpa_profile":
        blockers.append("post-run artifact validation did not use bounded_sdpa_profile gate")
    if attention_backend != "sdpa":
        blockers.append(f"attention_backend expected sdpa, got {attention_backend!r}")
    if summary.get("max_steps") != 50:
        blockers.append(f"max_steps expected 50, got {summary.get('max_steps')!r}")
    if len(metrics) != 50:
        blockers.append(f"metrics_rows expected 50, got {len(metrics)}")
    if len(validation_metrics) != 1:
        blockers.append(f"validation_rows expected 1, got {len(validation_metrics)}")
    if not tokens_per_sec_values:
        blockers.append("metrics.jsonl has no finite tokens_per_sec values")
    if not step_time_values:
        blockers.append("metrics.jsonl has no finite elapsed_seconds values")
    if not allocated_memory_values:
        blockers.append("metrics.jsonl has no finite gpu_memory_allocated_gib values")
    if not reserved_memory_values:
        blockers.append("metrics.jsonl has no finite gpu_memory_reserved_gib values")
    if not finite_number(summary.get("final_train_loss")):
        blockers.append(f"final_train_loss is not finite: {summary.get('final_train_loss')!r}")
    if not finite_number(final_validation_loss):
        blockers.append(f"final_validation_loss is not finite: {final_validation_loss!r}")

    mfu_available = bool(mfu_values)
    result = {
        "analysis_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "attention_backend": attention_backend,
        "max_steps": summary.get("max_steps"),
        "metrics_rows": len(metrics),
        "validation_rows": len(validation_metrics),
        "final_train_loss": summary.get("final_train_loss"),
        "final_validation_loss": round_float(final_validation_loss),
        "summary_tokens_per_sec": round_float(summary.get("approximate_tokens_per_sec")),
        "mean_step_tokens_per_sec": rounded_mean(tokens_per_sec_values),
        "min_step_tokens_per_sec": rounded_min(tokens_per_sec_values),
        "max_step_tokens_per_sec": rounded_max(tokens_per_sec_values),
        "average_step_time_seconds": rounded_mean(step_time_values),
        "min_step_time_seconds": rounded_min(step_time_values),
        "max_step_time_seconds": rounded_max(step_time_values),
        "peak_allocated_memory_gib": rounded_max(allocated_memory_values),
        "peak_reserved_memory_gib": rounded_max(reserved_memory_values),
        "mfu_available": mfu_available,
        "mfu_value": rounded_mean(mfu_values) if mfu_available else None,
        "profiling_result_interpretation": build_interpretation(blockers, mfu_available),
        "recommended_next_mvp": "MVP-29.P context length 512-to-1024 memory/preflight plan",
    }
    write_analysis(result)
    return result


def write_analysis(result: dict[str, Any]) -> None:
    ANALYSIS_SUMMARY_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    result = analyze()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["analysis_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
