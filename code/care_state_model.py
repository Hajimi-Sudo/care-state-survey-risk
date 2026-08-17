"""CARE-State model and training utilities.

The implementation follows the information path described in the manuscript:
each domain is encoded separately, multiplied by an availability-aware
reliability gate, aggregated with the availability vector, and mapped to a
fixed-horizon risk. Inputs are expected to be harmonised before training.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import torch
from torch import Tensor, nn


class CAREState(nn.Module):
    """Missingness-aware domain-gated population risk state."""

    def __init__(self, domain_dims: Mapping[str, int], hidden_dim: int = 32,
                 state_dim: int = 64, dropout: float = 0.10) -> None:
        super().__init__()
        if not domain_dims or any(int(v) < 1 for v in domain_dims.values()):
            raise ValueError("domain_dims must contain positive feature counts")
        self.domain_names = tuple(domain_dims)
        self.domain_dims = {name: int(size) for name, size in domain_dims.items()}
        self.encoders = nn.ModuleDict()
        self.gates = nn.ModuleDict()
        for name, size in self.domain_dims.items():
            self.encoders[name] = nn.Sequential(
                nn.Linear(size, hidden_dim), nn.LayerNorm(hidden_dim),
                nn.GELU(), nn.Dropout(dropout)
            )
            self.gates[name] = nn.Sequential(
                nn.Linear(hidden_dim + 1, max(1, hidden_dim // 2)),
                nn.GELU(), nn.Linear(max(1, hidden_dim // 2), 1)
            )
        n_domains = len(self.domain_names)
        self.state = nn.Sequential(
            nn.Linear(hidden_dim + n_domains, state_dim), nn.LayerNorm(state_dim),
            nn.GELU(), nn.Dropout(dropout)
        )
        self.risk_head = nn.Linear(state_dim, 1)

    def forward(self, domains: Mapping[str, Tensor], masks: Mapping[str, Tensor]) -> Tensor:
        gated, mask_vector = [], []
        for name in self.domain_names:
            x = domains[name].float()
            mask = masks[name].float().reshape(-1, 1).clamp(0.0, 1.0)
            if x.ndim != 2 or x.shape[1] != self.domain_dims[name]:
                raise ValueError(f"{name} has shape {tuple(x.shape)}; expected (*, {self.domain_dims[name]})")
            z = self.encoders[name](x)
            reliability = torch.sigmoid(self.gates[name](torch.cat([z, mask], dim=1)))
            gated.append(mask * reliability * z)
            mask_vector.append(mask)
        evidence = torch.stack(gated, dim=0).sum(dim=0)
        availability = torch.cat(mask_vector, dim=1)
        state = self.state(torch.cat([evidence, availability], dim=1))
        return self.risk_head(state).squeeze(1)

    @torch.no_grad()
    def predict_proba(self, domains: Mapping[str, Tensor], masks: Mapping[str, Tensor]) -> Tensor:
        self.eval()
        return torch.sigmoid(self(domains, masks))


@dataclass
class FitResult:
    best_epoch: int
    best_val_loss: float
    history: list[dict[str, float]]


def _weighted_bce(logits: Tensor, target: Tensor, weight: Tensor) -> Tensor:
    losses = nn.functional.binary_cross_entropy_with_logits(logits, target.float(), reduction="none")
    normalized = weight.float() / weight.float().mean().clamp_min(1e-12)
    return (losses * normalized).mean()


def _monotonic_penalty(model: CAREState, domains: Mapping[str, Tensor],
                       masks: Mapping[str, Tensor], signs: Mapping[str, Tensor]) -> Tensor:
    """Penalise violations of prespecified directional signs.

    ``signs[name]`` has one value per input feature: ``+1`` means increasing
    the feature should not decrease the logit, ``-1`` means the reverse, and
    ``0`` leaves the feature unconstrained. This is a soft training penalty;
    the exact signs and feature map must be supplied by the data audit.
    """
    if not signs:
        return next(model.parameters()).new_zeros(())
    tracked = {name: value.detach().clone().requires_grad_(True) for name, value in domains.items()}
    logits = model(tracked, masks)
    gradients = torch.autograd.grad(
        logits.sum(), tuple(tracked.values()), create_graph=True, allow_unused=True
    )
    penalties = []
    for (name, _), gradient in zip(tracked.items(), gradients):
        if name not in signs or gradient is None:
            continue
        sign = torch.as_tensor(signs[name], dtype=gradient.dtype, device=gradient.device).reshape(1, -1)
        if sign.shape[1] != gradient.shape[1]:
            raise ValueError(f"monotonic sign count for {name} does not match its feature count")
        active = sign.abs() > 0
        if active.any():
            violations = torch.relu(-gradient * sign).pow(2)
            penalties.append(violations[:, active.squeeze(0)].mean())
    return torch.stack(penalties).mean() if penalties else next(model.parameters()).new_zeros(())


def fit_care_state(model: CAREState, train_domains: Mapping[str, Tensor],
                   train_masks: Mapping[str, Tensor], train_y: Tensor,
                   train_weight: Tensor, val_domains: Mapping[str, Tensor],
                   val_masks: Mapping[str, Tensor], val_y: Tensor,
                   val_weight: Tensor, *, max_epochs: int = 300,
                   patience: int = 30, learning_rate: float = 2e-3,
                   weight_decay: float = 1e-4, seed: int = 2026,
                   monotonic_signs: Mapping[str, Tensor] | None = None,
                   monotonic_lambda: float = 0.0) -> FitResult:
    """Fit with weighted BCE and validation-only early stopping."""
    if patience < 1 or max_epochs < patience:
        raise ValueError("max_epochs must be at least patience and patience must be positive")
    if monotonic_lambda < 0:
        raise ValueError("monotonic_lambda must be non-negative")
    torch.manual_seed(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    best_state, best_val, best_epoch, stale = None, float("inf"), 0, 0
    history: list[dict[str, float]] = []
    for epoch in range(1, max_epochs + 1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        train_loss = _weighted_bce(model(train_domains, train_masks), train_y, train_weight)
        if monotonic_signs and monotonic_lambda > 0:
            train_loss = train_loss + monotonic_lambda * _monotonic_penalty(
                model, train_domains, train_masks, monotonic_signs
            )
        train_loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            val_loss = _weighted_bce(model(val_domains, val_masks), val_y, val_weight)
        train_value, val_value = float(train_loss), float(val_loss)
        history.append({"epoch": float(epoch), "train_loss": train_value, "val_loss": val_value})
        if val_value < best_val - 1e-7:
            best_val, best_epoch, stale = val_value, epoch, 0
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
        else:
            stale += 1
            if stale >= patience:
                break
    if best_state is None:
        raise RuntimeError("training produced no validation checkpoint")
    model.load_state_dict(best_state)
    return FitResult(best_epoch, best_val, history)


def state_config(model: CAREState) -> dict:
    """Return JSON-serialisable model configuration for checkpoint metadata."""
    return {
        "domain_dims": model.domain_dims,
        "domain_names": list(model.domain_names),
        "hidden_dim": model.encoders[model.domain_names[0]][0].out_features,
        "state_dim": model.state[0].out_features,
        "supports_monotonic_penalty": True,
    }
