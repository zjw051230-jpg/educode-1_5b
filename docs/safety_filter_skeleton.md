# Safety Filter Skeleton

This branch adds a local rule-based safety/content filter skeleton for future data filtering and generated-output checks. It does not use an external safety model or API.

## Scope

- Rule-based regex safety patterns.
- Severity validation.
- Text-level safety result with matched pattern names.
- Filtering report with safe/unsafe/match counts.
- Local validator with synthetic unsafe fixtures.

## Safety Boundaries

- No external API.
- No network calls.
- No model checkpoint or safety model.
- No GPU, Modal, training, profiling, or preflight.
- Patterns are synthetic guardrail scaffolding, not a production safety policy.

## Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\safety_filter.py scripts\validate_safety_filter.py tests\test_safety_filter.py
.\.venv\Scripts\python.exe scripts\validate_safety_filter.py
.\.venv\Scripts\python.exe tests\test_safety_filter.py
git diff --check
```

Future real safety work requires policy review, false-positive/false-negative evaluation, data provenance checks, and a clear boundary between data filtering and generation-time moderation.
