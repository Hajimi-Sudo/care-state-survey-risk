# CARE-State cardiorenal direction: experiment closeout

## Scope

This report records aggregate-only results from the CARE-State server
experiment. Raw NHANES rows and identifiers remain on the server; no
individual-level data are copied into this manuscript directory.

The study uses public NHANES cycles 2007-2008 through 2015-2016 for model
development, validation, and temporal testing. A separate 2017-2018 cycle was
used only after model freezing for an external temporal check.

## Data audit

- Five development/test cycles: 29,571 eligible participants and 3,135 all-cause events.
- Common feature map: demographic, metabolic, cardiovascular, and renal domains.
- Main 36-month test: 5,710 participants and 186 events.
- 2017-2018 linked sample: 5,495 participants; median follow-up 24 months.
- The 2019 mortality linkage does not provide a comparable 36-month horizon for all 2017-2018 participants.

## Frozen 36-month results

Across three seeds on the 2015-2016 temporal test:

| Model | AUROC mean +/- SD | Brier mean +/- SD |
|---|---:|---:|
| CARE-State | 0.8719 +/- 0.0018 | 0.0208 +/- 0.0001 |
| Weighted Cox | 0.7857 +/- 0.0000 | 0.0226 +/- 0.0000 |
| Weighted GBM | 0.8671 +/- 0.0058 | 0.0207 +/- 0.0003 |

The full CARE-State model does not outperform the `no_gate` or
`no_monotonic` ablations on AUROC. The clinical gate and monotonic constraints
must therefore be presented as interpretability and clinical-ordering
mechanisms, not as proven discrimination improvements.

The frozen CARE-State risk strata preserved monotonic ordering on the 2015-
2016 test: weighted event rates were approximately 0.002, 0.011, and 0.104.

## 24-month external temporal check

The 24-month follow-up sensitivity was trained with the same train/validation
boundary and early-stopping protocol, with three seeds. The frozen models were
then evaluated on NHANES 2017-2018; calibration parameters came only from the
2013-2014 validation cycle.

- External evaluation: 2,910 participants and 110 24-month events.
- CARE-State AUROC: 0.8293, 0.8319, and 0.8324 across seeds.
- Weighted GBM AUROC: 0.8195.
- Weighted Cox AUROC: 0.7493 raw, 0.7514 after validation-only calibration.
- CARE-State risk-stratum event rates were approximately 0.0038, 0.0141, and 0.0876.

The three-seed CARE-State ensemble was numerically above GBM by 0.0127 AUROC,
but the paired participant bootstrap 95% CI was -0.0080 to 0.0358. Against
Cox, the AUROC difference was 0.0809 (95% CI 0.0534 to 0.1094). Therefore the
claim is bounded: stable external risk ordering and competitive discrimination,
not statistically established superiority over GBM.

## Missingness stress

On the 2015-2016 test, masking one domain at inference time gave the following
three-seed CARE-State means:

| Masked domain | AUROC mean +/- SD | Brier mean +/- SD |
|---|---:|---:|
| Cardiovascular | 0.8757 +/- 0.0016 | 0.0209 +/- 0.0001 |
| Demographic | 0.7037 +/- 0.0091 | 0.0224 +/- 0.0003 |
| Metabolic | 0.8731 +/- 0.0011 | 0.0228 +/- 0.0010 |
| Renal | 0.8553 +/- 0.0012 | 0.0252 +/- 0.0013 |

These are stress tests, not evidence that a missing domain improves the model.

## Interpretability and coverage aggregates

The frozen CARE-State post-hoc export was reduced to aggregate calibration
deciles for the primary temporal test. The resulting calibration audit is
stored in `derived_results/primary_calibration_bins.csv`; participant-level
predictions and identifiers are not copied into this manuscript directory.

The audited feature map was also summarized by NHANES cycle and clinical
domain. Mean weighted observed-variable coverage across the five cycles was
98.2% for demographic, 96.8% for metabolic, 96.5% for cardiovascular, and
96.4% for renal variables. These coverage values describe data availability;
they are not outcome or model-performance estimates.

## Decision and claim boundary

The experiment block is complete enough for manuscript drafting and external
review. Do not spend more GPU time on repeated seeds or a larger leaderboard.
The defensible contribution is a missingness-aware, domain-gated clinical risk
state with frozen temporal evaluation and external time-period checking. The
study supports association and bounded prospective risk prediction on the
tested NHANES cycles. It does not support causal claims, clinical deployment,
universal generalization, or proven superiority over every nonlinear baseline.

## Independent external-source validation

An additional external-source analysis used NHIS public-use adult samples and
the NHIS 2019 public mortality linkage. NHIS 2016 was used only to fit the
prespecified two-parameter cohort calibration adapter; the frozen model was
not retrained. NHIS 2017 was held out for the final external test.

- NHIS 2016 calibration cohort: 32,487 adults and 797 24-month events.
- NHIS 2017 external test cohort: 26,267 adults and 656 24-month events.
- NHIS 2017 AUROC after adaptation: 0.8468, 0.8507, and 0.8476 across seeds.
- Direct NHANES calibration gave the same discrimination but substantially worse Brier scores, approximately 0.0221-0.0277 versus 0.0173-0.0175 after NHIS calibration.
- Adapted risk-stratum event rates were approximately 0.002, 0.009, and 0.055.
- Paired bootstrap Brier changes for the three seeds were -0.0102, -0.0055,
  and -0.0048; every 95% interval remained below zero.

This is a genuine external-source validation relative to NHANES, with a
separate NHIS test year. Its scope is deliberately bounded: NHIS lacks several
NHANES laboratory fields and uses a different race coding system, so the
analysis validates transport of the missingness-aware risk state and its
cohort-specific calibration adapter under a reduced self-report/BMI feature
intersection. It does not establish validity of the full laboratory-rich
feature map in every population.

## Server artifacts

The server retains the audited data, model checkpoints, ablations, and
participant-level prediction files. This local project intentionally stores
only aggregate results and manuscript sources. The server handoff should map
the following artifact roles to the current CARE-State workspace before
submission: data audit, three-seed primary results, structural ablations,
NHANES 2017--2018 temporal check, NHIS calibration audit, and NHIS
2016-to-2017 transport check.
