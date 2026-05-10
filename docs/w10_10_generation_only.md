# W10.10 Generation Only

## 1. Purpose
This step only verifies the minimal generation path.

## 2. Files Added
- `src/educode/generation.py`
- `scripts/inspect_generation.py`

## 3. What It Does
This step:
- converts a prompt to token ids
- maps token ids to model logits
- uses last-position logits to sample the next token
- appends the token
- decodes token ids back to text
- prints a generated text preview

## 4. Current Limitations
Current limitations:
- the model is still untrained
- the tokenizer is currently `ByteTokenizer`
- a random model can generate invalid UTF-8 byte sequences
- fallback decode may show replacement characters
- generation quality does not represent model capability
- this step only validates generation control flow

## 5. What It Does Not Do
This step does not:
- train
- compute loss
- run backward
- perform an optimizer step
- save or load checkpoints
- run evaluation
- use beam search
- use top-p sampling
- use KV cache
- deploy a service

## 6. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/inspect_generation.py
```

## 7. Observed Result
- `inspect_generation.py` ran successfully
- device was `cuda`
- prompt was `hello`
- prompt token ids were `[104, 101, 108, 108, 111]`
- generated token ids length was `21`
- new token count was `16`
- generated text preview was `hello`
- fallback decode was not needed in the observed run
- the generation control flow succeeded

## 8. Learning Note
- generation is different from training
- generation does not use `target_ids`
- the model outputs logits
- generation chooses the next token from logits
- poor output from an untrained model is normal
- generation quality only becomes meaningful after training

## 9. Next Step
Suggested W10.11:
- logging integration only
- write forward / loss / generation / checkpoint inspection results to `metrics.jsonl`, `generation_samples.jsonl`, and `summary.md`
- still do not write a full training loop
