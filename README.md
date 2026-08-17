# EduCode Training Lab

A small PyTorch language-model training project inspired by Stanford CS336. The emphasis is on reproducible systems work: tokenization, data loading, model code, validation checks, Modal/A100 runs, artifact validation, and lightweight profiling.

## Current results

- A 5 GB FineWeb-Edu run continued to improve between 1,000 and 3,000 steps.
- The 3,000-step run used 15 unique validation documents without prefix-only leakage risk.
- SDPA profiling reached about 44.1k tokens/s at sequence length 512, batch size 8.
- Sequence length 1024, batch size 4 reached about 41.4k tokens/s without OOM.

These are training-system measurements rather than a model-quality benchmark. Raw datasets, checkpoints, and result archives are kept outside Git.

## Layout

- `src/`: tokenizer, data, model, and training code.
- `configs/`: experiment configuration.
- `scripts/`: data preparation, training, and profiling entry points.
- `tests/`: unit and integration checks.
- `docs/experiment_index.md`: index of completed runs and notes.

## Notes and reports

- [Project asset summary](docs/project_asset_summary.md)
- [Experiment index](docs/experiment_index.md)
- [5 GB / 3,000-step analysis](docs/mvp_27_a_5gb_3000step_result_analysis.md)
- [seq512 SDPA profile](docs/mvp_28_a_sdpa_profile_result_analysis.md)
- [seq1024 memory preflight](docs/mvp_29_a_seq1024_memory_preflight_result_analysis.md)
- [seq1024 SDPA profile](docs/mvp_30_a_seq1024_sdpa_profile_result_analysis.md)

GPU runs can incur cost, so training and profiling commands should be reviewed before they are submitted.
