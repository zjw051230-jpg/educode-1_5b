# Experiment Matrix

This matrix summarizes completed small imported artifacts and future candidates. It does not read result tarballs, run Modal, use GPU, or start training.

- Matrix status: `passed`
- Blocker count: `0`
- Completed experiments: `4`
- Planned candidates: `7`
- Recommended next: `mvp31_seq1024_bs8_memory_preflight`

| Experiment | Status | Shape | Key metrics | Gate |
| --- | --- | --- | --- | --- |
| `mvp27_5gb_3000step_training` | completed | steps=3000 | val_loss=8.341638 | none |
| `mvp28_seq512_sdpa_50step_profile` | completed | steps=50, sdpa | 44100.712407 tok/s, 0.371513s step, 8.416016 GiB reserved, val_loss=8.897261 | none |
| `mvp29_seq1024_bs4_10step_memory_preflight` | completed | ctx=1024, bs=4, steps=10, sdpa | 27151.11506 tok/s, 0.603437s step, 8.412109 GiB reserved, val_loss=9.044042 | none |
| `mvp30_seq1024_bs4_50step_sdpa_profile` | completed | ctx=1024, bs=4, steps=50, sdpa | 41430.475003 tok/s, 0.395458s step, 8.412109 GiB reserved, val_loss=9.930368 | none |
| `mvp31_seq1024_bs8_memory_preflight` | planned_requires_gpu | memory_preflight | n/a | required before A100 run |
| `naive_attention_baseline` | planned_local_then_gpu | attention_backend | n/a | GPU confirmation needed only for measured profiling |
| `flashattention_feasibility` | planned_local_feasibility | attention_backend | n/a | GPU confirmation needed only after dependency feasibility passes |
| `adamw_vs_muon_optimizer_prep` | planned_local_prep | optimizer | n/a | GPU confirmation needed for future training comparison |
| `moe_routing_prep` | planned_local_prep | moe | n/a | GPU confirmation needed only after MoE config is explicitly enabled |
| `rope_long_context_prep` | planned_local_prep | position_encoding | n/a | GPU confirmation needed for future long-context profiling |
| `mvp_future_5gb_5000step_continuation` | planned_requires_gpu | training | n/a | required before any longer A100 training |
