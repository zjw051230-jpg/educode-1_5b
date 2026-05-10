# W10.13 One-Step Smoke Review

## 1. Purpose
The purpose of this step is to:
- review whether W10.12 one-step smoke run reached its intended goal
- check that the implementation did not cross the boundary into multi-step training
- check that run artifacts were written correctly and remained ignored by Git
- solidify the Windows 10M smoke milestone
- decide whether the project can proceed to a minimal training loop

## 2. W10.12 Result Summary
- run_id: `20260511_024724_windows_cuda_one_step_smoke`
- device: `cuda`
- input_ids shape: `(4, 16)`
- target_ids shape: `(4, 16)`
- loss value: `8.964268`
- grad_norm: `3.601954`
- checkpoint generated: yes
- checkpoint reload parameters match: `True`
- metrics.jsonl exists: yes
- generation_samples.jsonl exists: yes
- summary.md exists: yes
- generated preview: `helloX`
- success: `True`

## 3. Pipeline Coverage
W10.12 covered:
- config loading
- config validation
- run setup
- run metadata
- config snapshot
- toy data
- ByteTokenizer
- sequence x/y construction
- tiny model forward
- next-token cross entropy loss
- backward
- optimizer step
- checkpoint save
- checkpoint reload
- generation
- metrics logging
- generation sample logging
- summary writing

## 4. Boundary Check
W10.12 did not do:
- no multi-step training loop
- no long training
- no evaluation loop
- no real dataset download
- no pretrained model download
- no MoE
- no alignment
- no RAG/Web UI
- no distributed training
- no Git-tracked checkpoint
- no Git-tracked generated run directory

## 5. Git Tracking Check
- generated run directories under `experiments/*/*/` are ignored
- checkpoint `.pt` files are ignored
- source code, docs, configs, and templates are tracked
- W10.12 run artifacts are local-only
- summary information is captured in `docs/w10_12_one_step_smoke.md` and this review document

## 6. Current Limitations
- current tokenizer path uses `ByteTokenizer`, while config declares BPE/8192
- current tiny model uses learned position embeddings, not RoPE
- current attention backend uses PyTorch SDPA, not FlashAttention-2
- current model is an 8M-ish tiny smoke model, not 10M exactly and not 1.5B
- current generation quality is meaningless because the model is untrained
- current data is toy corpus only
- current checkpoint is single-process, non-sharded

## 7. Why This Milestone Matters
- one-step smoke proves the core training control flow can execute once
- it reduces risk before writing a repeated training loop
- it proves CUDA, model, loss, optimizer, checkpoint, generation, and logging can interoperate
- it is the smallest credible bridge toward A100/B200 scaling

## 8. Decision
- W10.12 one-step smoke is accepted
- Windows 4060 Ti is validated for engineering smoke tests
- project can proceed to W11 minimal training loop plan
- do not jump directly to long training
- next should be a carefully bounded minimal training loop

## 9. Recommended Next Step
Suggested next step:
- W11: minimal training loop plan

W11 should still start with a plan instead of directly writing the full loop. The W11 plan should define:
- max_steps small, e.g. 10 or 20
- log every step
- save checkpoint at end
- run generation at end
- no real dataset yet
- no A100/B200 yet
- no large model yet
