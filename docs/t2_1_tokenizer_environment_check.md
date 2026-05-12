# T2.1 Tokenizer Environment Check

## 1. Purpose
The purpose of T2.1 is to check the local tokenizer-related Python environment only.
This step does not install packages, does not train a tokenizer, and does not change the training path.

## 2. Files Added
- `scripts/check_tokenizer_env.py`

## 3. Environment Results
- Python executable: `C:\Users\zjw\AppData\Local\Programs\Python\Python311\python.exe`
- Python version: `3.11.9`
- `tokenizers` import result: available
- `tokenizers` version: `0.22.2`
- `sentencepiece` import result: missing
- `sentencepiece` detail: `ModuleNotFoundError: No module named 'sentencepiece'`
- `transformers` import result: available
- `transformers` version: `5.1.0`
- `from transformers import AutoTokenizer` result: available
- `datasets` import result: available
- `datasets` version: `4.5.0`

## 4. Decision
- Hugging Face `tokenizers` can be the first-choice route for the EduCode BPE path because the package is already available locally.
- `sentencepiece` should not be the first route right now because it is not installed in the current environment.
- No new package installation is required for the immediate Hugging Face `tokenizers`-first direction.
- If a future step still wants `sentencepiece` or any other dependency changes, that installation must be approved separately.

## 5. What It Does Not Do
This step does not:
- install packages
- train a tokenizer
- download data
- download models
- modify the real training path
- modify `ByteTokenizer`
- modify model / training / checkpoint / generation code
- run training
- execute `git push`

## 6. Next Step
Recommended next step:
- T2.2: train a tiny BPE tokenizer on a toy or local sample corpus

Condition:
- proceed only because `tokenizers` is available locally
- if the route changes to a missing dependency later, make a separate dependency-install decision first
