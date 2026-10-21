"""
Direction model – logistic regression wrapper for predicting stock direction.

When a trained model is present it is loaded from disk; otherwise a
rule-based heuristic based on sentiment score is used as a fallback.
"""

from __future__ import annotations

import logging
import os
import pickle
from typing import Dict, Optional

logger = logging.getLogger(__name__)

_DIRECTION_LABELS = ["UP", "DOWN", "FLAT"]
_DEFAULT_MODEL_DIR = os.path.join("models", "saved")


class DirectionModel:
    """
    Wrapper around a sklearn LogisticRegression for direction prediction.

    The model predicts one of ``"UP"``, ``"DOWN"``, or ``"FLAT"`` given a
    feature dict.  If no trained model is available, a sentiment-score
    heuristic is applied.

    Args:
        ticker: Ticker symbol used to locate the saved model file.
        model_dir: Directory where ``direction_{ticker}_latest.pkl`` lives.
    """

    def __init__(self, ticker: str = "UNKNOWN", model_dir: str = _DEFAULT_MODEL_DIR):
        self.ticker = ticker.upper()
        self.model_dir = model_dir
        self._model = None
        self._feature_names: Optional[list] = None
        self._load()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def predict(self, features: Dict[str, float]) -> str:
        """
        Predict price direction from a feature dict.

        Args:
            features: Dict mapping feature names to numeric values.
                      Must include ``'sentiment_score'`` for the fallback path.

        Returns:
            One of ``"UP"``, ``"DOWN"``, or ``"FLAT"``.
        """
        if self._model is not None:
            return self._sklearn_predict(features)
        return self._heuristic_predict(features)

    def predict_proba(self, features: Dict[str, float]) -> Dict[str, float]:
        """
        Return class probability estimates.

        Returns:
            Dict mapping direction labels to probabilities summing to ~1.0.
        """
        if self._model is not None:
            try:
                x = self._dict_to_vector(features)
                probs = self._model.predict_proba([x])[0]
                classes = list(self._model.classes_)
                return {cls: float(p) for cls, p in zip(classes, probs)}
            except Exception as exc:
                logger.warning("predict_proba failed: %s", exc)

        # Fallback: crude probability from sentiment score
        sentiment = float(features.get("sentiment_score", 0.0))
        if sentiment > 0.15:
            return {"UP": 0.65, "DOWN": 0.20, "FLAT": 0.15}
        elif sentiment < -0.15:
            return {"UP": 0.20, "DOWN": 0.65, "FLAT": 0.15}
        return {"UP": 0.30, "DOWN": 0.30, "FLAT": 0.40}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """Try to load a saved LogisticRegression model from disk."""
        path = os.path.join(
            self.model_dir, f"direction_{self.ticker}_latest.pkl"
        )
        if os.path.exists(path):
            try:
                with open(path, "rb") as fh:
                    payload = pickle.load(fh)
                self._model = payload.get("model")
                self._feature_names = payload.get("feature_names")
                logger.info("Loaded DirectionModel for %s from %s", self.ticker, path)
            except Exception as exc:
                logger.warning("Could not load DirectionModel: %s", exc)
        else:
            logger.debug(
                "No saved DirectionModel found for %s; using heuristic.", self.ticker
            )

    def _sklearn_predict(self, features: Dict[str, float]) -> str:
        try:
            x = self._dict_to_vector(features)
            pred = self._model.predict([x])[0]
            return str(pred) if pred in _DIRECTION_LABELS else "FLAT"
        except Exception as exc:
            logger.warning("sklearn predict failed: %s – falling back.", exc)
            return self._heuristic_predict(features)

    def _heuristic_predict(self, features: Dict[str, float]) -> str:
        """Simple rule-based direction prediction using sentiment score."""
        sentiment = float(features.get("sentiment_score", 0.0))
        confidence = float(features.get("confidence", 0.5))

        if sentiment > 0.2 and confidence > 0.5:
            return "UP"
        elif sentiment < -0.2 and confidence > 0.5:
            return "DOWN"
        return "FLAT"

    def _dict_to_vector(self, features: Dict[str, float]) -> list:
        """Convert a feature dict to an ordered list matching training columns."""
        if self._feature_names:
            return [float(features.get(k, 0.0)) for k in self._feature_names]
        return list(features.values())
