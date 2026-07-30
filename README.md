<div align="center">
  <a href="https://vicena.ai"><strong>Vicena</strong></a>
  <p><strong>Built with Vicena</strong></p>
  <p>Vicena is a scientific research workspace that combines AI-assisted research, durable project files, Jupyter notebooks, reproducible computation, literature tools, and protected remote scientific compute in one environment.</p>
</div>

---

# Chemical Reactor Digital Twin

An open-source, vendor-neutral, calibratable R&D digital twin for ideal laboratory and pilot-scale batch reactors, continuous stirred-tank reactors (CSTRs), and plug-flow reactors (PFRs). The repository combines transparent mass and energy balances, Arrhenius reaction networks, parameter estimation, identifiability, held-out validation, uncertainty propagation, sensitivity analysis, and constrained research optimization.

[Installation](#installation) | [Quick start](#60-second-example) | [Upload data](#upload-your-own-data) | [Notebooks](#notebooks) | [Scientific status](#scientific-status) | [Safety](#safety-and-limitations) | [Citation](#citation) | [AI agent](#use-this-repository-with-an-ai-agent) | [License](#license)

[![One-page overview](assets/chemical-reactor-digital-twin-onepager.png)](Chemical_Reactor_Digital_Twin_OnePager.pdf)

## What release 0.1.0 provides

- Configurable ideal batch, steady CSTR, and ideal PFR models.
- Reaction networks with general stoichiometry, power-law orders, Arrhenius parameters, and reaction enthalpies.
- Concentration and lumped-temperature balances with heat transfer.
- Uploaded concentration or spectroscopy time-series metadata contracts.
- Kinetic parameter estimation, local identifiability, and covariance diagnostics.
- Held-out validation metrics, Monte Carlo uncertainty propagation, local sensitivity, and constrained optimization.
- Stiff integration through SciPy BDF, explicit tolerances, and solver diagnostics.
- Synthetic abstract reactions, reproducible notebooks, conservation tests, and limiting-case tests.

## Scientific status

This is a Level 0 executable reference model. The bundled A to B or C network and measurements are synthetic. They demonstrate architecture and numerical behavior, not validated chemistry. Numerical convergence is not chemical validity. Product-specific claims require measured calibration data, held-out validation, verified properties, parameter provenance, and appropriate safety review.

## Installation

Supported on Linux, macOS, and Windows with Python 3.10 or newer.

```bash
git clone https://github.com/vicena-ai/chemical-reactor-digital-twin.git
cd chemical-reactor-digital-twin
python -m venv .venv
python -m pip install -e .
```

## 60-second example

```bash
python scripts/run_baseline.py
```

Expected result: JSON summaries for batch, CSTR, and PFR cases, including conversion, selectivity, outlet temperature, solver method, tolerances, residuals, and function evaluations.

## 10-minute quickstart

```bash
python scripts/validate_dataset.py datasets/synthetic/reaction_network.yaml schemas/reaction-network.schema.json
python scripts/validate_dataset.py datasets/synthetic/experiment.yaml schemas/experiment.schema.json
python scripts/generate_synthetic_data.py
python scripts/run_baseline.py
python -m unittest discover -s tests -v
```

Then open `notebooks/01_quickstart.ipynb`. See [docs/getting-started.md](docs/getting-started.md).

## Upload your own data

1. Copy uploaded files into a new `projects/<project-name>/data/` folder.
2. Preserve originals unchanged.
3. Create a reaction manifest and experiment manifest using [schemas](schemas/).
4. Declare every column, unit, species mapping, acquisition condition, preprocessing step, and calibration role.
5. Validate both manifests before analysis.

Do not guess missing units, species identities, stoichiometry, phase, sensor settings, baseline corrections, or experimental conditions. Spectroscopy data must have a separately validated calibration model before being interpreted as concentrations.

## Expected artifacts

Analyses should write versioned results under `outputs/<run-id>/`, including normalized inputs, parameter estimates, covariance and identifiability, held-out metrics, solver diagnostics, uncertainty intervals, sensitivities, optimization constraints, provenance, and limitations.

## Notebooks

- `01_quickstart.ipynb`: batch, CSTR, PFR, diagnostics, and plots.
- `02_kinetics_fitting.ipynb`: Arrhenius fitting and identifiability.
- `03_validation.ipynb`: held-out metrics and residual inspection.
- `04_sensitivity.ipynb`: local sensitivity and uncertainty propagation.
- `05_optimization.ipynb`: constrained multi-objective research optimization.

## Extension contract

Add reusable kinetics and reactor models under `src/chemical_reactor_twin/`, stable schemas under `schemas/`, abstract examples under `datasets/synthetic/`, product-specific work under `case_studies/`, and tests for conservation, invalid inputs, limiting cases, tolerance sensitivity, and held-out comparisons. Do not hide infrastructure or assumptions in notebooks.

## Safety and limitations

This repository does not provide operating instructions. Optimization outputs are research hypotheses only and must be validated experimentally and reviewed for process safety.

The baseline does not resolve nonideal mixing, residence-time distributions, axial dispersion, gas-liquid or liquid-solid mass transfer, catalyst deactivation, phase behavior, precipitation, fouling, pressure drop, geometry, scale-dependent heat transfer, relief design, mechanical integrity, decomposition, ignition, or thermal-runaway onset. It is not a substitute for reaction calorimetry, hazard and operability studies, layers-of-protection analysis, relief-system design, or qualified engineering review.

## Numerical diagnostics

Use BDF for suspected stiffness and compare with tighter tolerances or Radau when necessary. Record solver status, message, method, relative and absolute tolerances, function and Jacobian evaluations, residual norms, negative-state excursions, and peak temperatures. A successful solver exit proves execution only.

## Versioning and compatibility

The default branch documents the current development version. Tagged releases, examples, notebooks, schemas, and CHANGELOG.md must remain mutually compatible. Current version: 0.1.0.

## Citation

Use [CITATION.cff](CITATION.cff) for the software. Also cite every kinetic, thermodynamic, transport, spectroscopy, and experimental source used in a project. The synthetic example has no claim to represent a real reaction.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [RELEASE.md](RELEASE.md).

## Use this repository with an AI agent

Short prompt:

```text
Clone https://github.com/vicena-ai/chemical-reactor-digital-twin.git. Read AGENTS.md, AGENT_PLAYBOOK.md, and the repository skill under .agents/skills/. Run the documented smoke test and baseline example without changing the model. Summarize what is implemented, what is synthetic, what has been validated, and what data are required to adapt the twin. Then ask me for the dataset or engineering objective before making scientific changes.
```

Adaptation prompt:

```text
Clone https://github.com/vicena-ai/chemical-reactor-digital-twin.git and treat it as an existing scientific software project. Read AGENTS.md, AGENT_PLAYBOOK.md, the repository skill, the data contract, model card, and validation guidance. Verify the environment, run the tests, and reproduce the baseline output first. Validate my uploaded data against the documented schema without guessing missing units, species identities, stoichiometry, phases, component properties, acquisition settings, or experimental conditions. Create a new project or case study rather than overwriting the reference example. Calibrate only on the declared calibration split, evaluate on held-out data, report identifiability, uncertainty, solver diagnostics, conservation, safety limitations, and preserve reproducibility. Treat optimization as a research hypothesis, not an operating recommendation.
```

## Using this repository with Vicena

Open [Vicena.ai](https://vicena.ai), paste `https://github.com/vicena-ai/chemical-reactor-digital-twin.git`, and ask Vicena to clone it, read `AGENTS.md`, read the repository skill, run tests, and summarize the scientific validation boundary before adaptation. Local features remain standard Python workflows and do not require a Vicena account.

## License

MIT. See [LICENSE](LICENSE). Third-party datasets and models retain their own licenses and must not be redistributed without permission.
