# D1 Expand Permitted Corpus Plan

## 1. Purpose
说明 A100 可行性已经验证，下一阶段核心瓶颈是数据规模与 tokenizer 质量。

## 2. Current Baseline
- 当前训练数据是 project-authored synthetic seed corpus
- processed docs = 8
- train docs = 7
- val docs = 1
- BPE tokenizer observed vocab = 1174
- A100 2.15B seq512 50-step optimizer profile passed
- 但当前数据太小，不能支撑 meaningful pretraining

## 3. Target Corpus Scale Ladder
- D1 phase 0: keep synthetic seed corpus as smoke baseline
- D1 phase 1: 1MB - 10MB permitted educational/code text
- D1 phase 2: 50MB - 200MB curated corpus
- D1 phase 3: 1GB+ only after licensing and pipeline validation

## 4. Allowed Source Categories
- project-authored notes
- project-authored code examples
- synthetic educational examples
- public-domain text where license is explicit
- permissively licensed code/text where license is explicit
- user-approved local notes, only if user explicitly approves

## 5. Disallowed / High-Risk Sources
- private chats
- private documents without explicit approval
- copyrighted course PDFs or textbooks
- scraped web pages without license review
- API keys / logs / secrets
- unknown-license datasets
- large internet dumps at this stage

## 6. Data Intake Requirements
未来每个 source 必须有：
- source_id
- source_category
- path or origin
- license_or_ownership
- allowed_for_training
- allowed_to_commit
- privacy_risk
- expected_file_types
- notes

## 7. Cleaning Requirements
未来 pipeline 应：
- scan secrets
- normalize line endings
- preserve code indentation
- remove empty/duplicate docs
- keep train/val split document-level
- output processed JSONL
- write intake summary

## 8. Tokenizer Implication
- 当前 educode_bpe_8k observed vocab 只有 1174，因为语料太小
- corpus 扩大后需要重新训练 tokenizer
- tokenizer.vocab_size / model.vocab_size 必须重新对齐

## 9. Next Data Milestones
- D2 create expanded synthetic educational corpus
- D3 intake expanded corpus
- D4 train updated BPE tokenizer
- D5 BPE data/model/loss smoke
- D6 A100 small real-data training plan
- D7 A100 small real-data training run

## 10. What D1 Does Not Do
- 不下载数据
- 不复制数据
- 不训练 tokenizer
- 不训练模型
- 不进入 A100
