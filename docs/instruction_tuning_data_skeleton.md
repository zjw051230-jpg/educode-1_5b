# Instruction Tuning Data Skeleton

This branch adds a local schema and validator for future instruction-tuning and SFT data. It does not train a model, load a checkpoint, or process a real dataset.

## Scope

- Chat-style sample schema with `id` and `messages`.
- Supported roles: `system`, `user`, and `assistant`.
- Validation for non-empty messages, required user and assistant turns, assistant-final samples, and estimated token limits.
- Prompt/completion conversion for simple SFT-style downstream tooling.
- JSONL loader for local small fixtures.

## Safety Boundaries

- No GPU, Modal, or training.
- No raw dataset is required.
- No prepared data, checkpoint, or tarball is read or committed.
- Token counts are heuristic sanity estimates, not tokenizer-grounded measurements.

## Example Commands

Synthetic local validation:

```powershell
.\.venv\Scripts\python.exe scripts\validate_instruction_dataset.py
```

Validate a small local JSONL fixture:

```powershell
.\.venv\Scripts\python.exe scripts\validate_instruction_dataset.py --input path\to\samples.jsonl
```

## Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\instruction_data.py scripts\validate_instruction_dataset.py tests\test_instruction_data.py
.\.venv\Scripts\python.exe scripts\validate_instruction_dataset.py
.\.venv\Scripts\python.exe tests\test_instruction_data.py
git diff --check
```

Future real SFT runs require a separate data review, tokenization audit, training config, and explicit GPU/Modal cost confirmation.
