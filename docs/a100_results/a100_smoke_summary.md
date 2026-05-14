# A100 Smoke Summary

## Machine

- GPU: NVIDIA A100 80GB PCIe
- torch: 2.5.1+cu121
- torch CUDA: 12.1
- tokenizers: 0.22.2

## Summary JSON Runs

### 20260514_145930_a100_100m_10_step_smoke
- parameter_count: 134339328
- max_steps: 10
- batch_size: 8
- sequence_length: 397
- first_train_loss: 7.222545623779297
- final_train_loss: 4.500910758972168
- final_val_loss: 7.19232702255249
- train_loss_all_finite: True
- val_loss_all_finite: True
- checkpoint_reload_match: True
- elapsed_seconds: 8.545064926147461
- max_memory_allocated_gb: 5.018661022186279
- max_memory_reserved_gb: 5.302734375

### 20260514_150020_a100_100m_100_step_smoke
- parameter_count: 134339328
- max_steps: 100
- batch_size: 8
- sequence_length: 397
- first_train_loss: 7.224188327789307
- final_train_loss: 0.5201810002326965
- final_val_loss: 7.30624532699585
- train_loss_all_finite: True
- val_loss_all_finite: True
- checkpoint_reload_match: True
- elapsed_seconds: 25.673953533172607
- max_memory_allocated_gb: 5.018661022186279
- max_memory_reserved_gb: 5.302734375

### 20260514_150909_a100_300m_10_step_smoke
- parameter_count: 405632000
- max_steps: 10
- batch_size: 4
- sequence_length: 397
- first_train_loss: 7.198070526123047
- final_train_loss: 3.1536693572998047
- final_val_loss: 7.092921257019043
- train_loss_all_finite: True
- val_loss_all_finite: True
- checkpoint_reload_match: True
- elapsed_seconds: 19.49398136138916
- max_memory_allocated_gb: 12.18392562866211
- max_memory_reserved_gb: 13.5546875

### 20260514_151006_a100_300m_100_step_smoke
- parameter_count: 405632000
- max_steps: 100
- batch_size: 4
- sequence_length: 397
- first_train_loss: 7.252823352813721
- final_train_loss: 0.2099585384130478
- final_val_loss: 7.515316486358643
- train_loss_all_finite: True
- val_loss_all_finite: True
- checkpoint_reload_match: True
- elapsed_seconds: 46.38789129257202
- max_memory_allocated_gb: 12.18392562866211
- max_memory_reserved_gb: 13.5390625

### 20260514_151256_a100_1_5b_1_step_smoke
- parameter_count: 2153474048
- batch_size: 1
- sequence_length: 128
- loss: 7.188198566436768
- grad_norm: 9.072857856750488
- checkpoint_exists: True
- elapsed_seconds: 77.53780889511108
- max_memory_allocated_gb: 40.12801170349121
- max_memory_reserved_gb: 40.48828125

### 20260514_152102_a100_2_15b_3_step_no_ckpt_profile
- parameter_count: 2153474048
- max_steps: 3
- batch_size: 1
- sequence_length: 128
- first_loss: 7.322863578796387
- final_loss: 7.901147365570068
- loss_all_finite: True
- grad_norm_all_finite: True
- checkpoint_saved: False
- elapsed_seconds: 1.9878368377685547
- mean_step_time_seconds: 0.6596700350443522
- max_memory_allocated_gb: 40.12801170349121
- max_memory_reserved_gb: 40.490234375

### 20260514_152310_a100_2_15b_20_step_seq256_no_ckpt_profile
- parameter_count: 2153474048
- max_steps: 20
- batch_size: 1
- sequence_length: 256
- first_loss: 7.213736534118652
- final_loss: 2.376305341720581
- min_loss: 1.1478897333145142
- max_loss: 7.213736534118652
- loss_all_finite: True
- grad_norm_all_finite: True
- checkpoint_saved: False
- elapsed_seconds: 8.318289041519165
- mean_step_time_seconds: 0.41333780288696287
- max_memory_allocated_gb: 40.130093574523926
- max_memory_reserved_gb: 40.65234375

### 20260514_152517_a100_2_15b_10_step_seq512_no_ckpt_profile
- parameter_count: 2153474048
- max_steps: 10
- batch_size: 1
- sequence_length: 512
- first_loss: 7.206127166748047
- final_loss: 2.6245694160461426
- min_loss: 2.6245694160461426
- max_loss: 7.519742488861084
- loss_all_finite: True
- grad_norm_all_finite: True
- checkpoint_saved: False
- elapsed_seconds: 6.680814743041992
- mean_step_time_seconds: 0.6659234046936036
- max_memory_allocated_gb: 40.13074207305908
- max_memory_reserved_gb: 41.66796875

### 20260514_152710_a100_2_15b_50_step_seq512_no_ckpt_profile
- parameter_count: 2153474048
- max_steps: 50
- batch_size: 1
- sequence_length: 512
- first_loss: 7.215097904205322
- final_loss: 0.5468654036521912
- min_loss: 0.5468654036521912
- max_loss: 7.524284839630127
- loss_all_finite: True
- grad_norm_all_finite: True
- checkpoint_saved: False
- elapsed_seconds: 29.381282806396484
- mean_step_time_seconds: 0.5853188800811767
- max_memory_allocated_gb: 40.13074207305908
- max_memory_reserved_gb: 41.66796875

## Additional Forward/Loss Results From Terminal

- 100M/134M forward-loss: passed; loss=7.265879; max_memory_allocated_gb=0.7311
- 300M/405M forward-loss: passed; loss=7.195046; max_memory_allocated_gb=1.6675
- 1.5B/2.15B forward-loss: passed; loss=7.265502; max_memory_allocated_gb=8.0690

## Key Result

- 2.15B seq512 50-step no-checkpoint profile passed.
- loss: 7.215097904205322 -> 0.5468654036521912
- mean_step_time_seconds: 0.5853188800811767
- max_memory_allocated_gb: 40.13074207305908
- checkpoint_saved: false

## Decision

- A100 single-GPU path is accepted.
- 100M, 300M, and 2.15B-scale smoke milestones passed.
- 2.15B seq512 50-step optimizer profile passed.
- Do not continue long training on the current tiny synthetic corpus.
- Next engineering step: transfer small results locally and write an A100 milestone report.