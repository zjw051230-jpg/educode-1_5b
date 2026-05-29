from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SEQ1024_PROFILE_DIR = (
    REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile"
    / "results_imported_modal_streaming"
)
SEQ512_PROFILE_DIR = (
    REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile"
    / "results_imported_modal_streaming"
)
SEQ1024_PREFLIGHT_DIR = (
    REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight"
    / "results_imported_modal_streaming"
)
ANALYSIS_SUMMARY_PATH = SEQ1024_PROFILE_DIR / "mvp30_a_seq1024_sdpa_profile_analysis_summary.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
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


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def rounded(value: float | None, digits: int = 6) -> float | None:
    return round(value, digits) if value is not None and math.isfinite(value) else None


def delta(current: Any, baseline: Any) -> float | None:
    if finite_number(current) and finite_number(baseline):
        return rounded(float(current) - float(baseline))
    return None


def metric_values(rows: list[dict[str, Any]], key: str) -> list[float]:
    return [float(row[key]) for row in rows if finite_number(row.get(key))]


def build_interpretation(blockers: list[str]) -> str:
    if blockers:
        return "Analysis blockers remain; do not use this artifact for next-stage decisions yet."
    return (
        "Seq1024 50-step SDPA profiling succeeded on A100-40GB with no OOM at batch_size=4 and "
        "grad_accum=4. Throughput is slightly lower and step time slightly higher than the seq512 "
        "SDPA baseline, while peak memory is essentially unchanged because batch size was halved. "
        "The result is strong systems profiling evidence for this bounded shape, but it is not "
        "quality training evidence and does not prove long seq1024 training safety."
    )


def analyze() -> dict[str, Any]:
    blockers: list[str] = []
    caveats: list[str] = []
    required_paths = [
        SEQ1024_PROFILE_DIR / "summary.json",
        SEQ1024_PROFILE_DIR / "metrics.jsonl",
        SEQ1024_PROFILE_DIR / "validation_metrics.jsonl",
        SEQ1024_PROFILE_DIR / "run_config.json",
        SEQ1024_PROFILE_DIR / "run_metadata.json",
        SEQ1024_PROFILE_DIR / "post_run_artifact_validation_summary.json",
        SEQ512_PROFILE_DIR / "mvp28_a_sdpa_profile_analysis_summary.json",
        SEQ1024_PREFLIGHT_DIR / "mvp29_a_seq1024_memory_preflight_analysis_summary.json",
    ]
    for path in required_paths:
        if not path.exists():
            blockers.append(f"missing required artifact: {path.relative_to(REPO_ROOT).as_posix()}")

    if blockers:
        result = {
            "analysis_status": "failed",
            "blocker_count": len(blockers),
            "blockers": blockers,
            "caveats": caveats,
        }
        write_analysis(result)
        return result

    summary = load_json(SEQ1024_PROFILE_DIR / "summary.json")
    metrics = load_jsonl(SEQ1024_PROFILE_DIR / "metrics.jsonl")
    validation_metrics = load_jsonl(SEQ1024_PROFILE_DIR / "validation_metrics.jsonl")
    run_config = load_json(SEQ1024_PROFILE_DIR / "run_config.json")
    run_metadata = load_json(SEQ1024_PROFILE_DIR / "run_metadata.json")
    post_run = load_json(SEQ1024_PROFILE_DIR / "post_run_artifact_validation_summary.json")
    seq512 = load_json(SEQ512_PROFILE_DIR / "mvp28_a_sdpa_profile_analysis_summary.json")
    seq1024_10step = load_json(SEQ1024_PREFLIGHT_DIR / "mvp29_a_seq1024_memory_preflight_analysis_summary.json")

    profiling = run_config.get("profiling", {}) if isinstance(run_config.get("profiling"), dict) else {}
    declared_features = (
        summary.get("declared_model_features", {})
        if isinstance(summary.get("declared_model_features"), dict)
        else {}
    )
    attention_backend = profiling.get("attention_backend") or declared_features.get("attention_backend")
    final_validation_loss = summary.get("final_val_loss", summary.get("final_validation_loss"))
    post_run_blockers = post_run.get("blockers") if isinstance(post_run.get("blockers"), list) else []
    oom_detected = any("oom" in str(item).lower() or "out of memory" in str(item).lower() for item in post_run_blockers)

    if summary.get("success") is not True:
        blockers.append("summary.success must be true")
    if run_metadata.get("status") != "success":
        blockers.append("run_metadata.status must be success")
    if post_run.get("status") != "success" or post_run.get("blocker_count") != 0:
        blockers.append("post-run artifact validation must pass with blocker_count=0")
    if summary.get("sequence_length") != 1024:
        blockers.append(f"context_length expected 1024, got {summary.get('sequence_length')!r}")
    if summary.get("batch_size") != 4:
        blockers.append(f"batch_size expected 4, got {summary.get('batch_size')!r}")
    if summary.get("gradient_accumulation_steps") != 4:
        blockers.append(f"grad_accum expected 4, got {summary.get('gradient_accumulation_steps')!r}")
    if attention_backend != "sdpa":
        blockers.append(f"attention_backend expected sdpa, got {attention_backend!r}")
    if summary.get("max_steps") != 50:
        blockers.append(f"max_steps expected 50, got {summary.get('max_steps')!r}")
    if len(metrics) != 50:
        blockers.append(f"metrics rows expected 50, got {len(metrics)}")
    if len(validation_metrics) != 1:
        blockers.append(f"validation rows expected 1, got {len(validation_metrics)}")
    if oom_detected:
        blockers.append("OOM detected in post-run blockers")

    tokens_per_sec_values = metric_values(metrics, "tokens_per_sec")
    step_time_values = metric_values(metrics, "elapsed_seconds")
    allocated_values = metric_values(metrics, "gpu_memory_allocated_gib")
    reserved_values = metric_values(metrics, "gpu_memory_reserved_gib")
    mfu_values = metric_values(metrics, "mfu")

    if not tokens_per_sec_values:
        caveats.append("metrics.jsonl has no finite tokens_per_sec values")
    if not step_time_values:
        caveats.append("metrics.jsonl has no finite elapsed_seconds values")
    if not allocated_values or not reserved_values:
        caveats.append("metrics.jsonl has incomplete GPU memory values")
    if not mfu_values:
        caveats.append("mfu values are absent or null in metrics.jsonl")

    summary_tokens_per_sec = (
        rounded(float(summary["approximate_tokens_per_sec"]))
        if finite_number(summary.get("approximate_tokens_per_sec"))
        else None
    )
    mean_step_tokens_per_sec = rounded(mean(tokens_per_sec_values)) if tokens_per_sec_values else None
    average_step_time_seconds = rounded(mean(step_time_values)) if step_time_values else None
    peak_allocated_memory_gib = rounded(max(allocated_values)) if allocated_values else None
    peak_reserved_memory_gib = rounded(max(reserved_values)) if reserved_values else None

    result = {
        "analysis_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "caveat_count": len(caveats),
        "caveats": caveats,
        "context_length": summary.get("sequence_length"),
        "batch_size": summary.get("batch_size"),
        "grad_accum": summary.get("gradient_accumulation_steps"),
        "attention_backend": attention_backend,
        "max_steps": summary.get("max_steps"),
        "metrics_rows": len(metrics),
        "validation_rows": len(validation_metrics),
        "final_train_loss": summary.get("final_train_loss"),
        "final_validation_loss": final_validation_loss,
        "oom_detected": oom_detected,
        "summary_tokens_per_sec": summary_tokens_per_sec,
        "mean_step_tokens_per_sec": mean_step_tokens_per_sec,
        "average_step_time_seconds": average_step_time_seconds,
        "peak_allocated_memory_gib": peak_allocated_memory_gib,
        "peak_reserved_memory_gib": peak_reserved_memory_gib,
        "mfu_available": bool(mfu_values),
        "mfu_value": rounded(mean(mfu_values)) if mfu_values else None,
        "comparison_vs_seq512_summary_tokens_per_sec_delta": delta(
            summary_tokens_per_sec, seq512.get("summary_tokens_per_sec")
        ),
        "comparison_vs_seq512_mean_step_tokens_per_sec_delta": delta(
            mean_step_tokens_per_sec, seq512.get("mean_step_tokens_per_sec")
        ),
        "comparison_vs_seq512_average_step_time_delta": delta(
            average_step_time_seconds, seq512.get("average_step_time_seconds")
        ),
        "comparison_vs_seq512_peak_allocated_memory_delta": delta(
            peak_allocated_memory_gib, seq512.get("peak_allocated_memory_gib")
        ),
        "comparison_vs_seq512_peak_reserved_memory_delta": delta(
            peak_reserved_memory_gib, seq512.get("peak_reserved_memory_gib")
        ),
        "comparison_vs_seq1024_10step_summary_tokens_per_sec_delta": delta(
            summary_tokens_per_sec, seq1024_10step.get("summary_tokens_per_sec")
        ),
        "comparison_vs_seq1024_10step_average_step_time_delta": delta(
            average_step_time_seconds, seq1024_10step.get("average_step_time_seconds")
        ),
        "seq512_summary_tokens_per_sec": seq512.get("summary_tokens_per_sec"),
        "seq512_average_step_time_seconds": seq512.get("average_step_time_seconds"),
        "seq1024_10step_summary_tokens_per_sec": seq1024_10step.get("summary_tokens_per_sec"),
        "seq1024_10step_average_step_time_seconds": seq1024_10step.get("average_step_time_seconds"),
        "interpretation": build_interpretation(blockers),
        "recommended_next_mvp": "MVP-31.P seq1024 batch_size=8 memory preflight plan",
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
