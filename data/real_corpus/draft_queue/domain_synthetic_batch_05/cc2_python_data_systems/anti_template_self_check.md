# Anti-template Self Check

## How this batch avoids the batch_04 failure mode
- The batch does not use one repeated markdown skeleton. Writing forms rotate by 20-file blocks and neighboring files alternate internal shapes.
- Each file was assigned a unique learning objective before content rendering, so the body had to answer a different instructional question.
- Every file contains a concrete anchor such as a broken JSONL row, schema mismatch, tensor shape trace, config snippet, pseudo-run log, or before/after comparison.
- Python files implement topic-specific helpers and validation logic instead of generic summary emitters.

## Diversity controls
- Five topic subdirectories: jsonl_repair, schema_validation, batching_debug, config_checks, metrics_diagnostics.
- Five writing-form blocks: explainer note / mini lab / debugging diary / failure analysis / checklist / config review / Q&A / code walkthrough / comparison table / metric interpretation.
- Multiple concrete anchor families were intentionally mixed across neighboring topics to prevent phrase substitution from carrying the file.

## Known near-collisions
- Several files operate on related repair themes such as split leakage or schema drift, but each one differs by artifact type, teaching objective, and anchor shape.
- Metrics files share the same domain vocabulary, but some are metric-interpretation notes while others are executable row validators or summary renderers.

## Self-critique
- The metadata header is intentionally uniform because the batch requires fixed safety markers.
- Some python files share utility imports and ReviewIssue scaffolding, but the main function and review target are specific to each topic and subdirectory.
