"""
Metrics calculations for backtesting engine.
Provides Sharpe ratio, max drawdown, and win rate calculations.
"""

import math
from typing import List, Dict


def calculate_sharpe(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """
    Calculate the annualised Sharpe ratio from a list of period returns.

    Args:
        returns: List of period (e.g. daily) returns as decimals.
        risk_free_rate: Annual risk-free rate, default 2%.

    Returns:
        Annualised Sharpe ratio. Returns 0.0 if standard deviation is zero.
    """
    if not returns or len(returns) < 2:
        return 0.0

    n = len(returns)
    mean_return = sum(returns) / n
    variance = sum((r - mean_return) ** 2 for r in returns) / (n - 1)
    std_return = math.sqrt(variance) if variance > 0 else 0.0

    if std_return == 0.0:
        return 0.0

    # Convert annual risk-free rate to per-period (assuming 252 trading days)
    period_rf = risk_free_rate / 252
    excess_return = mean_return - period_rf

    # Annualise
    sharpe = (excess_return / std_return) * math.sqrt(252)
    return round(sharpe, 4)


def calculate_max_drawdown(equity_curve: List[float]) -> float:
    """
    Calculate the maximum drawdown from an equity curve.

    Args:
        equity_curve: List of portfolio values over time.

    Returns:
        Maximum drawdown as a negative decimal (e.g. -0.25 for 25% drawdown).
    """
    if not equity_curve or len(equity_curve) < 2:
        return 0.0

    peak = equity_curve[0]
    max_dd = 0.0

    for value in equity_curve:
        if value > peak:
            peak = value
        drawdown = (value - peak) / peak if peak != 0 else 0.0
        if drawdown < max_dd:
            max_dd = drawdown

    return round(max_dd, 4)


def calculate_win_rate(trades: List[Dict]) -> float:
    """
    Calculate win rate from a list of trade result dicts.

    Each trade dict must have a key ``'pnl'`` (float).
    A trade is a "win" if pnl > 0.

    Args:
        trades: List of dicts with at least ``{'pnl': float}``.

    Returns:
        Win rate between 0.0 and 1.0.  Returns 0.0 for empty list.
    """
    if not trades:
        return 0.0

    wins = sum(1 for t in trades if t.get("pnl", 0.0) > 0)
    return round(wins / len(trades), 4)


def calculate_profit_factor(trades: List[Dict]) -> float:
    """
    Calculate profit factor (gross profit / gross loss).

    Args:
        trades: List of dicts with at least ``{'pnl': float}``.

    Returns:
        Profit factor. Returns float('inf') if there are no losing trades.
    """
    gross_profit = sum(t["pnl"] for t in trades if t.get("pnl", 0) > 0)
    gross_loss = abs(sum(t["pnl"] for t in trades if t.get("pnl", 0) < 0))

    if gross_loss == 0:
        return float("inf") if gross_profit > 0 else 0.0

    return round(gross_profit / gross_loss, 4)


def calculate_sortino(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """
    Calculate the Sortino ratio (uses downside deviation only).

    Args:
        returns: List of period returns.
        risk_free_rate: Annual risk-free rate.

    Returns:
        Annualised Sortino ratio.
    """
    if not returns or len(returns) < 2:
        return 0.0

    period_rf = risk_free_rate / 252
    downside = [r for r in returns if r < period_rf]

    if not downside:
        return float("inf")

    mean_return = sum(returns) / len(returns)
    downside_var = sum((r - period_rf) ** 2 for r in downside) / len(downside)
    downside_std = math.sqrt(downside_var)

    if downside_std == 0:
        return 0.0

    sortino = ((mean_return - period_rf) / downside_std) * math.sqrt(252)
    return round(sortino, 4)
