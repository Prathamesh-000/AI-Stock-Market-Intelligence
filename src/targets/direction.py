"""
Direction target labelling.

Converts a raw percentage price change into a ternary direction label
(UP / DOWN / FLAT) used as the classification target.
"""

from __future__ import annotations


def classify_direction(
    price_change_pct: float,
    threshold: float = 0.5,
) -> str:
    """
    Classify a price change percentage into a direction label.

    Args:
        price_change_pct: Percentage price change (e.g. ``2.3`` for +2.3%,
                          ``-1.5`` for -1.5%).  Pass values as percentages,
                          NOT decimals.
        threshold: Minimum absolute percentage change to be labelled UP/DOWN.
                   Moves within ``±threshold`` are labelled FLAT.
                   Default is 0.5 (i.e. ±0.5%).

    Returns:
        - ``"UP"``   – price rose by more than *threshold*.
        - ``"DOWN"`` – price fell by more than *threshold*.
        - ``"FLAT"`` – price moved within ±*threshold*.
    """
    pct = float(price_change_pct)
    th = abs(float(threshold))

    if pct > th:
        return "UP"
    elif pct < -th:
        return "DOWN"
    return "FLAT"
