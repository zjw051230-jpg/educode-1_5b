from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_PARAMETER_COUNT = 319329280
EXPECTED_RUNTIME_DEVICE = "cuda"
EXPECTED_RUNTIME_DTYPE = "bf16"
POSITION_MISMATCH_TEXT = "position_encoding: declared='rope', implemented='learned_position_embedding'"

RUNS = [
    {
        "name": "mvp8",
        "label": "MVP-8 A800 300M 10-step training smoke",
        "results_dir": PROJECT_ROOT / "experiments" / "a100" / "fineweb_edu_50mb_300m_10step_execute" / "results_imported",
        "expected_max_steps": 10,
        "expected_final_step": 10,
        "expected_validation_rows": 2,
        "expected_checkpoint_path_prefix": "experiments/a100/fineweb_edu_50mb_300m_10step_execute/",
        "expect_validation_metrics_file": False,
        "expect_checkpoint_path_match": True,
    },
    {
        "name": "mvp9",
        "label": "MVP-9 A800 300M 100-step bounded run",
        "results_dir": PROJECT_ROOT / "experiments" / "a100" / "fineweb_edu_50mb_300m_100step_execute" / "results_imported",
        "expected_max_steps": 100,
        "expected_final_step": 100,
        "expected_validation_rows": 5,
        "expected_checkpoint_path_prefix": "experiments/a100/fineweb_edu_50mb_300m_100step_execute/",
        "expect_validation_metrics_file": False,
        "expect_checkpoint_path_match": False,
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            records.append(json.loads(line))
    return records


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_run(run: dict[str, Any]) -> dict[str, Any]:
    results_dir = run["results_dir"]
    summary_path = results_dir / "summary.json"
    metrics_path = results_dir / "metrics.jsonl"
    validation_metrics_path = results_dir / "validation_metrics.jsonl"

    blockers: list[str] = []
    caveats: list[str] = []

    if not summary_path.exists():
        blockers.append(f"missing summary.json: {summary_path}")
        summary: dict[str, Any] = {}
    else:
        summary = load_json(summary_path)

    if not metrics_path.exists():
        blockers.append(f"missing metrics.jsonl: {metrics_path}")
        metrics: list[dict[str, Any]] = []
    else:
        metrics = load_jsonl(metrics_path)

    if not blockers:
        if summary.get("success") is not True:
            blockers.append("summary.success must be true")
        if summary.get("runtime_device") != EXPECTED_RUNTIME_DEVICE:
            blockers.append(f"runtime_device must be {EXPECTED_RUNTIME_DEVICE}")
        if summary.get("runtime_dtype") != EXPECTED_RUNTIME_DTYPE:
            blockers.append(f"runtime_dtype must be {EXPECTED_RUNTIME_DTYPE}")
        if summary.get("exact_parameter_count") != EXPECTED_PARAMETER_COUNT:
            blockers.append(f"exact_parameter_count must be {EXPECTED_PARAMETER_COUNT}")
        if summary.get("loss_all_finite") is not True:
            blockers.append("loss_all_finite must be true")
        if summary.get("grad_all_finite") is not True:
            blockers.append("grad_all_finite must be true")
        if summary.get("checkpoint_reload_match") is not True:
            blockers.append("checkpoint_reload_match must be true")
        if int(summary.get("metrics_rows", -1)) != len(metrics):
            blockers.append("metrics.jsonl row count must match summary.metrics_rows")
        if int(summary.get("max_steps", -1)) != int(run["expected_max_steps"]):
            blockers.append(f"max_steps must equal {run['expected_max_steps']}")
        if int(summary.get("validation_rows", -1)) != int(run["expected_validation_rows"]):
            blockers.append(f"validation_rows must equal {run['expected_validation_rows']}")

        steps = [record.get("step") for record in metrics]
        if run["expected_final_step"] not in steps:
            blockers.append(f"metrics.jsonl must include step {run['expected_final_step']}")

        eval_rows = [record for record in metrics if record.get("val_loss") is not None]
        if not eval_rows:
            blockers.append("metrics.jsonl must contain eval rows with val_loss")
        if len(eval_rows) != int(summary.get("validation_rows", -1)):
            blockers.append("eval rows with val_loss must match summary.validation_rows")

        mismatches = summary.get("declared_vs_core_feature_mismatches") or []
        if POSITION_MISMATCH_TEXT in mismatches:
            caveats.append("core_model_feature_parity=false due to declared rope vs implemented learned_position_embedding")
        elif summary.get("declared_model_features", {}).get("position_encoding") == "rope":
            caveats.append("position_encoding mismatch not found in mismatch list but rope is still declared")

        if not validation_metrics_path.exists():
            caveats.append("standalone validation_metrics.jsonl is missing; validation rows are embedded in metrics.jsonl")

        checkpoint_path = str(summary.get("checkpoint_path", ""))
        expected_prefix = str(run["expected_checkpoint_path_prefix"])
        if checkpoint_path and not checkpoint_path.startswith(expected_prefix):
            caveats.append(
                f"checkpoint_path logging/path mismatch: {checkpoint_path} does not start with {expected_prefix}"
            )
            if run["expect_checkpoint_path_match"]:
                blockers.append("checkpoint_path points outside the expected run directory")

    validation_summary = {
        "run": run["name"],
        "label": run["label"],
        "results_dir": str(results_dir.relative_to(PROJECT_ROOT)).replace('\\', '/'),
        "summary_path": str(summary_path.relative_to(PROJECT_ROOT)).replace('\\', '/'),
        "metrics_path": str(metrics_path.relative_to(PROJECT_ROOT)).replace('\\', '/'),
        "status": "success" if not blockers else "failed",
        "success": not blockers,
        "metrics_rows": len(metrics),
        "validation_rows_in_metrics": len([record for record in metrics if record.get("val_loss") is not None]),
        "final_step_present": run["expected_final_step"] in [record.get("step") for record in metrics],
        "runtime_device": summary.get("runtime_device"),
        "runtime_dtype": summary.get("runtime_dtype"),
        "exact_parameter_count": summary.get("exact_parameter_count"),
        "loss_all_finite": summary.get("loss_all_finite"),
        "val_loss_all_finite": summary.get("val_loss_all_finite"),
        "grad_all_finite": summary.get("grad_all_finite"),
        "checkpoint_reload_match": summary.get("checkpoint_reload_match"),
        "checkpoint_path": summary.get("checkpoint_path"),
        "final_train_loss": summary.get("final_train_loss"),
        "final_val_loss": summary.get("final_val_loss"),
        "blockers": blockers,
        "caveats": caveats,
    }
    return validation_summary


def main() -> int:
    exit_code = 0
    for run in RUNS:
        validation_summary = validate_run(run)
        summary_path = run["results_dir"] / "import_validation_summary.json"
        write_json(summary_path, validation_summary)
        print(f"{run['name']}: status={validation_summary['status']}")
        print(f"{run['name']}: metrics_rows={validation_summary['metrics_rows']}")
        print(f"{run['name']}: caveats={len(validation_summary['caveats'])}")
        print(
            f"{run['name']}: import_validation_summary={summary_path.relative_to(PROJECT_ROOT).as_posix()}"
        )
        if not validation_summary["success"]:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
