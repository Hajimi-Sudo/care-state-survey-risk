# CARE-State Code

The repository includes the model and evaluation layer as well as the figure
generation code. `care_state_model.py` implements domain-specific encoders,
reliability gates, hard availability masks, a shared risk state, a fixed-
horizon risk head, weighted BCE training, and validation-only early stopping.
`metrics.py` implements survey-weighted AUROC, Brier score, fixed-cutpoint risk
strata, and aggregate calibration bins. `calibration.py` implements the
source-specific logit calibration adapter.

The model expects a harmonised input table represented as domain feature
matrices, one availability mask per domain, an outcome column, and a survey
weight column. The original server-side NHANES/NHIS harmonisation script was
not recovered from the unavailable server; no unverified data loader is
presented as an exact reproduction of the reported server run.

Run the CPU smoke test from this directory:

```bash
python smoke_test.py
```

The plotting script reads only aggregate CSV files from `derived_results/` and
regenerates:

- `primary_calibration.pdf/png`
- `domain_coverage_heatmap.pdf/png`
