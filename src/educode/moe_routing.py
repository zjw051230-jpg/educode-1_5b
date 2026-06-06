from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from torch.nn import functional as F


@dataclass(frozen=True)
class DispatchMetadata:
    expert_indices: torch.Tensor
    slot_indices: torch.Tensor
    combine_weights: torch.Tensor
    capacity: int


def load_balancing_loss(router_probs: torch.Tensor, expert_indices: torch.Tensor, num_experts: int) -> torch.Tensor:
    if router_probs.ndim != 2:
        raise ValueError("router_probs must have shape [tokens, experts]")
    if expert_indices.ndim != 2:
        raise ValueError("expert_indices must have shape [tokens, top_k]")
    token_fraction = F.one_hot(expert_indices, num_classes=num_experts).float().sum(dim=1).mean(dim=0)
    prob_fraction = router_probs.mean(dim=0)
    return num_experts * torch.sum(token_fraction * prob_fraction)


def router_z_loss(router_logits: torch.Tensor) -> torch.Tensor:
    if router_logits.ndim != 2:
        raise ValueError("router_logits must have shape [tokens, experts]")
    return torch.mean(torch.logsumexp(router_logits, dim=-1).pow(2))


def expert_capacity(num_tokens: int, num_experts: int, top_k: int, capacity_factor: float = 1.25) -> int:
    if num_tokens <= 0 or num_experts <= 0 or top_k <= 0:
        raise ValueError("num_tokens, num_experts, and top_k must be positive")
    if capacity_factor <= 0:
        raise ValueError("capacity_factor must be positive")
    return max(1, math.ceil(capacity_factor * num_tokens * top_k / num_experts))


def dispatch_tokens(
    tokens: torch.Tensor,
    expert_indices: torch.Tensor,
    combine_weights: torch.Tensor,
    *,
    num_experts: int,
    capacity_factor: float = 1.25,
) -> tuple[torch.Tensor, DispatchMetadata]:
    if tokens.ndim != 2:
        raise ValueError("tokens must have shape [tokens, d_model]")
    if expert_indices.shape != combine_weights.shape:
        raise ValueError("expert_indices and combine_weights must have matching shape")
    num_tokens, d_model = tokens.shape
    top_k = expert_indices.shape[1]
    capacity = expert_capacity(num_tokens, num_experts, top_k, capacity_factor)
    dispatched = tokens.new_zeros((num_experts, capacity, d_model))
    slot_counts = [0 for _ in range(num_experts)]
    slot_indices = torch.full_like(expert_indices, -1)
    for token_idx in range(num_tokens):
        for route_idx in range(top_k):
            expert = int(expert_indices[token_idx, route_idx].item())
            slot = slot_counts[expert]
            if slot >= capacity:
                continue
            dispatched[expert, slot] = tokens[token_idx] * combine_weights[token_idx, route_idx]
            slot_indices[token_idx, route_idx] = slot
            slot_counts[expert] += 1
    return dispatched, DispatchMetadata(expert_indices, slot_indices, combine_weights, capacity)


def combine_tokens(expert_outputs: torch.Tensor, metadata: DispatchMetadata, *, num_tokens: int) -> torch.Tensor:
    if expert_outputs.ndim != 3:
        raise ValueError("expert_outputs must have shape [experts, capacity, d_model]")
    output = expert_outputs.new_zeros((num_tokens, expert_outputs.shape[-1]))
    top_k = metadata.expert_indices.shape[1]
    for token_idx in range(num_tokens):
        for route_idx in range(top_k):
            slot = int(metadata.slot_indices[token_idx, route_idx].item())
            if slot < 0:
                continue
            expert = int(metadata.expert_indices[token_idx, route_idx].item())
            output[token_idx] += expert_outputs[expert, slot]
    return output
