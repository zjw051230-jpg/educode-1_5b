# Tokenizer Training Feasibility

This branch adds local tokenizer-training feasibility scaffolding. It does not train a real tokenizer and does not process a real dataset.

## Scope

- Tokenizer training config schema for future byte-level BPE planning.
- Required special-token policy for `<|endoftext|>`, `<|pad|>`, and `<|unk|>`.
- Tiny byte tokenizer toy implementation for local encode/decode sanity checks.
- Vocab statistics helper.
- Local validator using a tiny in-memory fixture.

## Safety Boundaries

- No raw data or prepared data processing.
- No real tokenizer training.
- No GPU, Modal, training, profiling, or preflight.
- The toy tokenizer is a feasibility fixture, not a production tokenizer.

## Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\tokenizer_training.py scripts\validate_tokenizer_training_config.py tests\test_tokenizer_training_config.py
.\.venv\Scripts\python.exe scripts\validate_tokenizer_training_config.py
.\.venv\Scripts\python.exe tests\test_tokenizer_training_config.py
git diff --check
```

Future real tokenizer work requires corpus provenance review, data-size bounds, artifact hygiene, and explicit approval before processing large raw text.
