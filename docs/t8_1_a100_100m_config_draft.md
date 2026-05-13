# T8.1 A100 100M Config Draft

## 1. Purpose
The purpose of T8.1 is to create a draft A100 100M-class config and a read-only inspection script before any A100 environment preflight or run attempt.

This step is config and inspection only.
It does not run training, does not use A100 hardware, and does not modify model code.

## 2. Files Added or Updated
- `configs/a100/educode_100m_a100_draft.json`
- `scripts/inspect_a100_100m_config.py`
- `docs/t8_1_a100_100m_config_draft.md`
- `README.md`
- `docs/experiment_index.md`

## 3. Draft Config Summary
Draft config details:
- `status`: `draft_not_run`
- `run.run_name`: `a100_educode_100m_draft`
- `hardware.target`: `a100_cuda`
- `hardware.gpu`: `A100 40GB or 80GB`
- `tokenizer.type`: `bpe`
- `tokenizer.vocab_size`: `1174`
- `tokenizer.path`: `tokenizers/educode_bpe_8k/tokenizer.json`
- `model.context_length`: `512`
- `model.num_layers`: `14`
- `model.d_model`: `768`
- `model.num_heads`: `12`
- `model.d_ff`: `3072`
- `profiling.attention_backend`: `sdpa`

Inspection-script parameter estimate under the current `TinyDecoderOnlyTransformer` parameterization:
- estimated total parameters: `134339328` (`~134.34M`)
- the 14-layer shape is a deliberate T8.1 adjustment from the earlier 12-layer proposal so the current repo implementation lands in the intended 100M-class range

Interpretation:
- this is a 100M-class draft, not a completed training result
- the draft keeps the current observed tokenizer vocab size `1174`
- the current vocab size reflects the current `educode_bpe_8k` tokenizer artifact trained on the synthetic seed corpus, not a future larger-corpus tokenizer target
- the parameter estimate reflects the current `TinyDecoderOnlyTransformer` implementation, including learned position embeddings and an untied output head
- `model.position_encoding = rope` is kept as a forward-looking A100 draft field; T8.1 does not claim that the current local runtime already executes RoPE
- a future permitted larger corpus may require tokenizer retraining and a vocab-size update before any real A100 training claim

## 4. Inspection Result
Observed from `scripts/inspect_a100_100m_config.py`:
- config loaded successfully
- tokenizer artifact loaded successfully
- loaded tokenizer vocab size matched the config value `1174`
- config validation passed under the current repo validator
- no training or profiling run was executed

## 5. Why This Matters
This matters because it:
- turns the T8 A100 planning step into a concrete repo-tracked draft config
- keeps the current tokenizer reality explicit instead of pretending an 8k or 16k vocab already exists here
- creates a safe handoff point for future A100 preflight, forward/loss smoke, and profiling milestones

## 6. What It Does Not Do
This step does not:
- run any model training
- use A100 hardware
- claim model quality
- retrain the tokenizer
- upgrade the corpus
- modify the model implementation

## 7. Next Step
Recommended next step:
- T8.2 A100 environment preflight checklist

Reason:
- the config draft now exists and passes validation
- the next remaining uncertainty is environment readiness, not config structure
