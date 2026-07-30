"""Execute compact, deterministic reference cases and preserve evidence."""
from __future__ import annotations
from pathlib import Path
import csv, hashlib, json, platform, sys, time
import numpy as np
import scipy
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from chemical_reactor_twin import ReactionNetwork, simulate_batch, simulate_cstr, simulate_pfr

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "reference-runs"
OUT.mkdir(parents=True, exist_ok=True)

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def timed(fn):
    start = time.perf_counter()
    value = fn()
    return value, time.perf_counter() - start

def metrics(result, feed_a=1000.0):
    a, b, c = result.concentration[-1]
    products = b + c
    return {
        "conversion": float(1.0 - a / feed_a),
        "selectivity_B": float(b / max(products, 1e-15)),
        "outlet_temperature_K": float(result.temperature[-1]),
        "peak_temperature_K": float(np.max(result.temperature)),
        "solver_diagnostics": result.diagnostics,
    }

network = ReactionNetwork(
    ["A", "B", "C"],
    [[-1, 1, 0], [-1, 0, 1]],
    [20.0, 2.0],
    [12000.0, 15000.0],
    [[1, 0, 0], [1, 0, 0]],
    [-20000.0, -30000.0],
)
feed = np.array([1000.0, 0.0, 0.0])

def baseline_case():
    batch = simulate_batch(network, feed, 330.0, 10.0, volume=0.001, ua=25.0, coolant_temperature=330.0)
    cstr = simulate_cstr(network, feed, 330.0, 10.0, ua_over_volume=25000.0, coolant_temperature=330.0)
    pfr = simulate_pfr(network, feed, 330.0, 10.0, ua_over_volume=25000.0, coolant_temperature=330.0)
    return {"batch": metrics(batch), "cstr": metrics(cstr), "pfr": metrics(pfr)}

baseline, baseline_runtime = timed(baseline_case)
baseline_record = {
    "case": "baseline",
    "status": "completed",
    "command": "python scripts/run_reference_cases.py",
    "simulator": "chemical_reactor_twin reduced-order ODE and algebraic models",
    "python_version": platform.python_version(),
    "numpy_version": np.__version__,
    "scipy_version": scipy.__version__,
    "inputs": {
        "species": ["A", "B", "C"],
        "feed_concentration_mol_m3": feed.tolist(),
        "temperature_K": 330.0,
        "pressure_Pa": 101325.0,
        "batch_duration_s": 10.0,
        "continuous_residence_time_s": 10.0,
        "batch_UA_W_K": 25.0,
        "continuous_UA_over_volume_W_m3_K": 25000.0,
        "synthetic_network": True,
    },
    "runtime_s": baseline_runtime,
    "results": baseline,
    "maturity": "Level 0 executable reference",
    "limitations": "Ideal homogeneous reactors, synthetic kinetics, lumped heat transfer, no scale-up or process-safety claim.",
}

def response_case():
    cool = simulate_batch(network, feed, 320.0, 5.0, volume=0.001, ua=25.0, coolant_temperature=320.0)
    warm = simulate_batch(network, feed, 340.0, 5.0, volume=0.001, ua=25.0, coolant_temperature=340.0)
    return {"cool_320_K": metrics(cool), "warm_340_K": metrics(warm)}

response, response_runtime = timed(response_case)
response_record = {
    "case": "temperature_response",
    "status": "completed",
    "command": "python scripts/run_reference_cases.py",
    "changed_parameter": {"initial_and_coolant_temperature_K": [320.0, 340.0]},
    "duration_s": 5.0,
    "runtime_s": response_runtime,
    "results": response,
    "acceptance": {
        "criterion": "Higher temperature increases conversion for the positive activation-energy synthetic network.",
        "passed": response["warm_340_K"]["conversion"] > response["cool_320_K"]["conversion"],
    },
    "limitations": "This is a qualitative Arrhenius response check, not a safe operating-temperature recommendation.",
}

def validation_case():
    k = 0.08
    duration = 25.0
    net = ReactionNetwork(["A", "B"], [[-1, 1]], [k], [0.0], [[1, 0]], [0.0])
    result = simulate_batch(net, [1000.0, 0.0], 300.0, duration, adiabatic=True, n_points=101,
                            stiff=True, rtol=1e-9, atol=1e-11)
    analytical = 1000.0 * np.exp(-k * result.coordinate)
    max_relative_error = float(np.max(np.abs(result.concentration[:, 0] - analytical) / 1000.0))
    conservation_error = float(np.max(np.abs(result.concentration.sum(axis=1) - 1000.0)))
    return {
        "k_1_s": k,
        "duration_s": duration,
        "max_relative_error": max_relative_error,
        "maximum_conservation_error_mol_m3": conservation_error,
        "acceptance_limits": {"max_relative_error": 1e-7, "maximum_conservation_error_mol_m3": 1e-6},
        "passed": max_relative_error < 1e-7 and conservation_error < 1e-6,
        "solver_diagnostics": result.diagnostics,
    }

validation, validation_runtime = timed(validation_case)
validation_record = {
    "case": "analytical_first_order_and_conservation",
    "status": "completed",
    "command": "python scripts/run_reference_cases.py",
    "runtime_s": validation_runtime,
    "reference": "C_A(t) = C_A0 exp(-k t) for an isothermal first-order batch reaction",
    "results": validation,
    "limitations": "Analytical verification checks implementation for a limiting case, not the validity of a real reaction mechanism.",
}

start = time.perf_counter()
try:
    simulate_batch(network, [-1.0, 0.0, 0.0], 330.0, 10.0)
    invalid = {"passed": False, "message": "Invalid negative concentration was unexpectedly accepted."}
except ValueError as exc:
    invalid = {"passed": True, "exception": type(exc).__name__, "message": str(exc)}
invalid_record = {
    "case": "intentional_invalid_input",
    "status": "rejected_as_expected" if invalid["passed"] else "failed",
    "command": "python scripts/run_reference_cases.py",
    "runtime_s": time.perf_counter() - start,
    "input": {"initial_concentration_mol_m3": [-1.0, 0.0, 0.0]},
    "acceptance": invalid,
}

records = {
    "baseline.json": baseline_record,
    "temperature-response.json": response_record,
    "validation.json": validation_record,
    "invalid-input.json": invalid_record,
}
for name, record in records.items():
    (OUT / name).write_text(json.dumps(record, indent=2) + "\n")

rows = [
    ["baseline_batch", baseline["batch"]["conversion"], baseline["batch"]["selectivity_B"], baseline["batch"]["peak_temperature_K"], baseline_runtime, True],
    ["baseline_cstr", baseline["cstr"]["conversion"], baseline["cstr"]["selectivity_B"], baseline["cstr"]["peak_temperature_K"], baseline_runtime, True],
    ["baseline_pfr", baseline["pfr"]["conversion"], baseline["pfr"]["selectivity_B"], baseline["pfr"]["peak_temperature_K"], baseline_runtime, True],
    ["response_320_K", response["cool_320_K"]["conversion"], response["cool_320_K"]["selectivity_B"], response["cool_320_K"]["peak_temperature_K"], response_runtime, response_record["acceptance"]["passed"]],
    ["response_340_K", response["warm_340_K"]["conversion"], response["warm_340_K"]["selectivity_B"], response["warm_340_K"]["peak_temperature_K"], response_runtime, response_record["acceptance"]["passed"]],
]
with (OUT / "summary.csv").open("w", newline="") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(["case", "conversion", "selectivity_B", "peak_temperature_K", "runtime_s", "accepted"])
    writer.writerows(rows)

print(json.dumps({
    "baseline_batch_conversion": baseline["batch"]["conversion"],
    "baseline_batch_selectivity_B": baseline["batch"]["selectivity_B"],
    "baseline_batch_peak_temperature_K": baseline["batch"]["peak_temperature_K"],
    "temperature_response_conversion_320_K": response["cool_320_K"]["conversion"],
    "temperature_response_conversion_340_K": response["warm_340_K"]["conversion"],
    "analytical_max_relative_error": validation["max_relative_error"],
    "conservation_error_mol_m3": validation["maximum_conservation_error_mol_m3"],
    "invalid_input_rejected": invalid["passed"],
    "reference_files": {name: sha256(OUT / name) for name in records},
}, indent=2))
