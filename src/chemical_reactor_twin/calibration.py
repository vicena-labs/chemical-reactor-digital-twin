"""Parameter estimation and local practical identifiability diagnostics."""
import numpy as np
from scipy.optimize import least_squares
from .models import simulate_batch

def fit_arrhenius_parameters(network, experiments, reaction_index=0, bounds=None):
    base_a = float(network.pre_exponential[reaction_index])
    base_e = float(network.activation_energy[reaction_index])
    x0 = np.array([np.log(base_a), base_e])
    if bounds is None:
        bounds = ([np.log(base_a)-8, 0.0], [np.log(base_a)+8, 300000.0])
    def residual(x):
        network.pre_exponential[reaction_index] = np.exp(x[0])
        network.activation_energy[reaction_index] = x[1]
        out = []
        for exp in experiments:
            sim = simulate_batch(network, exp["c0"], exp["temperature_K"], exp["time_s"][-1],
                                 adiabatic=False, coolant_temperature=exp["temperature_K"],
                                 ua=1e9, n_points=len(exp["time_s"]))
            out.extend((sim.concentration[:, exp["species_index"]] - exp["observed_concentration"]) / exp.get("sigma", 1.0))
        return np.asarray(out)
    fit = least_squares(residual, x0, bounds=bounds, jac="2-point")
    network.pre_exponential[reaction_index] = np.exp(fit.x[0])
    network.activation_energy[reaction_index] = fit.x[1]
    cov = np.full((2, 2), np.nan)
    if fit.jac.shape[0] > fit.jac.shape[1]:
        dof = fit.jac.shape[0] - fit.jac.shape[1]
        cov = np.linalg.pinv(fit.jac.T @ fit.jac) * (2 * fit.cost / dof)
    return {"A": float(np.exp(fit.x[0])), "Ea_J_mol": float(fit.x[1]), "cost": float(fit.cost),
            "success": bool(fit.success), "jacobian": fit.jac, "covariance_transformed": cov}

def identifiability_report(jacobian, parameter_names=("log_A", "Ea_J_mol"), threshold=1e8):
    j = np.asarray(jacobian, dtype=float)
    _, s, _ = np.linalg.svd(j, full_matrices=False)
    condition = float(np.inf if s[-1] == 0 else s[0] / s[-1])
    return {"parameter_names": list(parameter_names), "singular_values": s.tolist(),
            "condition_number": condition, "locally_identifiable": bool(condition < threshold),
            "warning": None if condition < threshold else "Strong parameter correlation or insufficient excitation"}
