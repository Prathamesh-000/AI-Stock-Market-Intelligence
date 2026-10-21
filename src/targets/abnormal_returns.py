"""
Abnormal and cumulative abnormal return calculations.

Based on the standard event-study methodology using the market model:
    AR_t = R_t - (alpha + beta * R_m_t)

where alpha is assumed to be 0 for simplicity (no intercept).
"""

from __future__ import annotations

from typing import List


def calculate_abnormal_return(
    stock_return: float,
    market_return: float,
    beta: float,
    alpha: float = 0.0,
) -> float:
    """
    Calculate the abnormal return for a single period.

    Uses the market model:
        AR = R_stock - (alpha + beta * R_market)

    Args:
        stock_return: Observed stock return for the period (decimal, e.g. 0.02).
        market_return: Contemporaneous market/benchmark return (decimal).
        beta: Stock's beta coefficient with respect to the market.
        alpha: Intercept term (default 0.0).

    Returns:
        Abnormal return as a decimal.
    """
    expected_return = alpha + beta * market_return
    ar = float(stock_return) - expected_return
    return round(ar, 6)


def calculate_car(
    returns: List[float],
    market_returns: List[float],
    beta: float,
    alpha: float = 0.0,
) -> float:
    """
    Calculate the Cumulative Abnormal Return (CAR) over an event window.

    Args:
        returns: List of stock returns over the event window.
        market_returns: List of market returns over the same window.
        beta: Stock beta.
        alpha: Market model intercept (default 0.0).

    Returns:
        Cumulative abnormal return (sum of individual ARs).

    Raises:
        ValueError: If ``returns`` and ``market_returns`` differ in length.
    """
    if len(returns) != len(market_returns):
        raise ValueError(
            f"returns ({len(returns)}) and market_returns ({len(market_returns)}) "
            "must have the same length."
        )

    car = sum(
        calculate_abnormal_return(r, mr, beta, alpha)
        for r, mr in zip(returns, market_returns)
    )
    return round(car, 6)
