"""Survey-weighted metrics used by the CARE-State evaluation."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


def weighted_auroc(y_true, probability, weight) -> float:
    y = np.asarray(y_true).astype(int)
    p = np.asarray(probability, dtype=float)
    w = np.asarray(weight, dtype=float)
    if np.unique(y).size < 2:
        return float("nan")
    return float(roc_auc_score(y, p, sample_weight=w))


def weighted_brier(y_true, probability, weight) -> float:
    y = np.asarray(y_true, dtype=float)
    p = np.asarray(probability, dtype=float)
    w = np.asarray(weight, dtype=float)
    return float(np.average((y - p) ** 2, weights=w))


def weighted_stratum_rates(y_true, probability, weight, cutpoints=(1 / 3, 2 / 3)) -> pd.DataFrame:
    """Return rates using fixed development cutpoints, not test quantiles."""
    y, p, w = (np.asarray(value, dtype=float) for value in (y_true, probability, weight))
    groups = np.digitize(p, np.asarray(cutpoints, dtype=float), right=False)
    rows = []
    for group in range(len(cutpoints) + 1):
        keep = groups == group
        rows.append({
            "stratum": group + 1,
            "n": int(keep.sum()),
            "weighted_n": float(w[keep].sum()),
            "event_rate": float(np.average(y[keep], weights=w[keep])) if keep.any() and w[keep].sum() > 0 else np.nan,
        })
    return pd.DataFrame(rows)


def calibration_bins(y_true, probability, weight, bins=10) -> pd.DataFrame:
    """Aggregate weighted calibration bins without retaining participant rows."""
    y, p, w = (np.asarray(value, dtype=float) for value in (y_true, probability, weight))
    order = np.argsort(p, kind="mergesort")
    rows = []
    for bin_id, indices in enumerate(np.array_split(order, bins), start=1):
        if len(indices) == 0:
            continue
        rows.append({
            "bin": bin_id,
            "n": len(indices),
            "weighted_predicted": float(np.average(p[indices], weights=w[indices])),
            "weighted_observed": float(np.average(y[indices], weights=w[indices])),
        })
    return pd.DataFrame(rows)
