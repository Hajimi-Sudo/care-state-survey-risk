# Reproducibility Status

## Included

- Aggregate result tables used in the manuscript.
- Figure-generation code for the aggregate coverage and calibration figures.
- The final DIGITAL HEALTH LaTeX source, bibliography, and PNG figures.
- The audited experiment summary and claim boundaries.

## Not included

- Individual-level NHANES or NHIS records.
- Credentials, server paths, or private data.
- The original server-side training and data-preparation pipeline.
- Model checkpoints or participant-level prediction exports.

The released repository is therefore an **aggregate-result and manuscript reproducibility package**, not a complete retraining environment. The manuscript's Code Availability Statement uses the same boundary. Releasing a complete retraining implementation requires exporting and reviewing the verified server-side code, configuration, preprocessing map, and risk-stratum cutpoint definitions; none of those artifacts are inferred or fabricated here.
