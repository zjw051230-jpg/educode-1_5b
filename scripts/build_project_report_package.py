from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_SUFFIXES = (
    ".tar.gz",
    ".tgz",
    ".zip",
    ".pt",
    ".pth",
    ".ckpt",
    ".safetensors",
    ".bin",
)
SAFE_DOC_PREFIXES = ("docs/",)
SAFE_IMPORTED_MARKER = "/results_imported"
RAW_DATA_MARKERS = ("/raw/", "/prepared/", "/prepared_data/", "/splits/")


@dataclass(frozen=True)
class ReportSource:
    path: str
    source_type: str
    title: str
    summary: str


def normalize_path(path: str | Path) -> str:
    return str(path).replace("\\", "/").strip()


def is_safe_report_source(path: str | Path) -> bool:
    normalized = normalize_path(path).lower()
    with_slashes = f"/{normalized}"
    if any(normalized.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES):
        return False
    if "/checkpoints/" in with_slashes or "/checkpoint" in with_slashes:
        return False
    if "/data/" in with_slashes and any(marker in with_slashes for marker in RAW_DATA_MARKERS):
        return False
    if normalized.startswith(SAFE_DOC_PREFIXES) and normalized.endswith(".md"):
        return True
    return SAFE_IMPORTED_MARKER in with_slashes and normalized.endswith((".json", ".jsonl", ".md", ".txt"))


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def summarize_markdown(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped[:160]
    return "Markdown evidence document."


def summarize_json(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return "JSON evidence artifact."
    interesting = []
    for key in ("run_name", "success", "max_steps", "batch_size", "sequence_length", "approximate_tokens_per_sec"):
        if key in payload:
            interesting.append(f"{key}={payload[key]}")
    return ", ".join(interesting) if interesting else "JSON evidence artifact."


def source_title(relative_path: str) -> str:
    stem = Path(relative_path).stem.replace("_", " ").replace("-", " ").strip()
    return stem.title() if stem else relative_path


def build_source(path: Path, repo_root: Path) -> ReportSource:
    relative_path = repo_relative(path, repo_root)
    suffix = path.suffix.lower()
    if suffix == ".md":
        source_type = "markdown"
        summary = summarize_markdown(path)
    elif suffix == ".json":
        source_type = "json"
        summary = summarize_json(path)
    else:
        source_type = suffix.lstrip(".") or "text"
        summary = "Small imported text artifact."
    return ReportSource(
        path=relative_path,
        source_type=source_type,
        title=source_title(relative_path),
        summary=summary,
    )


def collect_report_sources(repo_root: Path = REPO_ROOT) -> list[ReportSource]:
    candidates: list[Path] = []
    docs_dir = repo_root / "docs"
    experiments_dir = repo_root / "experiments"
    if docs_dir.exists():
        candidates.extend(docs_dir.rglob("*.md"))
    if experiments_dir.exists():
        candidates.extend(
            path
            for path in experiments_dir.rglob("*")
            if path.is_file() and any(part.startswith("results_imported") for part in path.parts)
        )

    sources = [
        build_source(path, repo_root)
        for path in sorted(candidates)
        if path.is_file() and is_safe_report_source(repo_relative(path, repo_root))
    ]
    return sorted(sources, key=lambda source: source.path)


def build_report_text(sources: Iterable[ReportSource]) -> str:
    ordered_sources = sorted(sources, key=lambda source: source.path)
    lines = [
        "# Project Report Package",
        "",
        "Generated from selected small documentation and imported artifact summaries.",
        "Safety boundary: excluded tarballs/checkpoints/raw data.",
        "",
        f"Source count: {len(ordered_sources)}",
        "",
        "## Evidence Index",
        "",
    ]
    for source in ordered_sources:
        lines.extend(
            [
                f"### {source.path}",
                "",
                f"- Type: {source.source_type}",
                f"- Title: {source.title}",
                f"- Summary: {source.summary}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def ensure_safe_output_path(repo_root: Path, output_path: Path) -> Path:
    resolved_root = repo_root.resolve()
    resolved_output = output_path.resolve()
    safe_dir = (repo_root / "docs" / "generated").resolve()
    try:
        resolved_output.relative_to(safe_dir)
    except ValueError as exc:
        raise ValueError("output must be under docs/generated") from exc
    try:
        resolved_output.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError("output must stay inside the repository") from exc
    return resolved_output


def write_project_report(repo_root: Path, output_path: Path) -> Path:
    safe_output = ensure_safe_output_path(repo_root, output_path)
    report_text = build_report_text(collect_report_sources(repo_root))
    safe_output.parent.mkdir(parents=True, exist_ok=True)
    safe_output.write_text(report_text, encoding="utf-8", newline="\n")
    return safe_output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a deterministic project report from safe local artifacts.")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--output", type=Path, help="Optional output path under docs/generated.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sources = collect_report_sources(args.repo_root)
    output_path = None
    if args.output:
        output_path = str(write_project_report(args.repo_root, args.output))
    payload = {
        "report_package_status": "passed",
        "source_count": len(sources),
        "output_written": output_path is not None,
        "output_path": output_path,
        "tarballs_included": False,
        "checkpoints_included": False,
        "raw_data_included": False,
        "source_preview": [source.path for source in sources[:20]],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
