# W2 CUDA Environment Check

## 1. Summary
This Windows RTX 4060 Ti 16GB machine is suitable for:
- local inference
- LoRA / PEFT
- small-model smoke test
- CUDA functionality validation

It is not intended for 1.5B full pretraining.

## 2. Python / Torch
- Python version: 3.11.9
- torch version: 2.5.1+cu121
- `torch.cuda.is_available()`: True
- `torch.version.cuda`: 12.1
- `torch.backends.cudnn.version()`: 90100

## 3. GPU
- GPU name: NVIDIA GeForce RTX 4060 Ti
- total memory: 16.0 GiB
- compute capability: 8.9
- CUDA device count: 1

## 4. bf16 / TF32
- `torch.cuda.is_bf16_supported()`: True
- `torch.backends.cuda.matmul.allow_tf32`: False
- `torch.backends.cudnn.allow_tf32`: True
- bf16 matmul sanity check: Success

## 5. SDPA
- `torch.nn.functional.scaled_dot_product_attention` ran successfully on CUDA.
- This is only a PyTorch SDPA primitive check, not a FlashAttention-2 integration.

## 6. nvidia-smi / nvcc
- `nvidia-smi`: Success
- `nvcc --version`: Success
- `nvidia-smi` reported CUDA 13.1.
- PyTorch reported CUDA 12.1.
- `nvcc` reported CUDA 11.8.
- This mismatch is common: driver capability, PyTorch compiled CUDA version, and local toolkit version can differ.

## 7. Timeout Fix
- W2.1 added explicit subprocess timeout protection to external command calls.
- All `subprocess.run` calls in `scripts/check_cuda_env.py` now use `timeout=15` seconds.
- The script now handles `subprocess.TimeoutExpired` and reports a clear timeout message.
- The script will not wait indefinitely if `nvidia-smi` or `nvcc` hangs.

## 8. Decision
- Windows line is suitable as an engineering fast track.
- It is suitable for small-model CUDA smoke tests.
- It is suitable for LoRA / PEFT experiments.
- It is not suitable as the formal platform for 1.5B full pretraining.

## 9. Next Step
Suggested W3 directions:
- create a minimal config schema draft
- or create a smoke test plan document
- still do not implement the training mainline
