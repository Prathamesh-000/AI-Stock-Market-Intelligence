"""
SHAP explainer wrapper.

Provides a safe ``explain_prediction`` helper that gracefully falls back
to feature-importance ranking when the ``shap`` package is not installed.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

try:
    import shap as _shap
    _SHAP_AVAILABLE = True
except ImportError:
    _shap = None  # type: ignore
    _SHAP_AVAILABLE = False


def explain_prediction(
    model: Any,
    features: Dict[str, float],
    top_n: int = 3,
) -> Dict:
    """
    Explain a single prediction using SHAP values.

    Falls back to a feature-magnitude ranking when ``shap`` is not available
    or when the model type is not supported.

    Args:
        model: Trained model object (XGBoost, sklearn, etc.).
        features: Dict of ``{feature_name: value}`` for one sample.
        top_n: Number of top features to return (default 3).

    Returns:
        Dict with keys:

        - ``method``  – ``"shap"`` or ``"fallback_magnitude"``.
        - ``top_features`` – list of ``{"feature", "importance", "value"}`` dicts
          sorted by abs. importance, descending.
        - ``shap_available`` – bool.
    """
    feature_names: List[str] = list(features.keys())
    feature_values: List[float] = [float(v) for v in features.values()]

    if _SHAP_AVAILABLE and model is not None:
        try:
            return _shap_explain(model, feature_names, feature_values, top_n)
        except Exception as exc:
            logger.warning("SHAP explanation failed: %s – using fallback.", exc)

    return _fallback_explain(feature_names, feature_values, top_n)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _shap_explain(
    model: Any,
    feature_names: List[str],
    feature_values: List[float],
    top_n: int,
) -> Dict:
    """Use SHAP TreeExplainer or Explainer to compute feature contributions."""
    import numpy as np

    x = np.array(feature_values).reshape(1, -1)

    try:
        explainer = _shap.TreeExplainer(model)
    except Exception:
        explainer = _shap.Explainer(model)

    shap_values = explainer.shap_values(x)

    # Handle multi-class output (list of arrays)
    if isinstance(shap_values, list):
        # Average absolute SHAP across classes
        import numpy as np
        sv = np.mean([np.abs(sv) for sv in shap_values], axis=0)[0]
    else:
        sv = abs(shap_values[0]) if hasattr(shap_values[0], "__iter__") else abs(shap_values)

    ranked = sorted(
        zip(feature_names, sv, feature_values),
        key=lambda t: abs(t[1]),
        reverse=True,
    )[:top_n]

    return {
        "method": "shap",
        "shap_available": True,
        "top_features": [
            {"feature": name, "importance": round(float(imp), 6), "value": val}
            for name, imp, val in ranked
        ],
    }


def _fallback_explain(
    feature_names: List[str],
    feature_values: List[float],
    top_n: int,
) -> Dict:
    """Rank features by absolute magnitude when SHAP is unavailable."""
    ranked: List[Tuple] = sorted(
        zip(feature_names, feature_values),
        key=lambda t: abs(t[1]),
        reverse=True,
    )[:top_n]

    return {
        "method": "fallback_magnitude",
        "shap_available": _SHAP_AVAILABLE,
        "top_features": [
            {"feature": name, "importance": round(abs(val), 6), "value": val}
            for name, val in ranked
        ],
    }
