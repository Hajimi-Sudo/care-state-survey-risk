# Reproducibility Status

## Included

- Aggregate result tables used in the manuscript.
- CARE-State model implementation with domain gates and availability masks.
- Reference input-schema template and equation-level smoke test.
- Weighted evaluation metrics, calibration adapter, validation-only early
  stopping, and a CPU smoke test for the released model code.
- Figure-generation code for the aggregate coverage and calibration figures.
- The final DIGITAL HEALTH LaTeX source, bibliography, and PNG figures.
- The audited experiment summary and claim boundaries.

## Not included

- Individual-level NHANES or NHIS records.
- Credentials, server paths, or private data.
- The original server-side NHANES/NHIS data-preparation and harmonisation
  pipeline.
- Model checkpoints or participant-level prediction exports.
- The verified historical feature dictionary, preprocessing configuration,
  directional-sign map, and risk-stratum cutpoints.

The released repository contains a complete implementation of the published
CARE-State model and evaluation layer for harmonised input tables, plus the
aggregate-result and manuscript reproduction layer. Exact end-to-end
retraining on the reported NHANES/NHIS cohorts still requires the verified
source-specific harmonisation map, preprocessing configuration, checkpoints,
and risk-stratum cutpoints from the original server run. Those artifacts are
not inferred or fabricated here.
