# Reference runs

All committed numerical evidence is synthetic and is classified as a Level 0 executable reference. Numerical convergence is not evidence that a real reaction mechanism, thermodynamic model, operating point, or safety boundary is valid.

## Environment

- Command: `PYTHONPATH=src python scripts/run_reference_cases.py`
- Simulator: `chemical_reactor_twin` reduced-order ODE and algebraic models
- Python: 3.12.10
- NumPy: 2.5.1
- SciPy: 1.17.1
- ODE method: BDF for batch and PFR cases
- Units: mol/m3, s, K, Pa, m3, kg/m3, J/(kg K), W/K, J/mol
- Random seed: not applicable for the deterministic reference runs

## R1: smallest meaningful baseline

Synthetic parallel reactions A to B and A to C were simulated in ideal batch, CSTR, and PFR reactors. The feed was 1000 mol/m3 A at 330 K and 101325 Pa. The batch duration was 10 s with volume 0.001 m3 and UA 25 W/K. CSTR and PFR residence time was 10 s with UA/V 25000 W/(m3 K).

| Quantity | Batch | CSTR | PFR |
|---|---:|---:|---:|
| A conversion | 0.933797 | 0.731477 | 0.933797 |
| B selectivity | 0.967347 | 0.967231 | 0.967347 |
| Peak temperature [K] | 334.355616 | 333.356488 | 334.355616 |

- Status: completed
- Runtime: 0.0264 s
- Evidence: `results/reference-runs/baseline.json`
- Scientific limitation: ideal homogeneous models with synthetic kinetics and lumped heat transfer

## R2: physical parameter response

The same 5 s batch case was evaluated with both initial and coolant temperature changed from 320 K to 340 K.

- Conversion at 320 K: 0.688732
- Conversion at 340 K: 0.782871
- Acceptance: passed, conversion increased for the positive activation-energy synthetic network
- Runtime: 0.0126 s
- Evidence: `results/reference-runs/temperature-response.json`
- Safety limitation: this is an Arrhenius response demonstration, not a recommended temperature range

## R3: analytical and conservation validation

An isothermal first-order batch limit used (k = 0.08;s^{-1}), (C_{A,0}=1000;mol/m^3), and the analytical solution (C_A(t)=C_{A,0}exp(-kt)).

- Maximum relative concentration error: 2.68e-9
- Maximum conserved-total error: 4.55e-13 mol/m3
- Acceptance limits: 1e-7 relative error and 1e-6 mol/m3 conservation error
- Acceptance: passed
- Runtime: 0.0099 s
- Evidence: `results/reference-runs/validation.json`
- Limitation: this verifies a mathematical limiting case, not a real mechanism

## R4: intentional invalid input

An initial concentration of -1 mol/m3 was supplied.

- Expected result: rejected
- Actual result: `ValueError: Initial concentrations must be nonnegative`
- Acceptance: passed
- Evidence: `results/reference-runs/invalid-input.json`

## R5: packaged quickstart rerun

The final package is rerun with:

```bash
python -m pip install -e .
python scripts/run_baseline.py
python -m unittest discover -s tests -v
```

The release checklist records the final status after the last repository edit.

## Remote compute

No registered Vicena Compute workflow is scientifically required for these ideal SciPy ODE and algebraic reference cases. No unrelated remote solver was submitted. Higher-fidelity CFD, multiphase, or reactive-flow work would require a separately selected and validated domain workflow, geometry, boundary conditions, and safety basis.

## Compact artifacts

- `results/reference-runs/baseline.json`
- `results/reference-runs/temperature-response.json`
- `results/reference-runs/validation.json`
- `results/reference-runs/invalid-input.json`
- `results/reference-runs/summary.csv`
- `results/reference-runs/console-summary.json`
- `results/reference-runs/final-quickstart.txt`
- `results/reference-runs/final-tests.txt`
- `results/reference-runs/artifact-manifest.json`
