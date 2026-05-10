from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch
from torch import nn
from torch.nn import functional as F


@dataclass
class TinyModelConfig:
    vocab_size: int
    context_length: int
    num_layers: int
    d_model: int
    num_heads: int
    d_ff: int
    dropout: float = 0.0
    attention_backend: str = "sdpa"

    def __post_init__(self) -> None:
        if not isinstance(self.vocab_size, int) or self.vocab_size <= 0:
            raise ValueError("vocab_size must be a positive integer")
        if not isinstance(self.context_length, int) or self.context_length <= 0:
            raise ValueError("context_length must be a positive integer")
        if not isinstance(self.num_layers, int) or self.num_layers <= 0:
            raise ValueError("num_layers must be a positive integer")
        if not isinstance(self.d_model, int) or self.d_model <= 0:
            raise ValueError("d_model must be a positive integer")
        if not isinstance(self.num_heads, int) or self.num_heads <= 0:
            raise ValueError("num_heads must be a positive integer")
        if not isinstance(self.d_ff, int) or self.d_ff <= self.d_model:
            raise ValueError("d_ff must be greater than d_model")
        if self.d_model % self.num_heads != 0:
            raise ValueError("d_model must be divisible by num_heads")
        if not isinstance(self.dropout, (int, float)) or not 0.0 <= float(self.dropout) <= 1.0:
            raise ValueError("dropout must be between 0.0 and 1.0")
        if self.attention_backend != "sdpa":
            raise ValueError("attention_backend must be sdpa")

        self.dropout = float(self.dropout)

    @property
    def head_dim(self) -> int:
        return self.d_model // self.num_heads


class RMSNorm(nn.Module):
    def __init__(self, d_model: int, eps: float = 1e-5) -> None:
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(d_model))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        rms = x.pow(2).mean(dim=-1, keepdim=True)
        normalized = x * torch.rsqrt(rms + self.eps)
        return normalized * self.weight


class CausalSelfAttention(nn.Module):
    def __init__(self, config: TinyModelConfig) -> None:
        super().__init__()
        if config.attention_backend != "sdpa":
            raise ValueError("CausalSelfAttention only supports attention_backend='sdpa'")

        self.num_heads = config.num_heads
        self.head_dim = config.head_dim
        self.dropout = config.dropout
        self.qkv_proj = nn.Linear(config.d_model, 3 * config.d_model, bias=False)
        self.out_proj = nn.Linear(config.d_model, config.d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, d_model = x.shape
        qkv = self.qkv_proj(x)
        q, k, v = qkv.chunk(3, dim=-1)

        q = q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        k = k.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        v = v.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        attn_output = F.scaled_dot_product_attention(
            q,
            k,
            v,
            dropout_p=self.dropout if self.training else 0.0,
            is_causal=True,
        )
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)
        return self.out_proj(attn_output)


class SwiGLUFeedForward(nn.Module):
    def __init__(self, config: TinyModelConfig) -> None:
        super().__init__()
        self.gate_proj = nn.Linear(config.d_model, config.d_ff, bias=False)
        self.up_proj = nn.Linear(config.d_model, config.d_ff, bias=False)
        self.down_proj = nn.Linear(config.d_ff, config.d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        gate = self.gate_proj(x)
        up = self.up_proj(x)
        return self.down_proj(F.silu(gate) * up)


class TransformerBlock(nn.Module):
    def __init__(self, config: TinyModelConfig) -> None:
        super().__init__()
        self.norm1 = RMSNorm(config.d_model)
        self.attention = CausalSelfAttention(config)
        self.norm2 = RMSNorm(config.d_model)
        self.mlp = SwiGLUFeedForward(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attention(self.norm1(x))
        x = x + self.mlp(self.norm2(x))
        return x


class TinyDecoderOnlyTransformer(nn.Module):
    def __init__(self, config: TinyModelConfig) -> None:
        super().__init__()
        self.config = config
        self.token_embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.position_embedding = nn.Embedding(config.context_length, config.d_model)
        self.blocks = nn.ModuleList(TransformerBlock(config) for _ in range(config.num_layers))
        self.final_norm = RMSNorm(config.d_model)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        if not isinstance(input_ids, torch.Tensor):
            raise TypeError("input_ids must be a torch.Tensor")
        if input_ids.ndim != 2:
            raise ValueError("input_ids must be a 2D tensor of shape [B, T]")
        if input_ids.dtype != torch.long:
            raise TypeError("input_ids must have dtype torch.long")

        batch_size, seq_len = input_ids.shape
        if seq_len > self.config.context_length:
            raise ValueError("input sequence length exceeds context_length")
        if input_ids.numel() > 0:
            min_token_id = int(input_ids.min().item())
            max_token_id = int(input_ids.max().item())
            if min_token_id < 0 or max_token_id >= self.config.vocab_size:
                raise ValueError("input_ids must be in range [0, vocab_size)")

        position_ids = torch.arange(seq_len, device=input_ids.device).unsqueeze(0).expand(batch_size, seq_len)
        x = self.token_embedding(input_ids) + self.position_embedding(position_ids)

        for block in self.blocks:
            x = block(x)

        x = self.final_norm(x)
        return self.lm_head(x)


def _require_section(config: dict[str, Any], section_name: str) -> dict[str, Any]:
    section = config.get(section_name)
    if not isinstance(section, dict):
        raise KeyError(f"missing required config section: {section_name}")
    return section


def _require_int(section: dict[str, Any], key: str, section_name: str) -> int:
    value = section.get(key)
    if not isinstance(value, int):
        raise KeyError(f"missing or invalid integer field: {section_name}.{key}")
    return value


def _require_float(section: dict[str, Any], key: str, section_name: str) -> float:
    value = section.get(key)
    if not isinstance(value, (int, float)):
        raise KeyError(f"missing or invalid numeric field: {section_name}.{key}")
    return float(value)


def _require_str(section: dict[str, Any], key: str, section_name: str) -> str:
    value = section.get(key)
    if not isinstance(value, str):
        raise KeyError(f"missing or invalid string field: {section_name}.{key}")
    return value


def model_config_from_dict(config: dict[str, Any]) -> TinyModelConfig:
    if not isinstance(config, dict):
        raise TypeError("config must be a dict")

    model = _require_section(config, "model")
    profiling = _require_section(config, "profiling")
    tokenizer = _require_section(config, "tokenizer")

    vocab_size = _require_int(model, "vocab_size", "model")
    tokenizer_vocab_size = _require_int(tokenizer, "vocab_size", "tokenizer")
    if vocab_size != tokenizer_vocab_size:
        raise ValueError("tokenizer.vocab_size must match model.vocab_size")

    return TinyModelConfig(
        vocab_size=vocab_size,
        context_length=_require_int(model, "context_length", "model"),
        num_layers=_require_int(model, "num_layers", "model"),
        d_model=_require_int(model, "d_model", "model"),
        num_heads=_require_int(model, "num_heads", "model"),
        d_ff=_require_int(model, "d_ff", "model"),
        dropout=_require_float(model, "dropout", "model"),
        attention_backend=_require_str(profiling, "attention_backend", "profiling"),
    )
