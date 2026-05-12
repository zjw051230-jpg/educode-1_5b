# T2 BPE Tokenizer Plan

## 1. Purpose
The purpose of T2 is to:
- design the BPE tokenizer route for the formal training line
- migrate from the current temporary ByteTokenizer path to a formal BPE tokenizer
- ensure `tokenizer.vocab_size` stays aligned with `model.vocab_size`
- prepare for T3 small real-data training
- keep this step planning-only, with no tokenizer implementation and no tokenizer training

## 2. Current Tokenizer Baseline
Current tokenizer baseline:
- the project already has `src/educode/byte_tokenizer.py`
- `ByteTokenizer` uses UTF-8 bytes
- `vocab_size = 256`
- it has already been used for toy smoke, one-step smoke, the 10-step toy loop, and the 50-step toy loop
- `ByteTokenizer` proved that the pipeline can run end to end
- it is not the formal training tokenizer
- the current config declares `tokenizer.type = bpe` and `tokenizer.vocab_size = 8192`, while the smoke path actually uses `ByteTokenizer`
- that mismatch was acceptable during toy smoke work, but it must be resolved before formal training

## 3. Why BPE Is Needed
BPE is needed because:
- a byte-level tokenizer tends to produce overly long sequences and lower training efficiency
- BPE can compress common subwords, code tokens, and English fragments
- BPE can still preserve fallback behavior for unknown text patterns
- BPE is a better fit for CS / ML / code educational corpora
- BPE vocab size can align directly with the model embedding and `lm_head`

## 4. Implementation Strategy Decision
Recommended decision:

The first formal training tokenizer should not start with a fully self-implemented BPE trainer.
The engineering line should prioritize a mature tokenizer library, such as Hugging Face `tokenizers` or `sentencepiece`.

Why this is the recommended first move:
- the current goal is to reach formal training sooner
- implementing a full BPE trainer from scratch would slow the engineering line
- the CS336 learning line can still implement BPE from scratch later if desired
- the Windows engineering line should optimize for stability, reproducibility, and training readiness

Future flexibility remains:
- the learning line can still implement BPE from scratch later
- the engineering line can start with a library tokenizer first
- a future self-implemented tokenizer can replace the library path if needed

## 5. Candidate Libraries
### Option A: Hugging Face tokenizers
Pros:
- fast
- supports BPE
- clear artifacts
- strong Python ecosystem fit
- compatible with later HF dataset and tooling choices

Risks:
- must verify whether `tokenizers` is already installed
- if not installed, package installation would need separate approval later

### Option B: sentencepiece
Pros:
- stable
- widely used for LLM tokenizers
- supports BPE and unigram models

Risks:
- current environment reports have not confirmed `sentencepiece` availability
- Windows installation may require extra handling later

### Option C: implement BPE from scratch
Pros:
- high learning value
- complete tokenizer understanding

Risks:
- higher engineering cost
- easier to introduce bugs
- not a good fit for the current goal of entering formal training quickly

Conclusion:
- T2 recommends Hugging Face `tokenizers` as the first choice
- if `tokenizers` is unavailable, T2.1 should only check the environment first
- any package installation still requires separate approval and is not part of T2

## 6. First Formal Tokenizer Target
The first formal tokenizer target should be:
- name: `educode_bpe_8k`
- type: `BPE`
- vocab_size: `8192`
- target hardware: Windows RTX 4060 Ti small run
- target use: T7 Windows small real-data training
- corpus: small curated CS / ML / code text
- special tokens:
  - `<pad>`
  - `<bos>`
  - `<eos>`
  - `<unk>`

Why this target makes sense:
- `8192` is a practical first size for Windows small-scale experiments
- later A100/B200 stages can move to `16000` or `32000`
- the 1.5B target is more likely to use `32000`

## 7. Tokenizer Artifacts
Recommended save path:

`tokenizers/educode_bpe_8k/`

Expected artifacts:
- `tokenizer.json`
- `vocab.json` or equivalent
- `merges.txt` or equivalent
- `tokenizer_config.json`
- `special_tokens_map.json`
- `README.md`

Artifact policy:
- tokenizer artifacts can be committed if they stay small and do not expose private data
- if a tokenizer is trained on private or copyrighted corpus material, artifact review must be cautious
- the tokenizer training corpus itself does not need to be committed to Git

## 8. Config Alignment Rules
Formal alignment rules:
- `tokenizer.type` must be `"bpe"`
- `tokenizer.vocab_size` must equal `model.vocab_size`
- `tokenizer.path` must point to `tokenizers/educode_bpe_8k/`
- special token ids must be recorded
- model embedding size must match vocab size
- `lm_head` output size must match vocab size

Required formula:

`model.vocab_size = tokenizer.vocab_size`

## 9. Encode / Decode Tests
T2.1 / T2.2 follow-up work should test:
- English round trip
- Chinese round trip
- emoji handling
- code snippet handling
- math text handling
- special tokens handling
- unknown character behavior
- empty string behavior
- long text behavior

Suggested test samples:
- `"hello world"`
- `"你好，世界"`
- `"Python code: print('hello')"`
- `"Transformer models predict the next token."`
- `"loss = F.cross_entropy(logits, targets)"`
- `"Emoji test 😊"`

## 10. Integration Plan
### T2.1 Tokenizer environment check
Check whether `tokenizers` or `sentencepiece` is already installed.
Do not install anything yet.

### T2.2 Train tiny BPE tokenizer on toy corpus
Use the toy corpus or a tiny local sample only to validate the artifact path.

### T2.3 BPE encode/decode inspection
Inspect round trip behavior, token ids, and special tokens.

### T2.4 Update config for BPE path
Make the config reference `tokenizer.path` explicitly.

### T2.5 Replace ByteTokenizer in real-data training path
Keep `ByteTokenizer` for smoke usage, but move formal training scripts to the BPE tokenizer path.

## 11. Relationship to Existing ByteTokenizer
`ByteTokenizer` should not be removed.
It should continue serving:
- learning
- smoke fallback
- debug
- no-dependency tests

The BPE tokenizer should be used for:
- formal training
- real dataset runs
- future A100/B200 scaling

## 12. Risks and Mitigations
Risk: tokenizer library unavailable  
Mitigation: run T2.1 environment check and install only with approval

Risk: tokenizer artifacts mismatch model vocab  
Mitigation: validator rules should enforce `tokenizer.vocab_size == model.vocab_size`

Risk: poor tokenizer trained on tiny corpus  
Mitigation: first tokenizer is only for pipeline validation; retrain later on a better corpus

Risk: copyrighted or private data  
Mitigation: use only allowed, open, or user-created corpus sources

Risk: encode/decode bugs  
Mitigation: add inspection scripts and tests before formal training

## 13. What T2 Does Not Do
T2 does not:
- implement tokenizer code
- train a tokenizer
- download data
- install `tokenizers` or `sentencepiece`
- modify the model
- run training
- replace `ByteTokenizer` yet
- execute `git push`

## 14. Recommended Next Step
Recommended next step:
- T2.1: tokenizer environment check

T2.1 should only check:
- whether `tokenizers` is installed
- whether `sentencepiece` is installed
- whether transformers tokenizer support is available
- without installing packages
- without training a tokenizer
