"""Constrained research optimization for ideal-reactor hypotheses."""
import numpy as np
from scipy.optimize import differential_evolution

def optimize_operating_conditions(evaluator, bounds, constraints, weights=None, seed=11):
    names = list(bounds)
    weights = weights or {"conversion": 1.0, "selectivity": 1.0, "throughput": 0.2, "heat_duty": 0.1}
    scales = {"conversion": 1.0, "selectivity": 1.0, "throughput": 1.0, "heat_duty": 1.0}
    def objective(x):
        m = evaluator(dict(zip(names, x)))
        penalty = 0.0
        for key, (lo, hi) in constraints.items():
            if m[key] < lo: penalty += 1e3 * (lo - m[key])**2
            if m[key] > hi: penalty += 1e3 * (m[key] - hi)**2
        utility = (weights["conversion"] * m["conversion"] / scales["conversion"] +
                   weights["selectivity"] * m["selectivity"] / scales["selectivity"] +
                   weights["throughput"] * m["throughput"] / scales["throughput"] -
                   weights["heat_duty"] * abs(m["heat_duty"]) / scales["heat_duty"])
        return -utility + penalty
    result = differential_evolution(objective, [bounds[n] for n in names], seed=seed, polish=True)
    metrics = evaluator(dict(zip(names, result.x)))
    return {"parameters": dict(zip(names, map(float, result.x))), "metrics": metrics,
            "objective": float(result.fun), "success": bool(result.success),
            "status": "research hypothesis, requires experimental validation and process-safety review"}
