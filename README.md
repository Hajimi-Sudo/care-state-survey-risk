# CARE-State: Survey-Transportable Population Risk State

This repository contains the reproducibility materials accompanying the DIGITAL HEALTH manuscript:

**CARE-State: A Missingness-Aware, Survey-Transportable Population Risk State for Short-Term Mortality Surveillance**

The study uses public NHANES and NHIS survey files with public-use mortality linkage files. It evaluates a missingness-aware, domain-gated population risk state across a frozen NHANES temporal test and an NHIS survey-source transport test. The paper is positioned as a bounded population-surveillance and evidence-audit study, not as a model leaderboard.

## Repository contents

```text
code/
  care_state_model.py          # Domain-gated CARE-State model and early stopping
  metrics.py                   # Survey-weighted evaluation metrics
  calibration.py               # Validation-only logit calibration adapter
  plot_result_figures.py       # Recreates aggregate coverage and calibration figures
  smoke_test.py                # CPU smoke test on generated data
  requirements.txt             # Runtime dependencies
derived_results/
  domain_coverage.csv
  primary_calibration_bins.csv
  README.txt
manuscript_digital_health/
  main.tex
  refs.bib
  *.png                       # Figures referenced by main.tex
EXPERIMENT_RESULTS.md          # Audited aggregate results and claim boundaries
REPRODUCIBILITY_STATUS.md      # Exact scope of the released code
```

## Reproduce the model smoke test

The released model layer runs on harmonised inputs with one feature matrix and
one availability mask per clinical domain, together with the outcome and
survey weight. A small CPU test is included:

```bash
python -m pip install -r code/requirements.txt
python code/smoke_test.py
```

The test uses generated data and does not claim to reproduce the reported
NHANES/NHIS estimates.

## Reproduce aggregate figures

The plotting layer uses only aggregate CSV files and does not download or reconstruct participant-level records.

```bash
python code/plot_result_figures.py
```

The script writes the regenerated coverage and calibration figures to the manuscript figure directory.

## Compile the manuscript

```bash
cd manuscript_digital_health
latexmk -pdf -interaction=nonstopmode main.tex
```

## Data access

All participant-level source files are public-use records maintained by the U.S. National Center for Health Statistics. The exact NHANES, NHIS, and public-use mortality-linkage URLs used by the manuscript are listed in the Data Availability Statement in `manuscript_digital_health/main.tex`.

The original server-side source-data harmonisation pipeline and participant-
level exports are not included. The repository therefore provides the
complete CARE-State model/evaluation implementation for harmonised inputs and
the exact aggregate-result and manuscript reproduction layer, while retaining
the privacy and provenance boundary documented in
`REPRODUCIBILITY_STATUS.md`.

## License

The code and manuscript materials are provided for research and reproducibility purposes. The public datasets remain subject to the terms of their original providers.
