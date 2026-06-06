# DoRA / LoftQ Feasibility Notes

DoRA and LoftQ are useful future PEFT/quantization directions, but this branch does not implement either method.

## Current Status

- DoRA: documentation-only feasibility note.
- LoftQ: documentation-only feasibility note.
- QLoRA: local config/readiness guard only.

## Required Before Implementation

- Decide adapter checkpoint format.
- Decide quantized model load path.
- Validate bitsandbytes and CUDA compatibility in a bounded environment.
- Add explicit cost confirmation before any Modal/GPU run.
