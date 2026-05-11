# T1 Formal Training Roadmap

## 1. Purpose
The purpose of T1 is to:
- transition from toy-data pipeline validation to formal training preparation
- define the real training route for EduCode-1.5B
- stop treating toy runs as final outcomes
- plan the stage path from a small real-data run to A100 profiling and then B200 1.5B work
- keep this step planning-only, with no data download and no training execution

## 2. Current Baseline
The project has already completed:
- modular project skeleton
- config loader / validator
- ByteTokenizer temporary path
- toy corpus pipeline
- sequence x/y dataset
- tiny decoder-only Transformer
- next-token loss
- optimizer step
- checkpoint save/load
- generation
- run logging
- one-step smoke
- 10-step toy training
- 50-step toy training
- resume-ready README, report, and demo packaging

These milestones prove that the pipeline can run end to end.
They do not yet constitute formal pretraining.
The current model is not 1.5B.
The current data is not a formal training corpus.
The current tokenizer is not the final BPE path.

## 3. Formal Training Definition
A formal training experiment should include at least:
- a real dataset or curated real text/code corpus
- a BPE tokenizer trained or selected consistently
- a train/validation split
- validation loss
- repeatable config
- checkpoint resume
- a training report
- a loss curve
- generation samples
- a clear hardware target

Important boundaries:
- the toy corpus does not count as formal training
- the 50-step toy run does not count as formal training
- a run without validation loss is not a complete training experiment

## 4. Project Theme
Formal project theme:

EduCode-1.5B: a CS / ML / Code learning-oriented dense Transformer language model.

Target corpus directions:
- CS course notes
- machine learning explanations
- Python/code snippets
- algorithm descriptions
- math-heavy technical text
- possibly curated open educational text

This project does not currently target:
- general web-scale pretraining
- copyrighted or private course material without permission
- alignment / RLHF / DPO
- MoE
- a RAG product
- a web UI

## 5. Stage Plan
### T2 BPE Tokenizer Plan
Goals:
- move from ByteTokenizer to BPE
- choose vocab_size such as 8k / 16k / 32k
- define special tokens
- define tokenizer artifacts
- ensure `model.vocab_size` matches `tokenizer.vocab_size`

### T3 Small Real Dataset Plan
Goals:
- choose a small real corpus
- define data sources
- define license and safety notes
- define cleaning rules
- define a train/val split

### T4 Real Dataset Pipeline
Goals:
- text file reading
- tokenization
- packed sequence dataset
- train/val split
- no huge data yet

### T5 Validation Loop
Goals:
- train loss
- val loss
- eval interval
- no generation-quality claims yet

### T6 Scheduler + Resume Plan
Goals:
- learning rate scheduler
- checkpoint resume
- config snapshot
- metrics summary

### T7 Windows Small Real-Data Training
Goals:
- 10M-40M model
- Windows RTX 4060 Ti
- short real-data training
- report a loss curve
- no 1.5B claim

### T8 A100 100M/300M Profiling
Goals:
- larger dense model
- tokens/sec
- memory
- SDPA / optional FlashAttention-2 if installed
- profiling report

### T9 B200 1.5B Preflight
Goals:
- final config
- token budget
- data readiness
- checkpoint storage
- resume strategy
- cost estimate

### T10 B200 1.5B Training
Goals:
- actual 1.5B dense Transformer run
- only after T2-T9 pass
- no premature claim before the run completes

## 6. Dataset Candidate Categories
### Open educational CS/ML text
- pros: aligned with project theme and easy to explain
- risks: uneven style and varying quality
- license concern: must verify redistribution and training permissibility
- expected use: foundation corpus for early small real-data runs

### Permissively licensed code snippets
- pros: matches code-oriented learning goals
- risks: fragmented context and noisy formatting
- license concern: must stay within permissive licenses
- expected use: supplement explanatory text with short code examples

### Synthetic explanation data generated later if allowed
- pros: controllable style and domain focus
- risks: model-generated artifacts may amplify repetition or factual drift
- license concern: depends on the generator and prompt ownership rules
- expected use: optional augmentation, not initial core training data

### Small manually curated local corpus
- pros: high control, fast inspection, and clear scope
- risks: small scale and possible author bias
- license concern: easiest if fully user-created
- expected use: first formal small-data Windows training target

### Public domain / permissive documentation
- pros: safe to cite and easier to share in reports
- risks: may be structurally inconsistent across sources
- license concern: still must verify exact terms and attribution needs
- expected use: clean educational base text for tokenizer and dataset tests

### User-created notes
- pros: strongest topic alignment and simplest provenance
- risks: limited volume
- license concern: easiest if entirely authored by the user
- expected use: seed corpus or validation subset for early experiments

## 7. Tokenizer Plan
Formal training should not stay on ByteTokenizer.
The current ByteTokenizer path is temporary.
Formal training should use BPE.
The first BPE target vocab_size can be `8192` for a Windows small run.
Later runs can target `32000` for larger experiments.

Special tokens should include:
- `<pad>`
- `<bos>`
- `<eos>`
- `<unk>`

Tokenizer artifacts should be saved under:
- `tokenizers/`

Tokenizer config should be referenced from the training config.
`model.vocab_size` must always match `tokenizer.vocab_size`.

## 8. First Real Training Target
The first formal real training target should be:
- hardware: Windows RTX 4060 Ti 16GB
- model size: 10M-40M
- tokenizer: BPE 8k
- context length: 128 or 256
- dataset: small curated CS/code text
- max tokens: intentionally small
- goal: prove the real-data training pipeline

Success criteria:
- train loss finite
- val loss finite
- checkpoint resume works
- summary and report are generated

## 9. What Not To Claim Yet
Do not claim yet:
- trained a 1.5B model
- trained a production LLM
- trained on a large-scale dataset
- achieved meaningful generation quality
- completed alignment / RLHF
- completed A100/B200 scaling
- implemented MoE

## 10. Resume Upgrade Path
Current resume-safe wording:
- pipeline validated on toy data

After T7, acceptable wording can become:
- pretrained a small dense Transformer on a curated CS/code corpus

After T8, acceptable wording can become:
- profiled 100M/300M dense Transformer experiments on A100

Only after T10 can the project claim:
- trained a 1.5B dense Transformer model

## 11. Immediate Next Step
Recommended next step:
- T2: BPE Tokenizer Plan

T2 should remain planning-first, not code-heavy immediately.
T2 should define:
- whether to implement BPE from scratch or use an existing tokenizer library
- vocab size
- special tokens
- artifact format
- encode/decode tests
- integration with model config
