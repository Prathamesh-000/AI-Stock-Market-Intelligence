"""Targets package – exports labelling utilities."""

from .abnormal_returns import calculate_abnormal_return, calculate_car
from .direction import classify_direction
from .impact_score import calculate_impact_score

__all__ = [
    "calculate_abnormal_return",
    "calculate_car",
    "classify_direction",
    "calculate_impact_score",
]
