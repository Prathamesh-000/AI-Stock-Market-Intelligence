"""
Model trainer – wraps XGBoost with cross-validation and model persistence.
"""

from __future__ import annotations

import logging
import os
import pickle
from typing import Any, Dict, List, Optional

import numpy as np

try:
    import xgboost as xgb
    _XGB_AVAILABLE = True
except ImportError:
    _XGB_AVAILABLE = False
    xgb = None  # type: ignore

try:
    from sklearn.model_selection import StratifiedKFold, cross_val_score
    _SKLEARN_AVAILABLE = True
except ImportError:
    _SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)

_DEFAULT_PARAMS: Dict[str, Any] = {
    "n_estimators": 200,
    "max_depth": 4,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "use_label_encoder": False,
    "eval_metric": "mlogloss",
    "random_state": 42,
}


class ModelTrainer:
    """
    Trains an XGBoost classifier with optional k-fold cross-validation.

    Args:
        params: XGBoost hyperparameters (merged with defaults).
        cv_folds: Number of stratified CV folds. Set to 0 to skip CV.
    """

    def __init__(
        self,
        params: Optional[Dict[str, Any]] = None,
        cv_folds: int = 5,
    ):
        self.params = {**_DEFAULT_PARAMS, **(params or {})}
        self.cv_folds = cv_folds
        self._model = None
        self._cv_scores: List[float] = []
        self._feature_names: List[str] = []
        self._ticker: str = "UNKNOWN"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def train(
        self,
        X: Any,  # array-like (n_samples, n_features)
        y: Any,  # array-like (n_samples,) – class labels
        ticker: str = "UNKNOWN",
        feature_names: Optional[List[str]] = None,
    ) -> "ModelTrainer":
        """
        Train XGBoost and optionally run cross-validation.

        Args:
            X: Feature matrix.
            y: Target labels (encoded as integers or strings).
            ticker: Ticker symbol for logging/saving.
            feature_names: Optional list of feature column names.

        Returns:
            self (for chaining).
        """
        self._ticker = ticker.upper()
        self._feature_names = feature_names or []

        if not _XGB_AVAILABLE:
            logger.warning("XGBoost not installed. Falling back to dummy model.")
            self._model = _DummyClassifier()
            return self

        X_arr = np.array(X)
        y_arr = np.array(y)

        # --- Cross-validation ---
        if self.cv_folds > 1 and _SKLEARN_AVAILABLE:
            cv_model = xgb.XGBClassifier(**self.params)
            skf = StratifiedKFold(n_splits=self.cv_folds, shuffle=True, random_state=42)
            scores = cross_val_score(
                cv_model, X_arr, y_arr, cv=skf, scoring="accuracy"
            )
            self._cv_scores = scores.tolist()
            logger.info(
                "[%s] CV accuracy: %.4f ± %.4f",
                ticker,
                scores.mean(),
                scores.std(),
            )

        # --- Final model (full dataset) ---
        self._model = xgb.XGBClassifier(**self.params)
        self._model.fit(X_arr, y_arr)
        logger.info("[%s] XGBoost training complete.", ticker)
        return self

    def save(self, path: str) -> str:
        """
        Persist the trained model and metadata to a pickle file.

        Args:
            path: File path (e.g. ``"models/saved/xgb_AAPL_latest.pkl"``).

        Returns:
            Absolute path to the saved file.
        """
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        payload = {
            "model": self._model,
            "feature_names": self._feature_names,
            "ticker": self._ticker,
            "cv_scores": self._cv_scores,
            "params": self.params,
        }
        with open(path, "wb") as fh:
            pickle.dump(payload, fh)
        logger.info("Model saved to %s", path)
        return os.path.abspath(path)

    @classmethod
    def load(cls, path: str) -> "ModelTrainer":
        """Load a previously saved ModelTrainer payload from disk."""
        with open(path, "rb") as fh:
            payload = pickle.load(fh)
        instance = cls(params=payload.get("params"))
        instance._model = payload.get("model")
        instance._feature_names = payload.get("feature_names", [])
        instance._ticker = payload.get("ticker", "UNKNOWN")
        instance._cv_scores = payload.get("cv_scores", [])
        return instance

    @property
    def cv_scores(self) -> List[float]:
        """Return per-fold cross-validation accuracy scores."""
        return self._cv_scores

    @property
    def model(self):
        """Access the underlying trained model object."""
        return self._model


class _DummyClassifier:
    """Fallback classifier when XGBoost is not installed."""

    def predict(self, X):
        return ["FLAT"] * len(X)

    def predict_proba(self, X):
        return [[0.33, 0.34, 0.33]] * len(X)
