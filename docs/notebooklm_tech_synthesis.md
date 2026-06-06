# NotebookLM Technical Synthesis

This document turns the NotebookLM technical notes into project-level implementation lanes for EduCode-1.5B. It records what can be implemented locally, what must wait for GPU validation, and what the project must not claim before measurement.

## 1. Attention

Local implementation:

- Attention backend registry with SDPA as default.
- Naive causal attention baseline for small CPU comparisons.
- FlashAttention2 availability guard that does not require `flash_attn`.
- GQA reshape helper for future grouped-query experiments.
- Feasibility notes for FlexAttention and FlashAttention3.

GPU validation required:

- Any throughput comparison between SDPA, naive, FlashAttention2, or future kernels.
- Any claim about memory improvement from an alternative kernel.
- Any long-context attention profile beyond imported artifacts.

Do not claim yet:

- SDPA is faster than naive attention.
- FlashAttention2 is available or faster in this repo.
- FlashAttention3 or FlexAttention is implemented.

Recommended branch: `feature/attention-backend-abstraction-v2`.

Risk level: medium, because core model attention plumbing can affect training behavior if merged carelessly.

Cost gate: required before backend profiling on A100.

## 2. Optimizer

Local implementation:

- Optimizer registry with AdamW default.
- Newton-Schulz orthogonalization helper for Muon experiments.
- Guarded Muon optimizer or step helper with explicit acknowledgement.
- Parameter grouping that separates 2D hidden matrices from embeddings, norms, biases, and LM head.

GPU validation required:

- Any AdamW vs Muon training comparison.
- Any claim about convergence, final loss, or training stability.

Do not claim yet:

- Muon improves EduCode loss.
- Muon is production-ready for this codebase.
- Mixed optimizer grouping is validated on a real training run.

Recommended branch: `feature/muon-experimental-optimizer`.

Risk level: medium-high, because optimizer changes can silently alter training dynamics.

Cost gate: required before any optimizer comparison run.

## 3. MoE

Local implementation:

- Top-k router skeleton.
- Load-balancing auxiliary loss.
- Router z-loss.
- Expert capacity helper.
- Synthetic token dispatch/combine path.
- MoE FFN skeleton guarded behind `moe.enabled=false`.

GPU validation required:

- Any MoE training, routing load-balance claim, throughput claim, or quality claim.
- Any capacity-factor tuning claim.

Do not claim yet:

- MoE improves quality or speed.
- MoE is wired into the dense baseline.
- Expert routing has been validated on real data.

Recommended branch: `feature/moe-routing-skeleton-v2`.

Risk level: high, because MoE changes model architecture and training semantics.

Cost gate: required before any MoE training or profiling run.

## 4. RoPE And Long Context

Local implementation:

- RoPE cache helper.
- `rotate_half` and `apply_rotary_emb`.
- Explicit position encoding schema for `learned` and `rope`.
- Passkey retrieval fixture generator.
- Placeholders for NTK, YaRN, and LongRoPE feasibility notes.

GPU validation required:

- Any long-context memory or throughput claim.
- Any assertion that RoPE improves long-context performance.
- Any checkpoint compatibility claim after wiring RoPE into the model.

Do not claim yet:

- RoPE is active in current checkpoints.
- Context extension is safe for long training.
- NTK, YaRN, or LongRoPE is implemented.

Recommended branch: `feature/rope-position-encoding-v2`.

Risk level: medium-high, because changing position encoding can break checkpoint assumptions.

Cost gate: required before long-context GPU profiling.

## 5. Inference

Local implementation:

- Greedy, temperature, top-k, and top-p sampling.
- EOS handling and deterministic seed support.
- KV cache skeleton with append/read/reset.
- Prefill/decode interface skeleton.
- PagedAttention block table skeleton.
- Speculative decoding protocol with fake or n-gram proposer.
- Small fixture perplexity evaluation.

GPU validation required:

- Any real checkpoint generation.
- Any inference latency, KV-cache speedup, PagedAttention speedup, or speculative decoding speedup claim.

Do not claim yet:

- The project has production inference.
- KV cache accelerates real checkpoints.
- Speculative decoding improves throughput.

Recommended branch: `feature/inference-kv-cache-harness-v2`.

Risk level: medium, because it is mostly additive and local-only if kept away from real checkpoints.

Cost gate: required before GPU checkpoint inference.

## Merge Order

Recommended review order:

1. `docs/notebooklm-tech-synthesis`
2. `feature/inference-kv-cache-harness-v2`
3. `feature/attention-backend-abstraction-v2`
4. `feature/muon-experimental-optimizer`
5. `feature/rope-position-encoding-v2`
6. `feature/moe-routing-skeleton-v2`

The lower-risk docs and inference skeletons should land before architecture or optimizer changes. MoE should be reviewed last because it has the highest chance of future model-behavior interaction.
