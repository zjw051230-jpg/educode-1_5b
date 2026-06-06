from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_ARTIFACT_DIRS = [
    REPO_ROOT
    / "experiments/a100/fineweb_edu_5gb_300m_3000step_public16k_execute/results_imported_modal_streaming",
    REPO_ROOT
    / "experiments/a100/fineweb_edu_5gb_300m_50step_public16k_sdpa_profile/results_imported_modal_streaming",
    REPO_ROOT
    / "experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/results_imported_modal_streaming",
    REPO_ROOT
    / "experiments/a100/fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile/results_imported_modal_streaming",
]

DEFAULT_OUTPUT_PATH = REPO_ROOT / "docs/generated_reports/training_report_summary.md"


@dataclass(frozen=True)
class RunSummary:
    name: str
    artifact_dir: Path
    success: bool | None
    max_steps: int | None
    context_length: int | None
    batch_size: int | None
    grad_accum: int | None
    final_train_loss: float | None
    final_validation_loss: float | None
    summary_tokens_per_sec: float | None
    mean_step_tokens_per_sec: float | None
    last_gpu_memory_allocated_gib: float | None
    last_gpu_memory_reserved_gib: float | None
    metrics_rows: int
    validation_rows: int

    @property
    def short_label(self) -> str:
        parts = []
        if self.context_length:
            parts.append(f"seq{self.context_length}")
        if self.batch_size:
            parts.append(f"batch{self.batch_size}")
        if self.max_steps:
            parts.append(f"{self.max_steps}step")
        return " ".join(parts) if parts else self.name


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _first_present(data: dict, keys: Iterable[str]):
    for key in keys:
        if key in data:
            return data[key]
    return None


def summarize_run(artifact_dir: Path) -> RunSummary:
    summary_path = artifact_dir / "summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(f"missing summary.json: {summary_path}")

    summary = _read_json(summary_path)
    metrics = _read_jsonl(artifact_dir / "metrics.jsonl")
    validation_metrics = _read_jsonl(artifact_dir / "validation_metrics.jsonl")
    step_tokens = [
        row["tokens_per_sec"]
        for row in metrics
        if isinstance(row.get("tokens_per_sec"), (int, float))
    ]

    return RunSummary(
        name=str(summary.get("run_name") or artifact_dir.parent.name),
        artifact_dir=artifact_dir,
        success=summary.get("success"),
        max_steps=summary.get("max_steps"),
        context_length=_first_present(summary, ["sequence_length", "context_length"]),
        batch_size=summary.get("batch_size"),
        grad_accum=_first_present(
            summary, ["gradient_accumulation_steps", "grad_accum"]
        ),
        final_train_loss=summary.get("final_train_loss"),
        final_validation_loss=_first_present(
            summary, ["final_val_loss", "final_validation_loss"]
        ),
        summary_tokens_per_sec=_first_present(
            summary, ["approximate_tokens_per_sec", "tokens_per_sec"]
        ),
        mean_step_tokens_per_sec=mean(step_tokens) if step_tokens else None,
        last_gpu_memory_allocated_gib=_first_present(
            summary, ["last_gpu_memory_allocated_gib", "peak_allocated_memory_gib"]
        ),
        last_gpu_memory_reserved_gib=_first_present(
            summary, ["last_gpu_memory_reserved_gib", "peak_reserved_memory_gib"]
        ),
        metrics_rows=len(metrics),
        validation_rows=len(validation_metrics),
    )


def collect_runs(artifact_dirs: Iterable[Path]) -> list[RunSummary]:
    runs = []
    for artifact_dir in artifact_dirs:
        if (artifact_dir / "summary.json").exists():
            runs.append(summarize_run(artifact_dir))
    return runs


def _fmt(value, digits: int = 6) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def build_report(runs: list[RunSummary]) -> str:
    lines = [
        "# Training Report Summary",
        "",
        "This generated report summarizes committed imported artifact metadata only. It does not read root-level result tarballs, checkpoints, raw data, or prepared data.",
        "",
        "## Runs",
        "",
        "| Run | Status | Rows | Loss | Throughput | Memory |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for run in runs:
        status = "success" if run.success else "unknown"
        rows = f"metrics {run.metrics_rows}, val {run.validation_rows}"
        loss = (
            f"train {_fmt(run.final_train_loss)}, "
            f"val {_fmt(run.final_validation_loss)}"
        )
        throughput = (
            f"summary {_fmt(run.summary_tokens_per_sec)}, "
            f"step mean {_fmt(run.mean_step_tokens_per_sec)} tokens/sec"
        )
        memory = (
            f"alloc {_fmt(run.last_gpu_memory_allocated_gib)} GiB, "
            f"reserved {_fmt(run.last_gpu_memory_reserved_gib)} GiB"
        )
        lines.append(
            f"| {run.short_label} | {status} | {rows} | {loss} | {throughput} | {memory} |"
        )

    lines.extend(
        [
            "",
            "## Comparability Notes",
            "",
            "- seq512 and seq1024 profiling rows are systems evidence for throughput, step time, and memory.",
            "- Short 10-step and 50-step runs are not model-quality evidence.",
            "- 3000-step training loss is useful for trend sanity checks only when paired with validation coverage notes.",
            "",
            "## Quality Caveat",
            "",
            "Loss values from short profiling or memory preflight runs are sanity signals. They should not be described as quality training results.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(output_path: Path, artifact_dirs: Iterable[Path]) -> list[RunSummary]:
    runs = collect_runs(artifact_dirs)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_report(runs), encoding="utf-8")
    return runs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a markdown report from imported training artifacts."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Markdown report path.",
    )
    args = parser.parse_args()

    runs = write_report(args.output, DEFAULT_ARTIFACT_DIRS)
    result = {
        "report_status": "generated",
        "output_path": str(args.output),
        "runs": len(runs),
        "modal_gpu_training_run": False,
        "tarballs_read": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
