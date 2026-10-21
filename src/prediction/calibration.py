"""
Probability calibration utilities.

Wraps sklearn's isotonic / sigmoid calibration and provides a loader
for per-ticker calibrator artefacts.
"""

from __future__ import annotations

import logging
import os
import pickle
from typing import List, Optional

logger = logging.getLogger(__name__)

_CALIBRATOR_DIR = os.path.join("models", "saved")


def calibrate_probabilities(
    raw_probs: List[float],
    method: str = "isotonic",
    calibrator=None,
) -> List[float]:
    """
    Calibrate a list of raw model probabilities.

    If a fitted *calibrator* object (``CalibratedClassifierCV`` or similar)
    is provided it is used directly.  Otherwise the raw probabilities are
    corrected with a simple Platt-like sigmoid transformation.

    Args:
        raw_probs: List of uncalibrated probabilities in [0.0, 1.0].
        method: ``"isotonic"`` or ``"sigmoid"`` (used only when no calibrator
                object is supplied).
        calibrator: Optional fitted sklearn calibrator with a ``predict_proba``
                    or ``transform`` method.

    Returns:
        List of calibrated probabilities in [0.0, 1.0].
    """
    if not raw_probs:
        return []

    if calibrator is not None:
        try:
            import numpy as np
            arr = np.array(raw_probs).reshape(-1, 1)
            if hasattr(calibrator, "transform"):
                calibrated = calibrator.transform(arr).flatten().tolist()
            elif hasattr(calibrator, "predict_proba"):
                calibrated = calibrator.predict_proba(arr)[:, 1].tolist()
            else:
                raise AttributeError("Calibrator has no transform/predict_proba.")
            return [round(float(p), 6) for p in calibrated]
        except Exception as exc:
            logger.warning("Calibrator failed: %s – using fallback.", exc)

    # Fallback: sigmoid squash to correct over-confidence
    import math

    def _sigmoid_calibrate(p: float) -> float:
        # Platt scaling approximation: slightly flatten towards 0.5
        p = min(max(p, 1e-7), 1 - 1e-7)
        logit = math.log(p / (1 - p))
        calibrated_logit = 0.85 * logit  # dampen by 15%
        return 1.0 / (1.0 + math.exp(-calibrated_logit))

    return [round(_sigmoid_calibrate(p), 6) for p in raw_probs]


def load_calibrator(ticker: str, calibrator_dir: str = _CALIBRATOR_DIR):
    """
    Load a fitted calibrator object for the given ticker from disk.

    Expected file: ``{calibrator_dir}/calibrator_{ticker}_latest.pkl``

    Args:
        ticker: Stock ticker symbol (e.g. ``"AAPL"``).
        calibrator_dir: Directory containing calibrator pickle files.

    Returns:
        Calibrator object if found, ``None`` otherwise.
    """
    ticker = ticker.upper().strip()
    path = os.path.join(calibrator_dir, f"calibrator_{ticker}_latest.pkl")

    if not os.path.exists(path):
        logger.debug("No calibrator found for %s at %s", ticker, path)
        return None

    try:
        with open(path, "rb") as fh:
            calibrator = pickle.load(fh)
        logger.info("Loaded calibrator for %s from %s", ticker, path)
        return calibrator
    except Exception as exc:
        logger.warning("Failed to load calibrator for %s: %s", ticker, exc)
        return None
