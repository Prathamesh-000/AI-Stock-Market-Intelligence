"""
Time-series cross-validation splitter.

Implements walk-forward (expanding window) splits so that future data
never leaks into training folds – essential for financial time series.
"""

from __future__ import annotations

from typing import Generator, List, Tuple

import numpy as np


class TimeSeriesSplit:
    """
    Walk-forward time-series cross-validation splitter.

    Unlike sklearn's ``TimeSeriesSplit`` which always uses an expanding
    training window, this implementation also supports a fixed
    ``max_train_size`` to simulate a rolling window.

    Args:
        n_splits: Number of CV folds (default 5).
        max_train_size: Maximum number of training samples.  Use ``None``
                        for an expanding (unlimited) training window.
        gap: Number of samples to skip between the train and test sets
             (useful when targets are computed with a look-ahead).

    Example::

        tss = TimeSeriesSplit(n_splits=5)
        for train_idx, test_idx in tss.split(X):
            X_train, X_test = X[train_idx], X[test_idx]
    """

    def __init__(
        self,
        n_splits: int = 5,
        max_train_size: int | None = None,
        gap: int = 0,
    ):
        if n_splits < 2:
            raise ValueError("n_splits must be at least 2.")
        self.n_splits = n_splits
        self.max_train_size = max_train_size
        self.gap = gap

    def split(
        self,
        X,
        y=None,
        groups=None,
    ) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """
        Generate (train_indices, test_indices) pairs.

        Args:
            X: Array-like of shape (n_samples, …).  Only the length is used.
            y: Ignored (kept for API compatibility).
            groups: Ignored.

        Yields:
            Tuples of ``(train_idx, test_idx)`` numpy integer arrays.
        """
        n_samples = len(X)
        n_splits = self.n_splits
        gap = self.gap

        # Minimum samples needed: at least one test sample per fold plus gap
        test_size = n_samples // (n_splits + 1)
        if test_size == 0:
            raise ValueError(
                f"Not enough samples ({n_samples}) for {n_splits} splits."
            )

        indices = np.arange(n_samples)

        for fold in range(n_splits):
            train_end = test_size * (fold + 1)
            test_start = train_end + gap
            test_end = test_start + test_size

            if test_end > n_samples:
                test_end = n_samples
            if test_start >= n_samples:
                break

            # Apply optional max_train_size (rolling window)
            train_start = 0
            if self.max_train_size is not None:
                train_start = max(0, train_end - self.max_train_size)

            train_idx = indices[train_start:train_end]
            test_idx = indices[test_start:test_end]

            yield train_idx, test_idx

    def get_n_splits(self, X=None, y=None, groups=None) -> int:
        """Return the number of splits."""
        return self.n_splits
