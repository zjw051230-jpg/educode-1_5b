# MVP-10 Training Logging Cleanup Plan

## 1. Current Logging / Reporting Gaps
Observed gaps from the imported MVP-8 and MVP-9 results:
- `validation_metrics.jsonl` was not written as a standalone artifact
- MVP-9 `checkpoint_path` points to the `10step_execute` directory
- `scheduler_config_present_but_not_applied=true`
- the MVP-9 `run_id` still contains the `10step_smoke` phrase even though the run used `100` steps

## 2. Why Cleanup Is Needed
These issues do not invalidate the bounded A800 runs, but they make later reviews noisier than necessary.

Before the next GPU run, the project should reduce avoidable ambiguity in:
- artifact names
- output paths
- config-to-runtime traceability
- post-run validation coverage

## 3. Recommended Cleanup Before the Next GPU Run
Recommended cleanup items:
- write standalone `validation_metrics.jsonl`
- derive `checkpoint_path` from the current config `output_dir` so it cannot point at the wrong run directory
- make `run_id` reflect `max_steps` accurately
- either apply the scheduler or remove the scheduler claim from the reviewed config/reporting path
- add post-run artifact validation so summary fields are checked against the actual run directory contents

## 4. Suggested Validation Focus
For the next reviewed GPU run, post-run validation should explicitly confirm:
- summary files exist
- metrics row count matches `max_steps`
- validation row count matches the expected eval schedule
- standalone validation metrics exist when promised
- checkpoint path points into the current run directory
- checkpoint reload verification result is recorded
- run naming matches the configured step count and output path

## 5. Scope Boundary
This MVP-10 cleanup plan does not itself change the training code.
It records the minimum logging and artifact-quality improvements recommended before the next GPU execution stage.
