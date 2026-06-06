# Next Experiment Candidates

This ranking is a planning aid only. It does not authorize any Modal, GPU, or training run.

| rank | candidate | status | requires Modal/GPU | why | next step |
| --- | --- | --- | --- | --- | --- |
| 1 | seq1024_batch_size_8_memory_preflight | planned_cost_gate_required | true | Tests the main unresolved memory question after seq1024 batch_size=4 passed 50-step profiling. | Write a plan/config gate first; do not execute without explicit cost approval. |
| 2 | naive_attention_baseline | planned_local_prep_first | false | Needed before claiming SDPA is faster than a manual baseline. | Prepare backend abstraction and small synthetic CPU tests. |
| 3 | flashattention_feasibility | planned_local_prep_first | false | Clarifies dependency and optional backend boundaries before any GPU comparison. | Add availability guard; do not install or require flash_attn in this step. |
| 4 | 5gb_5000step_training | deferred_cost_gate_required | true | Could extend quality trend, but profiling and memory questions should be closed first. | Plan only after explicit cost gate and route decision. |
| 5 | adamw_vs_muon | planned_local_prep_first | false | Requires optimizer registry and guarded Muon implementation before any training comparison. | Prepare optimizer registry; do not run training in this phase. |

Recommended next branch: `feature/attention-backend-prep` for backend abstraction and local-only checks.
