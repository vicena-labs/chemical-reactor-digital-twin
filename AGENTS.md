# Agent Instructions

Read this file, AGENT_PLAYBOOK.md, and .agents/skills/chemical-reactor-digital-twin/SKILL.md before edits.

## Scientific rules
- Use SI units internally: mol/m^3, s, K, Pa, m^3, kg/m^3, J/(kg K), W/K, J/mol.
- Never infer units, species identity, stoichiometry, phase, reaction order, activation parameters, heat capacity, density, or reaction enthalpy.
- Check elemental or conserved-moiety balances when molecular formulas or conservation vectors are available.
- Separate calibration, validation, and test data. Never tune on held-out data.
- Print solver method, tolerances, function evaluations, residuals, minimum concentrations, and maximum temperature.
- Numerical convergence does not prove chemical validity. Compare against conservation, limiting cases, measured data, and credible kinetics.
- Use BDF or Radau for suspected stiffness, then test tolerance sensitivity.
- Treat optimization results as research hypotheses until experimentally validated and reviewed for process safety.
- Do not recommend operating conditions for real chemistry without verified material properties, relief design, calorimetry, hazard review, and qualified engineering approval.

## Safety boundary
This reduced-order twin is not a process-hazard analysis, relief-sizing tool, runaway calorimetry substitute, mechanical-integrity assessment, or operating procedure. Escalate real reactive hazards, pressure systems, flammability, toxic releases, unstable intermediates, and scale-up decisions to qualified process-safety personnel.
