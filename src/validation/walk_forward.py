"""
Walk-forward cross-validation for time-series models.

Evaluates a model using expanding/rolling training windows so that future
data is never seen during training – the gold standard for financial ML.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

import numpy as np

from .time_split import TimeSeriesSplit
from ..models.evaluator import evaluate_model

logger = logging.getLogger(__name__)


def walk_forward_validate(
    model: Any,
    X,
    y,
    n_splits: int = 5,
    max_train_size: int | None = None,
    gap: int = 0,
) -> Dict:
    """
    Run walk-forward (time-series) cross-validation on a model.

    The model is **retrained** from scratch on each expanding training fold
    and evaluated on the subsequent test fold.

    Args:
        model: A scikit-learn-compatible estimator with ``fit`` and ``predict``
               methods.  It should not have been fit yet (or state is overwritten).
        X: Feature matrix, array-like of shape (n_samples, n_features).
        y: Target labels, array-like of shape (n_samples,).
        n_splits: Number of walk-forward folds (default 5).
        max_train_size: If set, uses a rolling training window of this size.
        gap: Samples to skip between train end and test start (look-ahead guard).

    Returns:
        Dict with keys:

        - ``fold_metrics``  – list of per-fold metric dicts.
        - ``mean_accuracy`` – mean accuracy across folds.
        - ``mean_f1``       – mean weighted F1 across folds.
        - ``n_splits``      – actual number of completed folds.
    """
    X_arr = np.array(X)
    y_arr = np.array(y)

    splitter = TimeSeriesSplit(
        n_splits=n_splits, max_train_size=max_train_size, gap=gap
    )

    fold_metrics: List[Dict] = []

    for fold_idx, (train_idx, test_idx) in enumerate(
        splitter.split(X_arr), start=1
    ):
        X_train, X_test = X_arr[train_idx], X_arr[test_idx]
        y_train, y_test = y_arr[train_idx], y_arr[test_idx]

        try:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            metrics = evaluate_model(list(y_test), list(y_pred))
            metrics["fold"] = fold_idx
            metrics["train_size"] = len(train_idx)
            metrics["test_size"] = len(test_idx)
            fold_metrics.append(metrics)
            logger.info(
                "Fold %d/%d – accuracy=%.4f  f1=%.4f",
                fold_idx,
                n_splits,
                metrics["accuracy"],
                metrics["f1"],
            )
        except Exception as exc:
            logger.warning("Fold %d failed: %s", fold_idx, exc)

    if not fold_metrics:
        return {
            "fold_metrics": [],
            "mean_accuracy": 0.0,
            "mean_f1": 0.0,
            "n_splits": 0,
        }

    mean_acc = sum(m["accuracy"] for m in fold_metrics) / len(fold_metrics)
    mean_f1 = sum(m["f1"] for m in fold_metrics) / len(fold_metrics)

    return {
        "fold_metrics": fold_metrics,
        "mean_accuracy": round(mean_acc, 4),
        "mean_f1": round(mean_f1, 4),
        "n_splits": len(fold_metrics),
    }
