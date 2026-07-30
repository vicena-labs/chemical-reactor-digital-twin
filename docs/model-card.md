# Model card and scientific status

## Implemented
Ideal homogeneous batch, steady CSTR, and ideal PFR models with concentration-dependent Arrhenius kinetics, sensible heat accumulation, reaction heat, and lumped heat transfer.

## Validation level
Level 0 executable reference. Tests cover conservation for a simple stoichiometric system, zero-time and no-reaction limits, CSTR residual closure, and the expected first-order PFR versus CSTR ordering.

## Required measured inputs
Reaction network, kinetic form, parameter provenance, feeds, reactor volume, residence time, temperature, pressure, density, heat capacity, heat-transfer parameters, sensor metadata, and declared data splits.

## Excluded physics
Nonideal mixing, residence-time distributions, axial dispersion, gas-liquid and liquid-solid mass transfer, catalyst deactivation, precipitation, fouling, detailed phase equilibrium, compressibility, pressure drop, geometry-resolved heat transfer, scale-dependent mixing, relief behavior, and thermal runaway onset.

## Claim boundary
A successful solve indicates numerical execution only. Chemical validity requires independent stoichiometric review, thermodynamic consistency, parameter provenance, experimental comparison, uncertainty analysis, and safety review.
