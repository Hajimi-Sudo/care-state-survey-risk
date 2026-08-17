"""Equation-level checks for the released CARE-State reference implementation."""

import torch

from care_state_model import CAREState, _monotonic_penalty


def main() -> None:
    dims = {"demographic": 2, "metabolic": 2}
    model = CAREState(dims, hidden_dim=8, state_dim=8, dropout=0.0).eval()
    domains = {name: torch.randn(6, size) for name, size in dims.items()}
    masks = {name: torch.ones(6) for name in dims}

    hidden_masks = dict(masks)
    hidden_masks["metabolic"] = torch.zeros(6)
    baseline = model(domains, hidden_masks)
    changed = {name: value.clone() for name, value in domains.items()}
    changed["metabolic"] += 100.0
    masked = model(changed, hidden_masks)
    assert torch.allclose(baseline, masked, atol=1e-6)

    penalty = _monotonic_penalty(
        model, domains, masks, {"demographic": torch.tensor([1.0, -1.0])}
    )
    assert torch.isfinite(penalty)
    assert baseline.shape == (6,)
    print("equation smoke test passed")


if __name__ == "__main__":
    main()
