# API

- `ReactionNetwork`: stoichiometry, Arrhenius parameters, reaction orders, and reaction enthalpies.
- `simulate_batch`: transient ideal batch mass and energy balances.
- `simulate_cstr`: steady ideal CSTR algebraic balances.
- `simulate_pfr`: residence-time coordinate ideal PFR balances.
- `fit_arrhenius_parameters`: least-squares estimation of one Arrhenius pair.
- `identifiability_report`: Jacobian singular-value diagnostic.
- `validate_prediction`: held-out error metrics.
- `uncertainty_propagation`: Monte Carlo summary.
- `local_sensitivity`: centered finite-difference sensitivities.
- `optimize_operating_conditions`: constrained research optimization.
