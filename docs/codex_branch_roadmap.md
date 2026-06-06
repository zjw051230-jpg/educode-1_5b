# Codex Branch Review Roadmap

This roadmap is a review guide for the NotebookLM-derived technical branches. It is not an execution plan for GPU work.

| Branch | Primary Review Question | Local Merge Readiness | Future Cost Gate |
| --- | --- | --- | --- |
| `docs/notebooklm-tech-synthesis` | Does the roadmap accurately separate local code from GPU claims? | Docs-only, low risk | None |
| `feature/inference-kv-cache-harness-v2` | Are sampling, KV cache, and speculative interfaces local-only and checkpoint-safe? | Merge after tests pass | Real checkpoint inference |
| `feature/attention-backend-abstraction-v2` | Does SDPA remain default and unchanged for existing configs? | Merge after synthetic SDPA/naive parity tests | Backend profiling |
| `feature/muon-experimental-optimizer` | Is Muon explicitly acknowledged and unable to run accidentally? | Merge after CPU optimizer tests | Optimizer training comparison |
| `feature/moe-routing-skeleton-v2` | Is MoE fully disabled for dense baseline configs? | Merge after routing/loss tests | MoE training or profiling |
| `feature/rope-position-encoding-v2` | Is learned position encoding still the default and checkpoint-safe? | Merge after helper/schema tests | Long-context profiling |

## Review Checklist

- Confirm each branch only touches its own technical lane.
- Confirm `docs/change_log.md` records validation and no-cost status.
- Confirm no branch commits tarballs, checkpoints, raw data, prepared data, or large artifacts.
- Confirm future GPU/Modal commands appear only as documented gates.
- Confirm claims are limited to local synthetic validation unless a real imported artifact exists.

## Recommended First Merges

1. `docs/notebooklm-tech-synthesis`
2. `feature/inference-kv-cache-harness-v2`
3. `feature/attention-backend-abstraction-v2`

These provide planning, local inference scaffolding, and backend structure without changing optimizer or architecture defaults.

## Branches Requiring Extra Review

- `feature/muon-experimental-optimizer`: review optimizer math and parameter grouping before any training use.
- `feature/moe-routing-skeleton-v2`: review architecture boundaries and config guards before merging.
- `feature/rope-position-encoding-v2`: review checkpoint compatibility before wiring into the model.
