# Checkpoint And Artifact Hygiene

This branch adds a standalone hygiene checker for commit review. It is meant to catch accidental staging of result tarballs, checkpoints, raw data, prepared data, and large experiment artifacts before they reach Git.

## Scope

- Checks staged files by default.
- Blocks checkpoint-like suffixes such as `.pt`, `.pth`, `.ckpt`, `.safetensors`, `.bin`, `.tar.gz`, and `.tgz`.
- Blocks raw, prepared, and split data paths under `data/`.
- Allows small imported result text artifacts such as JSON, JSONL, Markdown, and text files.
- Flags large files under `experiments/`.

## Non-Goals

- The checker does not delete files.
- The checker does not install a Git hook automatically.
- The checker does not run Modal, GPU jobs, training, profiling, or preflight.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\check_artifact_hygiene.py tests\test_artifact_hygiene.py
.\.venv\Scripts\python.exe scripts\check_artifact_hygiene.py
.\.venv\Scripts\python.exe tests\test_artifact_hygiene.py
git diff --check
```

## Future Gate

Future GPU or Modal result-import branches should run this checker before commit. If a result tarball or checkpoint is staged, the branch should stop before commit and require cleanup or user confirmation.
