# Model Compression / Distillation Skeleton

This branch adds local distillation and compression feasibility scaffolding. It is designed for future teacher-student experiments without loading a real teacher checkpoint or mutating model weights.

## Scope

- Distillation config schema with temperature and alpha validation.
- Pure-Python KL divergence distillation loss for synthetic logits.
- Teacher logits provider interface placeholder.
- Compression plan metadata for pruning, distillation-only, and quantization-audit directions.
- Local validator that runs on synthetic logits only.

## Safety Boundaries

- No teacher checkpoint is loaded.
- No student checkpoint is loaded.
- No GPU, Modal, training, profiling, or preflight is run.
- Compression plans are metadata reports only; they do not mutate model weights.

## Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\distillation.py src\educode\compression.py scripts\validate_distillation_config.py tests\test_distillation_loss.py
.\.venv\Scripts\python.exe scripts\validate_distillation_config.py
.\.venv\Scripts\python.exe tests\test_distillation_loss.py
git diff --check
```

Future real distillation requires an explicit teacher checkpoint policy, GPU/Modal cost confirmation, data split review, and artifact hygiene checks.
