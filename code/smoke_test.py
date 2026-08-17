"""Small CPU smoke test for the released CARE-State implementation."""

import numpy as np
import torch

from care_state_model import CAREState, fit_care_state
from metrics import weighted_auroc, weighted_brier


def main() -> None:
    generator = np.random.default_rng(7)
    domain_dims = {"demographic": 3, "metabolic": 4, "cardiovascular": 2, "renal": 3}

    def make(n):
        x = {name: torch.tensor(generator.normal(size=(n, dim)), dtype=torch.float32) for name, dim in domain_dims.items()}
        m = {name: torch.tensor(generator.binomial(1, 0.85, size=n), dtype=torch.float32) for name in domain_dims}
        score = 0.8 * x["demographic"][:, 0] + 0.7 * x["renal"][:, 0] + 0.2 * x["metabolic"][:, 1]
        y = torch.bernoulli(torch.sigmoid(score - 1.0))
        return x, m, y, torch.ones(n)

    train, val = make(320), make(120)
    model = CAREState(domain_dims, hidden_dim=16, state_dim=24, dropout=0.0)
    result = fit_care_state(model, *train, *val, max_epochs=40, patience=8, seed=7)
    probability = model.predict_proba(val[0], val[1]).numpy()
    assert np.isfinite(weighted_auroc(val[2].numpy(), probability, val[3].numpy()))
    assert np.isfinite(weighted_brier(val[2].numpy(), probability, val[3].numpy()))
    print(f"smoke test passed; best_epoch={result.best_epoch}; val_loss={result.best_val_loss:.4f}")


if __name__ == "__main__":
    main()
