# Inference KV Cache Harness V2

This branch adds CPU-testable inference scaffolding for generation, sampling, KV cache interfaces, PagedAttention-style block tables, speculative decoding protocols, and small perplexity evaluation.

## Implemented Scope

- Greedy generation.
- Temperature, top-k, and top-p sampling.
- EOS handling and deterministic seed support.
- KV cache append/read/reset skeleton.
- Prefill/decode interface skeleton.
- PagedAttention block table skeleton.
- Speculative decoding interface with an n-gram proposer.
- Tiny CPU generation smoke and finite loss/perplexity eval.

## Non-Goals

- No real checkpoint loading.
- No GPU execution.
- No Modal run.
- No inference speedup claim.
- No production serving implementation.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\generation.py src\educode\sampling.py src\educode\kv_cache.py src\educode\inference.py src\educode\speculative.py src\educode\paged_cache.py src\educode\eval.py scripts\run_generation_smoke.py scripts\validate_inference_harness.py tests\test_generation.py tests\test_sampling.py tests\test_kv_cache.py tests\test_speculative_interface.py tests\test_eval_harness.py
.\.venv\Scripts\python.exe scripts\run_generation_smoke.py
.\.venv\Scripts\python.exe scripts\validate_inference_harness.py
.\.venv\Scripts\python.exe tests\test_generation.py
.\.venv\Scripts\python.exe tests\test_sampling.py
.\.venv\Scripts\python.exe tests\test_kv_cache.py
.\.venv\Scripts\python.exe tests\test_speculative_interface.py
.\.venv\Scripts\python.exe tests\test_eval_harness.py
git diff --check
```

## Future Gate

Any real checkpoint inference, latency measurement, KV-cache speedup claim, or speculative decoding speedup claim requires a separate GPU/Modal gate and explicit user confirmation.
