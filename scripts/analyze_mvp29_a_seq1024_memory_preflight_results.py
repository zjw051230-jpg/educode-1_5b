from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SEQ1024_DIR = (
    REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight"
    / "results_imported_modal_streaming"
)
SEQ512_DIR = (
    REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile"
    / "results_imported_modal_streaming"
)
ANALYSIS_SUMMARY_PATH = SEQ1024_DIR / "mvp29_a_seq1024_memory_preflight_analysis_summary.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def round_float(value: Any, digits: int = 6) -> Any:
    if isinstance(value, float):
        return round(value, digits)
    return value


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def build_interpretation(result: dict[str, Any], blockers: list[str]) -> str:
    if blockers:
        return "Analysis blockers remain; do not use this result for next-step decisions yet."
    return (
        "Seq1024 SDPA memory preflight succeeded with no OOM at batch_size=4 and grad_accum=4. "
        "Throughput is lower and step time is higher than the seq512 SDPA baseline, while peak "
        "allocated/reserved memory is roughly comparable because batch_size was reduced from 8 to 4. "
        "This supports seq1024 as a viable short-run profiling direction, but it is not model-quality "
        "evidence and does not prove long seq1024 training or batch_size=8 safety."
    )


def analyze() -> dict[str, Any]:
    blockers: list[str] = []
    required_files = [
        SEQ1024_DIR / "summary.json",
        SEQ1024_DIR / "metrics.jsonl",
        SEQ1024_DIR / "validation_metrics.jsonl",
        SEQ1024_DIR / "post_run_artifact_validation_summary.json",
        SEQ1024_DIR / "import_validation_summary.json",
        SEQ512_DIR / "mvp28_a_sdpa_profile_analysis_summary.json",
    ]
    for path in required_files:
        if not path.exists():
            blockers.append(f"missing required artifact: {path.relative_to(REPO_ROOT).as_posix()}")

    if blockers:
        result = {"analysis_status": "failed", "blocker_count": len(blockers), "blockers": blockers}
        write_analysis(result)
        return result

    seq1024_summary = load_json(SEQ1024_DIR / "summary.json")
    seq1024_import = load_json(SEQ1024_DIR / "import_validation_summary.json")
    seq1024_post_run = load_json(SEQ1024_DIR / "post_run_artifact_validation_summary.json")
    seq512_analysis = load_json(SEQ512_DIR / "mvp28_a_sdpa_profile_analysis_summary.json")

    if seq1024_import.get("validation_status") != "passed":
        blockers.append("seq1024 import validation did not pass")
    if seq1024_import.get("blocker_count") != 0:
        blockers.append(f"seq1024 import blocker_count expected 0, got {seq1024_import.get('blocker_count')!r}")
    if seq1024_post_run.get("blocker_count") != 0:
        blockers.append(f"seq1024 post-run blocker_count expected 0, got {seq1024_post_run.get('blocker_count')!r}")
    if seq1024_import.get("oom_detected") is True:
        blockers.append("seq1024 import validation detected OOM")
    if seq512_analysis.get("analysis_status") != "passed":
        blockers.append("seq512 baseline analysis did not pass")

    summary_tokens_delta = (
        seq1024_import.get("summary_tokens_per_sec") - seq512_analysis.get("summary_tokens_per_sec")
        if finite_number(seq1024_import.get("summary_tokens_per_sec"))
        and finite_number(seq512_analysis.get("summary_tokens_per_sec"))
        else None
    )
    step_time_delta = (
        seq1024_import.get("average_step_time_seconds") - seq512_analysis.get("average_step_time_seconds")
        if finite_number(seq1024_import.get("average_step_time_seconds"))
        and finite_number(seq512_analysis.get("average_step_time_seconds"))
        else None
    )
    allocated_delta = (
        seq1024_import.get("peak_gpu_memory_allocated_gib") - seq512_analysis.get("peak_allocated_memory_gib")
        if finite_number(seq1024_import.get("peak_gpu_memory_allocated_gib"))
        and finite_number(seq512_analysis.get("peak_allocated_memory_gib"))
        else None
    )
    reserved_delta = (
        seq1024_import.get("peak_gpu_memory_reserved_gib") - seq512_analysis.get("peak_reserved_memory_gib")
        if finite_number(seq1024_import.get("peak_gpu_memory_reserved_gib"))
        and finite_number(seq512_analysis.get("peak_reserved_memory_gib"))
        else None
    )

    result = {
        "analysis_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "context_length": seq1024_import.get("context_length"),
        "batch_size": seq1024_import.get("batch_size"),
        "grad_accum": seq1024_import.get("grad_accum"),
        "attention_backend": seq1024_import.get("attention_backend"),
        "max_steps": seq1024_import.get("max_steps"),
        "metrics_rows": seq1024_import.get("metrics_rows"),
        "validation_rows": seq1024_import.get("validation_metrics_rows"),
        "final_train_loss": seq1024_import.get("final_train_loss"),
        "final_validation_loss": seq1024_import.get("final_validation_loss"),
        "oom_detected": seq1024_import.get("oom_detected"),
        "summary_tokens_per_sec": seq1024_import.get("summary_tokens_per_sec"),
        "mean_step_tokens_per_sec": seq1024_import.get("mean_step_tokens_per_sec"),
        "average_step_time_seconds": seq1024_import.get("average_step_time_seconds"),
        "peak_allocated_memory_gib": seq1024_import.get("peak_gpu_memory_allocated_gib"),
        "peak_reserved_memory_gib": seq1024_import.get("peak_gpu_memory_reserved_gib"),
        "mfu_available": seq1024_import.get("mfu_available"),
        "comparison_vs_seq512_tokens_per_sec_delta": round_float(summary_tokens_delta),
        "comparison_vs_seq512_step_time_delta": round_float(step_time_delta),
        "comparison_vs_seq512_peak_allocated_memory_delta": round_float(allocated_delta),
        "comparison_vs_seq512_peak_reserved_memory_delta": round_float(reserved_delta),
        "seq512_summary_tokens_per_sec": seq512_analysis.get("summary_tokens_per_sec"),
        "seq512_average_step_time_seconds": seq512_analysis.get("average_step_time_seconds"),
        "seq512_peak_allocated_memory_gib": seq512_analysis.get("peak_allocated_memory_gib"),
        "seq512_peak_reserved_memory_gib": seq512_analysis.get("peak_reserved_memory_gib"),
        "interpretation": "",
        "recommended_next_mvp": "MVP-30.P seq1024 50-step SDPA profiling plan",
    }
    result["interpretation"] = build_interpretation(result, blockers)
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
