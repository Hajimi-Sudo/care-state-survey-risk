# Figure Generation Code

`plot_result_figures.py` regenerates the two post-processing figures used by the DIGITAL HEALTH manuscript:

- `primary_calibration.pdf/png`
- `domain_coverage_heatmap.pdf/png`

The script reads only aggregate CSV files from `derived_results/` and writes outputs to `manuscript_digital_health/`. It does not download public data, access a server, or reconstruct participant-level records.
