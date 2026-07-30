"""Transparent reduced-order chemical reactor digital twin."""
from .models import ReactionNetwork, ReactorResult, simulate_batch, simulate_cstr, simulate_pfr
from .calibration import fit_arrhenius_parameters, identifiability_report
from .analysis import validate_prediction, uncertainty_propagation, local_sensitivity
from .optimization import optimize_operating_conditions
__version__ = "0.1.0"
