# T3 Small Real Dataset Plan

## 1. Purpose
The purpose of T3 is to move from the toy corpus stage toward a small real dataset stage for EduCode-1.5B.

This step is meant to:
- transition from toy corpus experiments to a small real dataset baseline
- prepare the first batch of real small-scale text for the formal training line
- define source policy, license boundaries, safety boundaries, cleaning rules, and train/validation split rules
- prepare for the later `educode_bpe_8k` tokenizer and small real-data training path
- stay as a planning-only step with no data download, no corpus creation, and no model training

## 2. Current Baseline
Already completed:
- ByteTokenizer smoke path
- tiny BPE tokenizer artifact
- BPE tokenizer integration smoke
- tokenizer config path validation
- tokenizer config split:
  - `configs/windows/byte_smoke_10m.json`
  - `configs/windows/bpe_toy_512_smoke.json`
  - `configs/windows/bpe_8k_formal_placeholder.json`
- training loop on toy data
- checkpoint / generation / logging

Still not completed:
- real dataset
- formal BPE 8k tokenizer
- train / validation split
- validation loop
- real-data training

## 3. Dataset Goal
The first small real dataset should be designed for EduCode-1.5B's CS / ML / code learning direction.

The goal is:
- small enough to stay controllable and reproducible
- realistic enough to exercise the later real-data path
- appropriate for Windows RTX 2080 Ti / 4060 Ti small real-data runs
- not a large-scale pretraining corpus
- focused on validating the real-data pipeline, BPE tokenizer, train/val loss logging, and checkpoint resume behavior

Recommended first-stage scale:
- raw text: 1MB - 20MB
- token budget: 100k - 2M tokens
- `context_length`: 128 or 256
- model size: 10M - 40M
- hardware: local Windows GPU

## 4. Candidate Data Sources

### Option A: User-created study notes
Description:
- user-written CS / ML / Python / math notes
- lowest license risk
- quality is easier to control
- a good first candidate for small real-data experiments

Pros:
- safe
- aligned with EduCode theme
- no copyright ambiguity
- easy to clean

Risks:
- total data volume may stay small
- style may be narrow

### Option B: Public domain / permissive educational text
Description:
- educational text with clear public-domain or permissive licensing
- source and license must be recorded

Pros:
- closer to broader real text
- can scale gradually

Risks:
- license review is required
- cleaning effort is required

### Option C: Permissively licensed code snippets
Description:
- only small code snippets with permissive licenses
- helpful for code / math / CS style modeling

Pros:
- aligned with EduCode's code-oriented theme
- useful for tokenizer exposure to code tokens

Risks:
- license handling is more complex
- must avoid large-scale copying of third-party projects

### Option D: Synthetic educational examples
Description:
- small synthetic teaching examples can be added later
- generation method should be recorded so they are not confused with real data

Pros:
- controllable
- useful for adding format diversity

Risks:
- distribution may not reflect real text
- easy to overfit on repeated templates

### Option E: Local curated mini corpus
Description:
- manually curated set of allowed markdown / txt / python files
- a practical starting point for T4 / T5

Pros:
- most stable engineering path
- easiest way to enter the real-data pipeline gradually

Risks:
- limited scale
- should not be described as large-scale training data

## 5. Recommended First Dataset Strategy
Recommended first-stage priority:
1. user-created notes
2. small local curated CS / ML / code examples
3. permissive / public-domain snippets only when the license is explicit

Do not start with:
- internet-scale scraping
- large downloaded datasets
- unclear copyright course material
- private chats or private notes unless the user explicitly allows it

Recommended future directory structure:

```text
data/real_corpus/
  README.md
  raw/
  processed/
  splits/
  metadata/
```

Important note:
- T3 only documents this structure
- T3 does not create these directories
- T4 can create the skeleton later

## 6. Data Format
Allowed future raw formats:
- `.txt`
- `.md`
- `.py`
- `.jsonl`

Recommended normalized processed format: text JSONL.

Example line:

```json
{
  "id": "doc_000001",
  "source": "user_notes",
  "license": "user_created",
  "text": "...",
  "split": "train"
}
```

Alternative intermediate format:

```json
{
  "id": "...",
  "text": "...",
  "metadata": {
    "source": "...",
    "license": "...",
    "path": "..."
  }
}
```

## 7. Cleaning Rules
Future cleaning rules should include:
- normalize line endings
- remove binary / non-text files
- strip excessive whitespace
- preserve code indentation
- preserve markdown headings when they are useful
- remove private paths / names if needed
- remove secrets / API keys
- remove huge duplicated blocks
- keep Chinese / English / code mixed text
- record dropped files and reasons

## 8. License and Safety Rules
The first real dataset must follow these rules:
- only use user-created, public-domain, or permissively licensed material
- record source and license per document
- do not include private credentials
- do not include private personal data
- do not include copyrighted books or course PDFs unless permission is clearly documented
- do not commit large raw datasets by default
- `raw/` and `processed/` may remain ignored when dataset size grows

## 9. Train / Validation Split Plan
The default split plan should be:
- 90% train / 10% validation
- split by document rather than random token chunks when possible
- keep the validation set fixed after the split is created
- record the split seed
- avoid leakage from train to validation
- require `val_loss` logging in later real-data training

## 10. Tokenizer Relationship
Tokenizer planning rules:
- the tiny BPE 512 artifact is only a path-validation artifact
- the first formal tokenizer target should be `educode_bpe_8k`
- `vocab_size` target should be `8192`
- tokenizer training should use the training split or a tokenizer-training corpus
- avoid training the tokenizer on validation-only text when possible
- tokenizer artifacts should live under `tokenizers/educode_bpe_8k/`
- `model.vocab_size` must match `tokenizer.vocab_size`

## 11. First Real-Data Training Target
The first bounded real-data training target should be:
- hardware: local Windows GPU
- tokenizer: `educode_bpe_8k`
- model size: 10M - 40M
- `context_length`: 128 or 256
- batch size: small and adjusted to GPU memory
- `max_steps`: initially 100 - 500
- `eval_interval`: 20 - 50
- checkpoint at the end
- generation sample at the end

Success criteria:
- `train_loss` is finite
- `val_loss` is finite
- no OOM occurs
- checkpoint reload works
- run summary / report is generated

## 12. What T3 Does Not Do
This step does not:
- download data
- create a real corpus
- train a tokenizer
- train a model
- write a data pipeline
- modify configs
- run evaluation
- execute `git push`

## 13. Recommended Next Step
Recommended next step:
- T4: Real Corpus Directory and Sample Data Intake Plan

If the project wants a narrower intermediate step, another option is:
- T3.1: Dataset source decision checklist

But for faster progress, T4 is the better next move. T4 can still avoid downloading external data while allowing creation of:
- `data/real_corpus/README.md`
- metadata templates or `.gitkeep` placeholders
- `docs/data_intake_checklist.md`
