# CARE-State Code

The repository includes the model and evaluation layer as well as the figure
generation code. `care_state_model.py` implements domain-specific encoders,
reliability gates, hard availability masks, a shared risk state, a fixed-
horizon risk head, weighted BCE training, validation-only early stopping, and
an optional directional-gradient penalty for prespecified monotonic features.
`metrics.py` implements survey-weighted AUROC, Brier score, fixed-cutpoint risk
strata, and aggregate calibration bins. `calibration.py` implements the
source-specific logit calibration adapter. `equation_smoke_test.py` checks the
hard-mask information path and the directional-penalty interface. The
historical server run's exact signs, feature map, and penalty coefficient are
not included and must not be inferred from this reference implementation.

The model expects a harmonised input table represented as domain feature
matrices, one availability mask per domain, an outcome column, and a survey
weight column. `reference_input_schema.yaml` records this generic input
contract, but it is not the historical NHANES/NHIS variable map. The original
server-side harmonisation script was not recovered from the unavailable
server; no unverified data loader is presented as an exact reproduction of the
reported server run.

Run the CPU smoke test from this directory:

```bash
python smoke_test.py
```

The plotting script reads only aggregate CSV files from `derived_results/` and
regenerates:

- `primary_calibration.pdf/png`
- `domain_coverage_heatmap.pdf/png`
