# A1 A100 Smoke Milestone Report

## 1. Purpose
记录 A100 80GB 单卡 scale smoke 结果。

## 2. Hardware
- NVIDIA A100 80GB PCIe
- torch 2.5.1+cu121
- torch CUDA 12.1

## 3. Completed Milestones
- 100M/134M forward-loss passed
- 100M/134M 10-step training smoke passed
- 100M/134M 100-step training smoke passed
- 300M/405M forward-loss passed
- 300M/405M 10-step training smoke passed
- 300M/405M 100-step training smoke passed
- 2.15B forward-loss passed
- 2.15B 1-step checkpoint smoke passed
- 2.15B seq256 20-step no-checkpoint optimizer profile passed
- 2.15B seq512 50-step no-checkpoint optimizer profile passed

## 4. Key Result
- parameters: 2,153,474,048
- sequence_length: 512
- steps: 50
- batch_size: 1
- first_loss: 7.215097904205322
- final_loss: 0.5468654036521912
- loss_all_finite: true
- grad_norm_all_finite: true
- mean_step_time_seconds: 0.5853188800811767
- elapsed_seconds: 29.381282806396484
- max_memory_allocated_gb: 40.13074207305908
- max_memory_reserved_gb: 41.66796875
- checkpoint_saved: false

## 5. Interpretation
- A100 single-GPU path validated up to 2.15B-scale optimizer profiling.
- This validates engineering pipeline and scaling feasibility.
- This is not full pretraining.
- Current corpus is tiny project-authored synthetic seed corpus.
- Do not claim model quality or generalization.

## 6. What This Enables
- future A100 100M/300M experiments
- 2.15B-scale preflight
- larger-corpus training after data expansion
- resume/project showcase as systems engineering milestone

## 7. Next Bottleneck
- GPU feasibility is no longer the main blocker.
- next bottleneck is data scale and tokenizer quality.
- need larger permitted corpus before meaningful longer training.

## 8. Next Step
D1: expand permitted corpus plan.
