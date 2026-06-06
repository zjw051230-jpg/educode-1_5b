from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class RunRecord:
    run_id: str
    run_name: str
    run_type: str
    artifact_dir: str
    summary_path: str
    success: bool
    context_length: int
    batch_size: int
    grad_accum: int
    max_steps: int
    attention_backend: str | None = None
    runtime_device: str | None = None
    runtime_dtype: str | None = None
    data_loading_mode: str | None = None
    final_train_loss: float | None = None
    final_validation_loss: float | None = None
    tokens_per_sec: float | None = None
    peak_allocated_memory_gib: float | None = None
    peak_reserved_memory_gib: float | None = None

    def __post_init__(self) -> None:
        if not self.run_id.strip():
            raise ValueError("run_id is required")
        if not self.run_name.strip():
            raise ValueError("run_name is required")
        if self.run_type not in {"training", "profile", "preflight", "smoke", "unknown"}:
            raise ValueError(f"unsupported run_type: {self.run_type}")
        if not self.artifact_dir.strip():
            raise ValueError("artifact_dir is required")
        if not self.summary_path.strip():
            raise ValueError("summary_path is required")
        for field_name in ("context_length", "batch_size", "grad_accum", "max_steps"):
            if getattr(self, field_name) <= 0:
                raise ValueError(f"{field_name} must be positive")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "RunRecord":
        return cls(
            run_id=str(payload.get("run_id", "")),
            run_name=str(payload.get("run_name", "")),
            run_type=str(payload.get("run_type", "unknown")),
            artifact_dir=str(payload.get("artifact_dir", "")),
            summary_path=str(payload.get("summary_path", "")),
            success=bool(payload.get("success", False)),
            context_length=int(payload.get("context_length", 0)),
            batch_size=int(payload.get("batch_size", 0)),
            grad_accum=int(payload.get("grad_accum", 0)),
            max_steps=int(payload.get("max_steps", 0)),
            attention_backend=_optional_str(payload.get("attention_backend")),
            runtime_device=_optional_str(payload.get("runtime_device")),
            runtime_dtype=_optional_str(payload.get("runtime_dtype")),
            data_loading_mode=_optional_str(payload.get("data_loading_mode")),
            final_train_loss=_optional_float(payload.get("final_train_loss")),
            final_validation_loss=_optional_float(payload.get("final_validation_loss")),
            tokens_per_sec=_optional_float(payload.get("tokens_per_sec")),
            peak_allocated_memory_gib=_optional_float(payload.get("peak_allocated_memory_gib")),
            peak_reserved_memory_gib=_optional_float(payload.get("peak_reserved_memory_gib")),
        )


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _optional_float(value: object) -> float | None:
    if value is None:
        return None
    return float(value)


def normalize_repo_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def infer_run_type(summary: dict[str, object]) -> str:
    run_name = str(summary.get("run_name") or summary.get("run_id") or "").lower()
    config_path = str(summary.get("config_path") or "").lower()
    haystack = f"{run_name} {config_path}"
    if "preflight" in haystack:
        return "preflight"
    if "profile" in haystack or "profiling" in haystack:
        return "profile"
    if "smoke" in haystack or "10step" in haystack or "100step" in haystack:
        return "smoke"
    if int(summary.get("max_steps") or 0) >= 1000:
        return "training"
    return "unknown"


def extract_attention_backend(summary: dict[str, object]) -> str | None:
    for key in ("attention_backend",):
        if summary.get(key):
            return str(summary[key])
    for feature_key in ("declared_model_features", "current_core_model_features"):
        features = summary.get(feature_key)
        if isinstance(features, dict) and features.get("attention_backend"):
            return str(features["attention_backend"])
    return None


def import_summary_file(summary_path: Path, *, repo_root: Path | None = None) -> RunRecord:
    repo_root = repo_root or Path.cwd()
    with summary_path.open("r", encoding="utf-8") as handle:
        summary = json.load(handle)

    if not isinstance(summary, dict):
        raise ValueError(f"summary must be a JSON object: {summary_path}")

    run_name = str(summary.get("run_name") or summary.get("run_id") or "")
    output_dir = str(summary.get("output_dir") or summary_path.parent.parent.as_posix())
    return RunRecord(
        run_id=str(summary.get("run_id") or run_name),
        run_name=run_name,
        run_type=infer_run_type(summary),
        artifact_dir=output_dir,
        summary_path=normalize_repo_path(summary_path, repo_root),
        success=bool(summary.get("success", False)),
        context_length=int(summary.get("sequence_length") or summary.get("context_length") or 0),
        batch_size=int(summary.get("batch_size") or 0),
        grad_accum=int(summary.get("gradient_accumulation_steps") or summary.get("grad_accum") or 0),
        max_steps=int(summary.get("max_steps") or 0),
        attention_backend=extract_attention_backend(summary),
        runtime_device=_optional_str(summary.get("runtime_device")),
        runtime_dtype=_optional_str(summary.get("runtime_dtype")),
        data_loading_mode=_optional_str(summary.get("data_loading_mode")),
        final_train_loss=_optional_float(summary.get("final_train_loss")),
        final_validation_loss=_optional_float(
            summary.get("final_val_loss", summary.get("final_validation_loss"))
        ),
        tokens_per_sec=_optional_float(
            summary.get("approximate_tokens_per_sec", summary.get("tokens_per_sec"))
        ),
        peak_allocated_memory_gib=_optional_float(summary.get("last_gpu_memory_allocated_gib")),
        peak_reserved_memory_gib=_optional_float(summary.get("last_gpu_memory_reserved_gib")),
    )


def find_imported_summary_files(repo_root: Path) -> list[Path]:
    experiments_dir = repo_root / "experiments"
    if not experiments_dir.exists():
        return []
    return sorted(
        path
        for path in experiments_dir.rglob("summary.json")
        if any(part.startswith("results_imported") for part in path.parts)
    )


def write_registry(registry_path: Path, records: Iterable[RunRecord]) -> None:
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with registry_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")


def append_record(registry_path: Path, record: RunRecord) -> None:
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with registry_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")


def load_registry(registry_path: Path) -> list[RunRecord]:
    records: list[RunRecord] = []
    with registry_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            if not isinstance(payload, dict):
                raise ValueError(f"registry line {line_number} must be a JSON object")
            records.append(RunRecord.from_dict(payload))
    return records


def query_records(
    records: Iterable[RunRecord],
    *,
    run_type: str | None = None,
    attention_backend: str | None = None,
    context_length: int | None = None,
    batch_size: int | None = None,
    success: bool | None = None,
) -> list[RunRecord]:
    matches: list[RunRecord] = []
    for record in records:
        if run_type is not None and record.run_type != run_type:
            continue
        if attention_backend is not None and record.attention_backend != attention_backend:
            continue
        if context_length is not None and record.context_length != context_length:
            continue
        if batch_size is not None and record.batch_size != batch_size:
            continue
        if success is not None and record.success != success:
            continue
        matches.append(record)
    return matches
