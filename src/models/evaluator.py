"""
Model evaluation utilities.

Wraps sklearn metrics into convenient dict-returning helpers so the rest
of the pipeline can consume them without importing sklearn directly.
"""

from __future__ import annotations

from typing import Dict, List, Union

import numpy as np

try:
    from sklearn.metrics import (
        accuracy_score,
        classification_report,
        f1_score,
        precision_score,
        recall_score,
    )
    _SKLEARN_AVAILABLE = True
except ImportError:
    _SKLEARN_AVAILABLE = False


def evaluate_model(
    y_true: List[Union[str, int]],
    y_pred: List[Union[str, int]],
) -> Dict[str, float]:
    """
    Compute classification metrics for a set of predictions.

    Args:
        y_true: Ground-truth labels.
        y_pred: Model-predicted labels.

    Returns:
        Dict with keys ``accuracy``, ``precision``, ``recall``, ``f1``.
    """
    if not y_true or not y_pred:
        return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}

    if len(y_true) != len(y_pred):
        raise ValueError(
            f"y_true ({len(y_true)}) and y_pred ({len(y_pred)}) must have equal length."
        )

    if _SKLEARN_AVAILABLE:
        avg = "weighted"
        return {
            "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
            "precision": round(
                float(precision_score(y_true, y_pred, average=avg, zero_division=0)), 4
            ),
            "recall": round(
                float(recall_score(y_true, y_pred, average=avg, zero_division=0)), 4
            ),
            "f1": round(
                float(f1_score(y_true, y_pred, average=avg, zero_division=0)), 4
            ),
        }

    # Manual fallback (binary / multiclass, macro avg)
    return _manual_metrics(y_true, y_pred)


def classification_report_dict(
    y_true: List[Union[str, int]],
    y_pred: List[Union[str, int]],
) -> Dict:
    """
    Return a full per-class classification report as a nested dict.

    Args:
        y_true: Ground-truth labels.
        y_pred: Model-predicted labels.

    Returns:
        Nested dict compatible with sklearn's ``classification_report(output_dict=True)``.
    """
    if _SKLEARN_AVAILABLE:
        return classification_report(
            y_true, y_pred, output_dict=True, zero_division=0
        )

    # Minimal fallback
    return {"summary": evaluate_model(y_true, y_pred)}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _manual_metrics(
    y_true: List[Union[str, int]],
    y_pred: List[Union[str, int]],
) -> Dict[str, float]:
    """Pure-Python metrics when sklearn is unavailable."""
    classes = list(set(y_true))
    n = len(y_true)

    correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    accuracy = correct / n if n else 0.0

    precisions, recalls, f1s = [], [], []
    for cls in classes:
        tp = sum(1 for a, b in zip(y_true, y_pred) if a == cls and b == cls)
        fp = sum(1 for a, b in zip(y_true, y_pred) if a != cls and b == cls)
        fn = sum(1 for a, b in zip(y_true, y_pred) if a == cls and b != cls)

        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0

        precisions.append(prec)
        recalls.append(rec)
        f1s.append(f1)

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(sum(precisions) / len(precisions) if precisions else 0.0, 4),
        "recall": round(sum(recalls) / len(recalls) if recalls else 0.0, 4),
        "f1": round(sum(f1s) / len(f1s) if f1s else 0.0, 4),
    }
