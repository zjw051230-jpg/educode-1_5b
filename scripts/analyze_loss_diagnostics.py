from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.diagnostics import diagnose_metrics, read_metrics_jsonl  # noqa: E402

DEFAULT_ARTIFACT_DIR = (
    REPO_ROOT
    / "experiments/a100/fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile/results_imported_modal_streaming"
)


def build_markdown(report: dict, artifact_dir: Path) -> str:
    return "\n".join(
        [
            "# Loss Metric Diagnostics Report",
            "",
            f"- Artifact dir: `{artifact_dir.as_posix()}`",
            f"- Metrics rows: `{report['row_count']}`",
            f"- Validation rows: `{report['validation_rows']}`",
            f"- Losses all finite: `{str(report['losses_all_finite']).lower()}`",
            f"- Non-finite steps: `{report['non_finite_steps']}`",
            f"- Spike steps: `{report['spike_steps']}`",
            f"- Final train loss: `{report['final_train_loss']}`",
            f"- Final validation loss: `{report['final_validation_loss']}`",
            f"- Mean tokens/sec: `{report['mean_tokens_per_sec']}`",
            f"- Divergence warning: `{str(report['divergence_warning']).lower()}`",
            "",
            "This is a local diagnostics pass only. It does not run Modal, GPU, training, profiling, or preflight jobs.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze imported metrics.jsonl for loss/throughput diagnostics."
    )
    parser.add_argument("--artifact-dir", type=Path, default=DEFAULT_ARTIFACT_DIR)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()

    metrics = read_metrics_jsonl(args.artifact_dir / "metrics.jsonl")
    validation = read_metrics_jsonl(args.artifact_dir / "validation_metrics.jsonl")
    report = diagnose_metrics(metrics, validation).to_dict()
    report.update(
        {
            "analysis_status": "passed" if report["losses_all_finite"] else "warning",
            "artifact_dir": str(args.artifact_dir),
            "modal_gpu_training_run": False,
        }
    )

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(build_markdown(report, args.artifact_dir), encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
