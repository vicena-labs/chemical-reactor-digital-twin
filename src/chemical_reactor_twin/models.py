"""Mass and energy balance models for ideal batch, CSTR, and PFR reactors.

Numerical convergence is necessary but does not establish chemical validity.
All concentrations are mol/m^3, time is s, temperature is K, pressure is Pa,
volumes are m^3, heat capacity is J/(kg K), density is kg/m^3, and reaction
enthalpy is J/mol of reaction as written.
"""
from dataclasses import dataclass
from typing import Sequence
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

R_GAS = 8.31446261815324

@dataclass
class ReactionNetwork:
    species: Sequence[str]
    stoichiometry: np.ndarray
    pre_exponential: np.ndarray
    activation_energy: np.ndarray
    reaction_orders: np.ndarray
    reaction_enthalpy: np.ndarray

    def __post_init__(self):
        self.stoichiometry = np.asarray(self.stoichiometry, dtype=float)
        self.pre_exponential = np.asarray(self.pre_exponential, dtype=float)
        self.activation_energy = np.asarray(self.activation_energy, dtype=float)
        self.reaction_orders = np.asarray(self.reaction_orders, dtype=float)
        self.reaction_enthalpy = np.asarray(self.reaction_enthalpy, dtype=float)
        nr, ns = self.stoichiometry.shape
        if ns != len(self.species) or self.reaction_orders.shape != (nr, ns):
            raise ValueError("Stoichiometry and reaction orders must be reactions by species")
        if np.any(self.pre_exponential < 0) or np.any(self.activation_energy < 0):
            raise ValueError("Kinetic parameters must be nonnegative")

    def rates(self, concentration, temperature):
        c = np.clip(np.asarray(concentration, dtype=float), 0.0, None)
        k = self.pre_exponential * np.exp(-self.activation_energy / (R_GAS * temperature))
        return k * np.prod(np.power(c[None, :], self.reaction_orders), axis=1)

@dataclass
class ReactorResult:
    coordinate: np.ndarray
    concentration: np.ndarray
    temperature: np.ndarray
    rates: np.ndarray
    diagnostics: dict

def _check_inputs(c0, temperature, pressure, rho, cp):
    c0 = np.asarray(c0, dtype=float)
    if np.any(c0 < 0):
        raise ValueError("Initial concentrations must be nonnegative")
    if temperature <= 0 or pressure <= 0 or rho <= 0 or cp <= 0:
        raise ValueError("Temperature, pressure, density, and heat capacity must be positive")
    return c0

def _method(stiff):
    return "BDF" if stiff else "RK45"

def simulate_batch(network, c0, temperature0, duration, *, pressure=101325.0,
                   density=1000.0, heat_capacity=4180.0, ua=0.0,
                   coolant_temperature=None, volume=1.0, adiabatic=False,
                   stiff=True, n_points=201, rtol=1e-7, atol=1e-9):
    c0 = _check_inputs(c0, temperature0, pressure, density, heat_capacity)
    if duration <= 0 or volume <= 0 or ua < 0:
        raise ValueError("Duration and volume must be positive, UA nonnegative")
    tc = temperature0 if coolant_temperature is None else coolant_temperature
    y0 = np.r_[c0, temperature0]
    def rhs(t, y):
        c = np.clip(y[:-1], 0, None)
        temp = max(y[-1], 1.0)
        rates = network.rates(c, temp)
        dcdt = network.stoichiometry.T @ rates
        q_rxn = -np.dot(network.reaction_enthalpy, rates) * volume
        q_ht = 0.0 if adiabatic else ua * (tc - temp)
        dtdt = (q_rxn + q_ht) / (density * volume * heat_capacity)
        return np.r_[dcdt, dtdt]
    t_eval = np.linspace(0, duration, n_points)
    sol = solve_ivp(rhs, (0, duration), y0, t_eval=t_eval, method=_method(stiff), rtol=rtol, atol=atol)
    conc = np.clip(sol.y[:-1].T, 0, None)
    temps = sol.y[-1]
    rates = np.vstack([network.rates(c, t) for c, t in zip(conc, temps)])
    diag = {"success": bool(sol.success), "message": sol.message, "nfev": sol.nfev,
            "njev": getattr(sol, "njev", 0), "method": _method(stiff),
            "rtol": rtol, "atol": atol, "min_concentration": float(conc.min()),
            "max_temperature_K": float(temps.max())}
    if not sol.success:
        raise RuntimeError(f"Batch integration failed: {sol.message}")
    return ReactorResult(sol.t, conc, temps, rates, diag)

def simulate_cstr(network, feed_concentration, feed_temperature, residence_time, *,
                  pressure=101325.0, density=1000.0, heat_capacity=4180.0,
                  ua_over_volume=0.0, coolant_temperature=None, adiabatic=False,
                  initial_guess=None):
    cf = _check_inputs(feed_concentration, feed_temperature, pressure, density, heat_capacity)
    if residence_time <= 0 or ua_over_volume < 0:
        raise ValueError("Residence time must be positive and UA/V nonnegative")
    tc = feed_temperature if coolant_temperature is None else coolant_temperature
    guess = np.r_[cf if initial_guess is None else initial_guess[:-1],
                  feed_temperature if initial_guess is None else initial_guess[-1]]
    def residual(y):
        c = np.clip(y[:-1], 0, None)
        temp = max(y[-1], 1.0)
        rates = network.rates(c, temp)
        mass = (cf - c) / residence_time + network.stoichiometry.T @ rates
        q_rxn_v = -np.dot(network.reaction_enthalpy, rates)
        q_ht_v = 0.0 if adiabatic else ua_over_volume * (tc - temp)
        energy = (feed_temperature - temp) / residence_time + (q_rxn_v + q_ht_v) / (density * heat_capacity)
        return np.r_[mass, energy]
    fit = least_squares(residual, guess, bounds=(np.r_[np.zeros(len(cf)), 1.0], np.full(len(cf)+1, np.inf)))
    c = fit.x[:-1]
    temp = fit.x[-1]
    rates = network.rates(c, temp)[None, :]
    diag = {"success": bool(fit.success), "message": fit.message, "nfev": fit.nfev,
            "residual_norm": float(np.linalg.norm(fit.fun)), "solver": "least_squares",
            "max_temperature_K": float(temp)}
    return ReactorResult(np.array([residence_time]), c[None, :], np.array([temp]), rates, diag)

def simulate_pfr(network, feed_concentration, feed_temperature, residence_time, *,
                 pressure=101325.0, density=1000.0, heat_capacity=4180.0,
                 ua_over_volume=0.0, coolant_temperature=None, adiabatic=False,
                 stiff=True, n_points=201, rtol=1e-7, atol=1e-9):
    cf = _check_inputs(feed_concentration, feed_temperature, pressure, density, heat_capacity)
    if residence_time <= 0 or ua_over_volume < 0:
        raise ValueError("Residence time must be positive and UA/V nonnegative")
    tc = feed_temperature if coolant_temperature is None else coolant_temperature
    def rhs(tau, y):
        c = np.clip(y[:-1], 0, None)
        temp = max(y[-1], 1.0)
        rates = network.rates(c, temp)
        dc = network.stoichiometry.T @ rates
        q_rxn_v = -np.dot(network.reaction_enthalpy, rates)
        q_ht_v = 0.0 if adiabatic else ua_over_volume * (tc - temp)
        dtemp = (q_rxn_v + q_ht_v) / (density * heat_capacity)
        return np.r_[dc, dtemp]
    tau = np.linspace(0, residence_time, n_points)
    sol = solve_ivp(rhs, (0, residence_time), np.r_[cf, feed_temperature], t_eval=tau,
                    method=_method(stiff), rtol=rtol, atol=atol)
    if not sol.success:
        raise RuntimeError(f"PFR integration failed: {sol.message}")
    conc = np.clip(sol.y[:-1].T, 0, None)
    temps = sol.y[-1]
    rates = np.vstack([network.rates(c, t) for c, t in zip(conc, temps)])
    diag = {"success": True, "message": sol.message, "nfev": sol.nfev,
            "njev": getattr(sol, "njev", 0), "method": _method(stiff),
            "rtol": rtol, "atol": atol, "max_temperature_K": float(temps.max())}
    return ReactorResult(sol.t, conc, temps, rates, diag)
