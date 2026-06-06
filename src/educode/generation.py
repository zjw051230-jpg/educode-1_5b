from __future__ import annotations

import torch
from torch.nn import functional as F


def safe_decode_token_ids(token_ids: list[int]) -> str:
    safe_token_ids = [token_id for token_id in token_ids if 0 <= token_id <= 255]
    return bytes(safe_token_ids).decode("utf-8", errors="replace")


def greedy_next_token(logits: torch.Tensor) -> int:
    if not isinstance(logits, torch.Tensor):
        raise TypeError("logits must be a torch.Tensor")
    if logits.ndim != 1:
        raise ValueError("logits must have shape [vocab_size]")
    return int(torch.argmax(logits).item())


def _apply_top_p_filter(logits: torch.Tensor, top_p: float | None) -> torch.Tensor:
    if top_p is None:
        return logits
    if not isinstance(top_p, (int, float)) or not 0.0 < float(top_p) <= 1.0:
        raise ValueError("top_p must be in the interval (0, 1]")
    if top_p >= 1.0:
        return logits

    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
    sorted_probs = F.softmax(sorted_logits, dim=-1)
    cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
    remove_mask = cumulative_probs > float(top_p)
    remove_mask[..., 1:] = remove_mask[..., :-1].clone()
    remove_mask[..., 0] = False

    filtered = logits.clone()
    filtered[sorted_indices[remove_mask]] = float("-inf")
    return filtered


def sample_next_token(
    logits: torch.Tensor,
    temperature: float = 1.0,
    top_k: int | None = None,
    top_p: float | None = None,
) -> int:
    if not isinstance(logits, torch.Tensor):
        raise TypeError("logits must be a torch.Tensor")
    if logits.ndim != 1:
        raise ValueError("logits must have shape [vocab_size]")
    if temperature <= 0:
        raise ValueError("temperature must be greater than 0")

    scaled_logits = logits / temperature
    scaled_logits = _apply_top_p_filter(scaled_logits, top_p)
    if top_k is not None and top_k > 0:
        k = min(top_k, scaled_logits.shape[0])
        top_values, top_indices = torch.topk(scaled_logits, k=k)
        probabilities = F.softmax(top_values, dim=-1)
        sampled_index = torch.multinomial(probabilities, num_samples=1)
        return int(top_indices[sampled_index].item())

    probabilities = F.softmax(scaled_logits, dim=-1)
    sampled_index = torch.multinomial(probabilities, num_samples=1)
    return int(sampled_index.item())


def generate_token_ids(
    model,
    tokenizer,
    prompt: str,
    max_new_tokens: int,
    device,
    temperature: float = 1.0,
    top_k: int | None = None,
    top_p: float | None = None,
    strategy: str = "sample",
) -> list[int]:
    if not isinstance(prompt, str):
        raise TypeError("prompt must be a str")
    if not isinstance(max_new_tokens, int) or max_new_tokens <= 0:
        raise ValueError("max_new_tokens must be a positive integer")
    if strategy not in {"greedy", "sample"}:
        raise ValueError("strategy must be one of: greedy, sample")

    token_ids = tokenizer.encode(prompt)
    model.eval()

    for _ in range(max_new_tokens):
        input_token_ids = token_ids[-model.config.context_length :]
        input_ids = torch.tensor([input_token_ids], dtype=torch.long, device=device)

        with torch.no_grad():
            logits = model(input_ids)
        next_token_logits = logits[0, -1, :]
        next_token_id = (
            greedy_next_token(next_token_logits)
            if strategy == "greedy"
            else sample_next_token(next_token_logits, temperature=temperature, top_k=top_k, top_p=top_p)
        )
        token_ids.append(next_token_id)

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
    strategy: str = "sample",
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
        strategy=strategy,
    )

    try:
        return tokenizer.decode(token_ids)
    except (UnicodeDecodeError, ValueError):
        return safe_decode_token_ids(token_ids)
