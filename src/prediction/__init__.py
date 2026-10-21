"""Prediction package – exports key prediction utilities."""

from .calibration import calibrate_probabilities, load_calibrator
from .confidence import calculate_confidence
from .shap_explainer import explain_prediction

__all__ = [
    "calibrate_probabilities",
    "load_calibrator",
    "calculate_confidence",
    "explain_prediction",
]
