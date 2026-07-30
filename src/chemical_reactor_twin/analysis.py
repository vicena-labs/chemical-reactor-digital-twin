"""Validation, uncertainty propagation, and sensitivity utilities."""
import numpy as np

def validate_prediction(observed, predicted, sigma=None):
    y = np.asarray(observed, float)
    p = np.asarray(predicted, float)
    if y.shape != p.shape:
        raise ValueError("Observed and predicted arrays must have the same shape")
    err = p - y
    scale = np.maximum(np.abs(y), 1e-12)
    out = {"rmse": float(np.sqrt(np.mean(err**2))), "mae": float(np.mean(np.abs(err))),
           "max_abs_error": float(np.max(np.abs(err))), "mean_relative_error": float(np.mean(np.abs(err)/scale)),
           "n": int(y.size)}
    if sigma is not None:
        out["reduced_chi_square"] = float(np.mean((err / np.asarray(sigma))**2))
    return out

def uncertainty_propagation(simulator, samples, output_extractor, seed=7):
    rng = np.random.default_rng(seed)
    values = []
    for sample in samples(rng):
        values.append(np.asarray(output_extractor(simulator(sample)), float))
    a = np.asarray(values)
    return {"mean": np.mean(a, axis=0), "std": np.std(a, axis=0, ddof=1),
            "q05": np.quantile(a, 0.05, axis=0), "q95": np.quantile(a, 0.95, axis=0),
            "n_samples": int(len(a))}

def local_sensitivity(model, parameters, relative_step=1e-3):
    base = np.asarray(model(parameters), float)
    sensitivities = {}
    for name, value in parameters.items():
        step = relative_step * max(abs(value), 1.0)
        plus = dict(parameters); minus = dict(parameters)
        plus[name] = value + step; minus[name] = value - step
        derivative = (np.asarray(model(plus)) - np.asarray(model(minus))) / (2 * step)
        sensitivities[name] = derivative
    return {"base": base, "derivatives": sensitivities}
