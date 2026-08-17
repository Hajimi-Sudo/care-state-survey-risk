"""Validation-only probability-scale adaptation."""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize


class LogitCalibrator:
    """Fit logit(p_cal) = intercept + slope * logit(p_raw)."""

    def __init__(self, intercept=0.0, slope=1.0) -> None:
        self.intercept, self.slope = float(intercept), float(slope)

    def fit(self, probability, y_true, weight=None):
        p = np.clip(np.asarray(probability, dtype=float), 1e-6, 1 - 1e-6)
        y = np.asarray(y_true, dtype=float)
        w = np.ones_like(y) if weight is None else np.asarray(weight, dtype=float)
        x = np.column_stack([np.ones_like(p), np.log(p / (1 - p))])

        def objective(theta):
            logits = x @ theta
            loss = np.logaddexp(0, logits) - y * logits
            return float(np.average(loss, weights=w))

        result = minimize(objective, np.array([0.0, 1.0]), method="BFGS")
        if not result.success:
            raise RuntimeError(f"calibration optimisation failed: {result.message}")
        self.intercept, self.slope = map(float, result.x)
        return self

    def predict(self, probability):
        p = np.clip(np.asarray(probability, dtype=float), 1e-6, 1 - 1e-6)
        logits = self.intercept + self.slope * np.log(p / (1 - p))
        return 1 / (1 + np.exp(-logits))
