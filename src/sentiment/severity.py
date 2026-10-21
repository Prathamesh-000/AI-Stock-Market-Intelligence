"""
Sentiment severity classifier.

Maps a numeric sentiment score to a human-readable severity label and
a corresponding float multiplier used to scale impact scores.
"""

from __future__ import annotations

_SEVERITY_MULTIPLIERS = {
    "HIGH": 1.5,
    "MEDIUM": 1.0,
    "LOW": 0.6,
    "NEUTRAL": 0.3,
}


def classify_severity(sentiment_score: float) -> str:
    """
    Classify sentiment magnitude into a severity tier.

    Thresholds:
    - |score| >= 0.6  → ``"HIGH"``
    - |score| >= 0.3  → ``"MEDIUM"``
    - |score| >= 0.05 → ``"LOW"``
    - otherwise       → ``"NEUTRAL"``

    Args:
        sentiment_score: Polarity score in [-1.0, 1.0].

    Returns:
        Severity label: ``"HIGH"``, ``"MEDIUM"``, ``"LOW"``, or ``"NEUTRAL"``.
    """
    abs_score = abs(float(sentiment_score))

    if abs_score >= 0.6:
        return "HIGH"
    elif abs_score >= 0.3:
        return "MEDIUM"
    elif abs_score >= 0.05:
        return "LOW"
    return "NEUTRAL"


def get_severity_multiplier(severity: str) -> float:
    """
    Return the impact multiplier for a severity label.

    Args:
        severity: One of ``"HIGH"``, ``"MEDIUM"``, ``"LOW"``, ``"NEUTRAL"``.

    Returns:
        Float multiplier. Defaults to 1.0 for unknown labels.
    """
    return _SEVERITY_MULTIPLIERS.get(severity.upper().strip(), 1.0)
