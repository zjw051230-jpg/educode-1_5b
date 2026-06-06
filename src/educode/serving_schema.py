from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GenerateRequest:
    prompt: str
    max_new_tokens: int = 32
    temperature: float = 0.7
    top_k: int | None = 50
    top_p: float = 0.95

    def __post_init__(self) -> None:
        if not self.prompt.strip():
            raise ValueError("prompt must be non-empty")
        if self.max_new_tokens <= 0:
            raise ValueError("max_new_tokens must be positive")
        if self.temperature <= 0:
            raise ValueError("temperature must be positive")
        if self.top_k is not None and self.top_k <= 0:
            raise ValueError("top_k must be positive when provided")
        if not 0 < self.top_p <= 1:
            raise ValueError("top_p must be in (0, 1]")


@dataclass(frozen=True)
class GenerateResponse:
    text: str
    model_name: str
    tokens_generated: int
    checkpoint_loaded: bool = False


def validate_generate_request(request: GenerateRequest | dict[str, object]) -> GenerateRequest:
    if isinstance(request, GenerateRequest):
        return request
    return GenerateRequest(
        prompt=str(request.get("prompt", "")),
        max_new_tokens=int(request.get("max_new_tokens", 32)),
        temperature=float(request.get("temperature", 0.7)),
        top_k=None if request.get("top_k") is None else int(request.get("top_k", 50)),
        top_p=float(request.get("top_p", 0.95)),
    )
