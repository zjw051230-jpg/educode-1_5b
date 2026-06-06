from __future__ import annotations

from dataclasses import dataclass

import torch


def newton_schulz_orthogonalize(matrix: torch.Tensor, steps: int = 5, eps: float = 1e-7) -> torch.Tensor:
    if matrix.ndim != 2:
        raise ValueError("Newton-Schulz helper expects a 2D matrix")
    if steps <= 0:
        raise ValueError("steps must be positive")
    x = matrix.float()
    norm = x.norm()
    if not torch.isfinite(norm) or float(norm.item()) <= 0:
        return torch.zeros_like(matrix)
    x = x / (norm + eps)
    transposed = False
    if x.shape[0] > x.shape[1]:
        x = x.T
        transposed = True
    for _ in range(steps):
        a = x @ x.T
        x = 1.5 * x - 0.5 * (a @ x)
    if transposed:
        x = x.T
    return x.to(dtype=matrix.dtype)


def is_muon_candidate(name: str, parameter: torch.nn.Parameter) -> bool:
    lowered = name.lower()
    excluded = ("embedding", "embed", "norm", "bias", "lm_head")
    return parameter.ndim == 2 and not any(marker in lowered for marker in excluded)


@dataclass(frozen=True)
class MuonParameterGroups:
    muon: list[tuple[str, torch.nn.Parameter]]
    adamw: list[tuple[str, torch.nn.Parameter]]


def split_muon_adamw_parameters(named_parameters) -> MuonParameterGroups:
    muon: list[tuple[str, torch.nn.Parameter]] = []
    adamw: list[tuple[str, torch.nn.Parameter]] = []
    for name, parameter in named_parameters:
        if not parameter.requires_grad:
            continue
        if is_muon_candidate(name, parameter):
            muon.append((name, parameter))
        else:
            adamw.append((name, parameter))
    return MuonParameterGroups(muon=muon, adamw=adamw)


class MuonExperimental(torch.optim.Optimizer):
    def __init__(self, params, lr: float = 0.02, momentum: float = 0.95, ns_steps: int = 5) -> None:
        if lr <= 0:
            raise ValueError("lr must be positive")
        if not 0 <= momentum < 1:
            raise ValueError("momentum must be in [0, 1)")
        defaults = {"lr": lr, "momentum": momentum, "ns_steps": ns_steps}
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        for group in self.param_groups:
            lr = group["lr"]
            momentum = group["momentum"]
            ns_steps = group["ns_steps"]
            for parameter in group["params"]:
                if parameter.grad is None:
                    continue
                if parameter.grad.ndim != 2:
                    raise ValueError("MuonExperimental only accepts 2D parameters")
                state = self.state[parameter]
                if "momentum_buffer" not in state:
                    state["momentum_buffer"] = torch.zeros_like(parameter.grad)
                buffer = state["momentum_buffer"]
                buffer.mul_(momentum).add_(parameter.grad)
                update = newton_schulz_orthogonalize(buffer, steps=ns_steps)
                parameter.add_(update, alpha=-lr)
        return loss
