# CARE-State: Survey-Transportable Population Risk State

This repository contains the reproducibility materials accompanying the DIGITAL HEALTH manuscript:

**CARE-State: A Missingness-Aware, Survey-Transportable Population Risk State for Short-Term Mortality Surveillance**

The study uses public NHANES and NHIS survey files with public-use mortality linkage files. It evaluates a missingness-aware, domain-gated population risk state across a frozen NHANES temporal test and an NHIS survey-source transport test. The paper is positioned as a bounded population-surveillance and evidence-audit study, not as a model leaderboard.

## Repository contents

```text
code/
  plot_result_figures.py       # Recreates the aggregate coverage and calibration figures
  requirements.txt
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

## Reproduce aggregate figures

The plotting layer uses only aggregate CSV files and does not download or reconstruct participant-level records.

```bash
python -m pip install -r code/requirements.txt
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

## License

The code and manuscript materials are provided for research and reproducibility purposes. The public datasets remain subject to the terms of their original providers.
