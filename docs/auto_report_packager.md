# Auto Report Packager

This branch adds a local project report packager skeleton. It collects selected Markdown documents and small imported artifact summaries into a deterministic evidence index while excluding tarballs, checkpoints, raw data, prepared data, and split files.

## Scope

- Collect safe Markdown evidence from `docs/`.
- Collect small imported artifact text files from `experiments/**/results_imported*/`.
- Generate a deterministic Markdown report.
- Write only to `docs/generated/` when an explicit output path is provided.
- Avoid external services, Modal, GPU, training, checkpoint loading, and tarball unpacking.

## Safety Rules

The packager refuses sources with checkpoint or archive suffixes such as `.pt`, `.ckpt`, `.safetensors`, `.bin`, `.tar.gz`, `.tgz`, and `.zip`. It also excludes raw, prepared, and split data paths.

## Example Commands

Dry-run source scan:

```powershell
.\.venv\Scripts\python.exe scripts\build_project_report_package.py
```

Write a report only when explicitly requested:

```powershell
.\.venv\Scripts\python.exe scripts\build_project_report_package.py --output docs\generated\project_report.md
```

## Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\build_project_report_package.py tests\test_project_report_packager.py
.\.venv\Scripts\python.exe scripts\build_project_report_package.py
.\.venv\Scripts\python.exe tests\test_project_report_packager.py
git diff --check
```

This branch is local-only and does not need a GPU or Modal gate. If a generated report is later committed, artifact hygiene should be run before commit.
