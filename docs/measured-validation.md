# Measured silica-polymerization validation

## Scope

Release 0.2.0 adds measured-data evidence for within-experiment time extrapolation across 61 silica-polymerization experiments. The generic batch, CSTR, PFR, energy-balance, and optimization lanes remain Level 0.

The normalized fourth-order model is `y(t) = (1 + 3 k t)^(-1/3)`, where `y` is monomeric silica divided by its initial measured value. A normalized first-order decay is the comparator.

## Protocol

Within each experiment, the earliest 60 percent of observations fit the rate constant, the next 20 percent calibrate an empirical residual interval, and the final 20 percent are untouched late-time tests. This is a time-extrapolation test within each condition, not a test on unseen temperatures, pH values, ionic strengths, reactor scales, or chemistries.

Quality gates require numeric nonnegative time, positive concentration, unique time values, and at least eight valid observations per experiment.

## Held-out result

- Usable experiments: 61.
- Median fourth-order normalized RMSE: 0.1710.
- Median first-order normalized RMSE: 0.3077.
- Fourth-order model lower RMSE: 51 of 61 experiments.
- Median RMSE improvement: 44.42 percent.
- Median empirical 90 percent interval coverage: 0.1000.

The very poor interval coverage shows strong late-time model drift or nonstationary residuals. Therefore this release demonstrates measured benchmarking and a useful model comparison, but it does not support a robust predictive, mechanistic, scale-up, or safety claim.

## Reproduction

Download and verify the workbook, place it under `datasets/external`, then run `PYTHONPATH=src python scripts/run_measured_validation.py datasets/external/SupplementaryData_SilicaPolymerization.xlsx --output outputs/measured_silica`.
