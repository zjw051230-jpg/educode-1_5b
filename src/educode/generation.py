from __future__ import annotations

import torch

from educode.sampling import greedy_token, sample_token, validate_sampling_args


def safe_decode_token_ids(token_ids: list[int]) -> str:
    safe_token_ids = [token_id for token_id in token_ids if 0 <= token_id <= 255]
    return bytes(safe_token_ids).decode("utf-8", errors="replace")


def sample_next_token(
    logits: torch.Tensor,
    temperature: float = 1.0,
    top_k: int | None = None,
    top_p: float | None = None,
    *,
    generator: torch.Generator | None = None,
) -> int:
    if not isinstance(logits, torch.Tensor):
        raise TypeError("logits must be a torch.Tensor")
    return int(sample_token(logits, temperature=temperature, top_k=top_k, top_p=top_p, generator=generator).item())


def greedy_next_token(logits: torch.Tensor) -> int:
    if not isinstance(logits, torch.Tensor):
        raise TypeError("logits must be a torch.Tensor")
    return int(greedy_token(logits).item())


def generate_token_ids(
    model,
    tokenizer,
    prompt: str,
    max_new_tokens: int,
    device,
    temperature: float = 1.0,
    top_k: int | None = None,
    top_p: float | None = None,
    eos_token_id: int | None = None,
    strategy: str = "sample",
    seed: int | None = None,
) -> list[int]:
    if not isinstance(prompt, str):
        raise TypeError("prompt must be a str")
    if not isinstance(max_new_tokens, int) or max_new_tokens <= 0:
        raise ValueError("max_new_tokens must be a positive integer")
    if strategy not in {"greedy", "sample"}:
        raise ValueError("strategy must be greedy or sample")
    validate_sampling_args(temperature=temperature, top_k=top_k, top_p=top_p)

    token_ids = tokenizer.encode(prompt)
    generator = torch.Generator(device="cpu")
    if seed is not None:
        generator.manual_seed(seed)
    model.eval()

    for _ in range(max_new_tokens):
        input_token_ids = token_ids[-model.config.context_length :]
        input_ids = torch.tensor([input_token_ids], dtype=torch.long, device=device)

        with torch.no_grad():
            logits = model(input_ids)
        next_token_logits = logits[0, -1, :]
        if strategy == "greedy":
            next_token_id = greedy_next_token(next_token_logits)
        else:
            next_token_id = sample_next_token(
                next_token_logits,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                generator=generator,
            )
        token_ids.append(next_token_id)
        if eos_token_id is not None and next_token_id == eos_token_id:
            break

    return token_ids


def generate_text(
    model,
    tokenizer,
    prompt: str,
    max_new_tokens: int,
    device,
    temperature: float = 1.0,
    top_k: int | None = None,
    top_p: float | None = None,
    eos_token_id: int | None = None,
    strategy: str = "sample",
    seed: int | None = None,
) -> str:
    token_ids = generate_token_ids(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        device=device,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        eos_token_id=eos_token_id,
        strategy=strategy,
        seed=seed,
    )

    try:
        return tokenizer.decode(token_ids)
    except (UnicodeDecodeError, ValueError):
        return safe_decode_token_ids(token_ids)
