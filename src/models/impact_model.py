"""
Impact score model.

Computes a normalised 0.0–1.0 impact score that reflects the expected
magnitude of a news event's effect on a stock's price, combining
sentiment strength, trading volume anomaly, and event type.
"""

from __future__ import annotations

import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Event type base weights – higher = more market-moving
_EVENT_WEIGHTS: Dict[str, float] = {
    "earnings": 0.35,
    "acquisition": 0.30,
    "fda_approval": 0.28,
    "layoff": 0.18,
    "lawsuit": 0.15,
    "partnership": 0.12,
    "leadership_change": 0.10,
    "general": 0.05,
}


class ImpactModel:
    """
    Heuristic-based model that produces a 0.0–1.0 impact score.

    The score combines:
    - Absolute sentiment magnitude (how strongly positive/negative).
    - Volume ratio anomaly (how abnormal today's volume is vs baseline).
    - Event-type weight (earnings beat/miss move prices more than partnerships).

    Args:
        sentiment_weight: Contribution of sentiment to the final score (0–1).
        volume_weight: Contribution of volume anomaly to the final score (0–1).
        event_weight: Contribution of event-type weight to the final score (0–1).

    The three weights should sum to 1.0.
    """

    def __init__(
        self,
        sentiment_weight: float = 0.45,
        volume_weight: float = 0.35,
        event_weight: float = 0.20,
    ):
        total = sentiment_weight + volume_weight + event_weight
        if abs(total - 1.0) > 1e-6:
            logger.warning(
                "ImpactModel weights sum to %.4f, not 1.0. Normalising.", total
            )
            sentiment_weight /= total
            volume_weight /= total
            event_weight /= total

        self.sentiment_weight = sentiment_weight
        self.volume_weight = volume_weight
        self.event_weight = event_weight

    def predict_impact(
        self,
        sentiment_score: float,
        volume_score: float,
        event_type: str = "general",
    ) -> float:
        """
        Predict the market impact score.

        Args:
            sentiment_score: Sentiment polarity in [-1.0, 1.0].
            volume_score: Normalised volume anomaly in [0.0, 1.0].
                          A value of 0.0 means normal volume; 1.0 means very high.
            event_type: One of the keys in ``_EVENT_WEIGHTS`` (e.g. ``"earnings"``).

        Returns:
            Impact score in [0.0, 1.0].
        """
        # Sentiment component: absolute magnitude
        sentiment_component = min(abs(float(sentiment_score)), 1.0)

        # Volume component
        volume_component = min(max(float(volume_score), 0.0), 1.0)

        # Event type component
        key = event_type.lower().strip() if event_type else "general"
        event_component = _EVENT_WEIGHTS.get(key, _EVENT_WEIGHTS["general"])

        score = (
            self.sentiment_weight * sentiment_component
            + self.volume_weight * volume_component
            + self.event_weight * event_component
        )

        return round(min(max(score, 0.0), 1.0), 4)

    def batch_predict(
        self,
        records: list,
    ) -> list:
        """
        Run :meth:`predict_impact` over a list of record dicts.

        Each record must have keys ``sentiment_score``, ``volume_score``,
        and optionally ``event_type``.

        Args:
            records: List of dicts.

        Returns:
            List of float impact scores.
        """
        results = []
        for rec in records:
            score = self.predict_impact(
                sentiment_score=rec.get("sentiment_score", 0.0),
                volume_score=rec.get("volume_score", 0.0),
                event_type=rec.get("event_type", "general"),
            )
            results.append(score)
        return results
