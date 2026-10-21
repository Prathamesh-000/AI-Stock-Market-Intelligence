"""
Impact score target computation.

Combines abnormal return magnitude and volume ratio into a single
0.0–10.0 impact score used as a regression target.
"""

from __future__ import annotations

import math


def calculate_impact_score(
    abnormal_return: float,
    volume_ratio: float,
    ar_weight: float = 0.6,
    vol_weight: float = 0.4,
) -> float:
    """
    Calculate a 0.0–10.0 impact score from abnormal return and volume ratio.

    The score reflects how much market attention a news event received,
    combining price dislocation (abnormal return) with trading volume anomaly.

    Formula::

        ar_component  = tanh(|AR| * 10) * 10   → [0, 10]
        vol_component = tanh(log1p(vol_ratio)) * 10  → [0, 10]
        score = ar_weight * ar_component + vol_weight * vol_component

    Args:
        abnormal_return: Abnormal return as a decimal (e.g. ``0.05`` for 5%).
        volume_ratio: Today's volume / average volume (e.g. ``2.5`` for 2.5×).
                      Must be >= 0.
        ar_weight: Weight for abnormal return component (default 0.6).
        vol_weight: Weight for volume component (default 0.4).

    Returns:
        Impact score in [0.0, 10.0], rounded to 2 d.p.
    """
    ar = abs(float(abnormal_return))
    vol = max(float(volume_ratio), 0.0)

    # Abnormal return contribution – saturates at extreme moves
    ar_component = math.tanh(ar * 10) * 10  # [0, 10]

    # Volume contribution – log-scale to handle very large spikes
    vol_component = math.tanh(math.log1p(vol)) * 10  # [0, 10]

    # Normalise weights
    total_w = ar_weight + vol_weight
    aw = ar_weight / total_w if total_w > 0 else 0.6
    vw = vol_weight / total_w if total_w > 0 else 0.4

    score = aw * ar_component + vw * vol_component
    return round(min(max(score, 0.0), 10.0), 2)
