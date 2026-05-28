from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULT_3000_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_3000step_public16k_execute"
    / "results_imported_modal_streaming"
)
RESULT_1000_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_1000step_public16k_execute"
    / "results_imported_modal_streaming"
)
ANALYSIS_SUMMARY_PATH = RESULT_3000_DIR / "mvp27_a_analysis_summary.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def loss_direction(first: float, last: float) -> str:
    if last < first:
        return "down"
    if last > first:
        return "up"
    return "flat"


def round_float(value: Any, digits: int = 6) -> Any:
    if isinstance(value, float):
        return round(value, digits)
    return value


def build_recommendation(summary: dict[str, Any], blockers: list[str]) -> str:
    if blockers:
        return "Blockers remain; do not plan another training run until imported artifacts are fixed."
    if summary["validation_prefix_only_risk"]:
        return "Do not continue scaling until validation coverage is fixed."
    if summary["comparison_vs_5gb_1000_final_validation_loss_delta"] < 0:
        return (
            "Proceed to MVP-27.B for next-stage experiment route selection. The 3000-step run improves "
            "validation measurement and final validation loss versus the 5GB 1000-step baseline, but do "
            "not jump directly to 10000-step; compare a bounded 5GB 5000-step option against technical "
            "experiments such as AdamW vs Muon, context length 1024, SDPA/FlashAttention profiling, and "
            "B200 scale planning."
        )
    return "Analyze stability further before spending on longer runs; prefer technical experiments over more steps."


def analyze() -> dict[str, Any]:
    blockers: list[str] = []

    required_3000 = [
        RESULT_3000_DIR / "summary.json",
        RESULT_3000_DIR / "metrics.jsonl",
        RESULT_3000_DIR / "validation_metrics.jsonl",
        RESULT_3000_DIR / "post_run_artifact_validation_summary.json",
        RESULT_3000_DIR / "import_validation_summary.json",
    ]
    required_1000 = [
        RESULT_1000_DIR / "summary.json",
        RESULT_1000_DIR / "metrics.jsonl",
        RESULT_1000_DIR / "validation_metrics.jsonl",
    ]
    for path in required_3000 + required_1000:
        if not path.exists():
            blockers.append(f"missing required artifact: {path.relative_to(PROJECT_ROOT).as_posix()}")

    if blockers:
        result = {"analysis_status": "failed", "blocker_count": len(blockers), "blockers": blockers}
        write_analysis(result)
        return result

    summary_3000 = load_json(RESULT_3000_DIR / "summary.json")
    post_run_3000 = load_json(RESULT_3000_DIR / "post_run_artifact_validation_summary.json")
    import_validation_3000 = load_json(RESULT_3000_DIR / "import_validation_summary.json")
    metrics_3000 = load_jsonl(RESULT_3000_DIR / "metrics.jsonl")
    validation_3000 = load_jsonl(RESULT_3000_DIR / "validation_metrics.jsonl")

    summary_1000 = load_json(RESULT_1000_DIR / "summary.json")

    train_losses = [float(row["train_loss"]) for row in metrics_3000 if "train_loss" in row]
    validation_losses = [float(row["val_loss"]) for row in validation_3000 if "val_loss" in row]
    if not train_losses:
        blockers.append("metrics.jsonl has no train_loss values")
    if not validation_losses:
        blockers.append("validation_metrics.jsonl has no val_loss values")

    metrics_rows = len(metrics_3000)
    validation_rows = len(validation_3000)
    if metrics_rows != 3000:
        blockers.append(f"metrics_rows expected 3000, got {metrics_rows}")
    if validation_rows != 10:
        blockers.append(f"validation_rows expected 10, got {validation_rows}")
    if summary_3000.get("success") is not True:
        blockers.append(f"summary.success expected true, got {summary_3000.get('success')!r}")
    if post_run_3000.get("blocker_count") != 0:
        blockers.append(f"post-run blocker_count expected 0, got {post_run_3000.get('blocker_count')!r}")
    if import_validation_3000.get("validation_status") != "passed":
        blockers.append(f"import validation expected passed, got {import_validation_3000.get('validation_status')!r}")

    first_train_loss = train_losses[0] if train_losses else None
    last_train_loss = train_losses[-1] if train_losses else None
    first_validation_loss = validation_losses[0] if validation_losses else None
    last_validation_loss = validation_losses[-1] if validation_losses else None
    validation_loss_range = max(validation_losses) - min(validation_losses) if validation_losses else None
    validation_loss_population_stddev = statistics.pstdev(validation_losses) if len(validation_losses) > 1 else 0.0

    final_train_loss = summary_3000.get("final_train_loss")
    final_validation_loss = summary_3000.get("final_val_loss")
    comparison_train_delta = final_train_loss - summary_1000.get("final_train_loss")
    comparison_validation_delta = final_validation_loss - summary_1000.get("final_val_loss")

    result = {
        "analysis_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "metrics_rows": metrics_rows,
        "validation_rows": validation_rows,
        "first_train_loss": round_float(first_train_loss),
        "last_train_loss": round_float(last_train_loss),
        "min_train_loss": round_float(min(train_losses)) if train_losses else None,
        "max_train_loss": round_float(max(train_losses)) if train_losses else None,
        "first_validation_loss": round_float(first_validation_loss),
        "last_validation_loss": round_float(last_validation_loss),
        "min_validation_loss": round_float(min(validation_losses)) if validation_losses else None,
        "max_validation_loss": round_float(max(validation_losses)) if validation_losses else None,
        "validation_loss_range": round_float(validation_loss_range),
        "validation_loss_population_stddev": round_float(validation_loss_population_stddev),
        "final_train_loss": final_train_loss,
        "final_validation_loss": final_validation_loss,
        "validation_unique_doc_count": summary_3000.get("validation_unique_doc_count"),
        "validation_prefix_only_risk": summary_3000.get("validation_prefix_only_risk"),
        "train_loss_direction_first_to_last": loss_direction(first_train_loss, last_train_loss)
        if first_train_loss is not None and last_train_loss is not None
        else None,
        "validation_loss_direction_first_to_last": loss_direction(first_validation_loss, last_validation_loss)
        if first_validation_loss is not None and last_validation_loss is not None
        else None,
        "comparison_vs_5gb_1000_final_train_loss_delta": round_float(comparison_train_delta),
        "comparison_vs_5gb_1000_final_validation_loss_delta": round_float(comparison_validation_delta),
        "comparison_vs_5gb_1000_final_train_loss": summary_1000.get("final_train_loss"),
        "comparison_vs_5gb_1000_final_validation_loss": summary_1000.get("final_val_loss"),
        "recommendation": "",
    }
    result["recommendation"] = build_recommendation(result, blockers)
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
