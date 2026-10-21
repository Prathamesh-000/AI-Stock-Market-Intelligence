"""
Backtesting engine for evaluating prediction performance.

Takes a list of predictions (ticker, direction, confidence) and actual
price data, then calculates P&L, win rate, Sharpe ratio, and other metrics.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .metrics import (
    calculate_max_drawdown,
    calculate_profit_factor,
    calculate_sharpe,
    calculate_sortino,
    calculate_win_rate,
)

logger = logging.getLogger(__name__)


@dataclass
class Prediction:
    """A single model prediction."""

    ticker: str
    direction: str  # "UP", "DOWN", "FLAT"
    confidence: float  # 0.0 – 1.0
    timestamp: Optional[str] = None


@dataclass
class TradeResult:
    """Result of simulating a single trade based on a prediction."""

    ticker: str
    direction: str
    confidence: float
    entry_price: float
    exit_price: float
    pnl: float
    pnl_pct: float
    correct: bool


class BacktestEngine:
    """
    Simulates trades from model predictions and evaluates performance.

    Usage::

        engine = BacktestEngine(initial_capital=10_000)
        engine.run(predictions, price_data)
        report = engine.summary()
    """

    def __init__(self, initial_capital: float = 10_000.0, position_size: float = 0.1):
        """
        Initialise the engine.

        Args:
            initial_capital: Starting portfolio value in USD.
            position_size: Fraction of capital allocated per trade (0–1).
        """
        self.initial_capital = initial_capital
        self.position_size = position_size
        self._trades: List[TradeResult] = []
        self._equity_curve: List[float] = [initial_capital]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(
        self,
        predictions: List[Prediction],
        price_data: Dict[str, List[Tuple[str, float]]],
    ) -> "BacktestEngine":
        """
        Simulate trades for every prediction.

        Args:
            predictions: List of :class:`Prediction` objects.
            price_data: Mapping of ticker -> list of (date_str, close_price) tuples
                        sorted chronologically.  Each prediction uses the first two
                        consecutive prices available after the prediction timestamp.

        Returns:
            self (for chaining)
        """
        self._trades = []
        capital = self.initial_capital
        self._equity_curve = [capital]

        for pred in predictions:
            ticker = pred.ticker
            if ticker not in price_data or len(price_data[ticker]) < 2:
                logger.warning("No price data for %s – skipping prediction.", ticker)
                continue

            prices = price_data[ticker]
            entry_price, exit_price = self._get_entry_exit(prices, pred.timestamp)

            if entry_price is None or exit_price is None:
                continue

            trade = self._simulate_trade(pred, entry_price, exit_price, capital)
            self._trades.append(trade)
            capital += trade.pnl
            self._equity_curve.append(capital)

        logger.info("Backtest complete: %d trades simulated.", len(self._trades))
        return self

    def summary(self) -> Dict:
        """
        Return a dict of performance metrics.

        Returns:
            Dict with keys: total_trades, win_rate, total_pnl, total_pnl_pct,
            sharpe_ratio, sortino_ratio, max_drawdown, profit_factor,
            avg_pnl_per_trade, final_capital.
        """
        if not self._trades:
            return {"error": "No trades to summarise. Run run() first."}

        trade_dicts = [{"pnl": t.pnl} for t in self._trades]
        returns = [t.pnl_pct for t in self._trades]

        total_pnl = sum(t.pnl for t in self._trades)
        final_capital = self._equity_curve[-1]

        return {
            "total_trades": len(self._trades),
            "win_rate": calculate_win_rate(trade_dicts),
            "total_pnl": round(total_pnl, 2),
            "total_pnl_pct": round(
                (final_capital - self.initial_capital) / self.initial_capital * 100, 2
            ),
            "sharpe_ratio": calculate_sharpe(returns),
            "sortino_ratio": calculate_sortino(returns),
            "max_drawdown": calculate_max_drawdown(self._equity_curve),
            "profit_factor": calculate_profit_factor(trade_dicts),
            "avg_pnl_per_trade": round(total_pnl / len(self._trades), 2),
            "final_capital": round(final_capital, 2),
        }

    @property
    def trades(self) -> List[TradeResult]:
        """Access list of individual trade results."""
        return self._trades

    @property
    def equity_curve(self) -> List[float]:
        """Access the equity curve over time."""
        return self._equity_curve

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_entry_exit(
        self,
        prices: List[Tuple[str, float]],
        timestamp: Optional[str],
    ) -> Tuple[Optional[float], Optional[float]]:
        """Pick entry (t) and exit (t+1) prices from chronological price list."""
        if timestamp is None:
            # Use first available pair
            if len(prices) >= 2:
                return prices[0][1], prices[1][1]
            return None, None

        for i, (date_str, price) in enumerate(prices):
            if date_str >= timestamp and i + 1 < len(prices):
                return price, prices[i + 1][1]

        return None, None

    def _simulate_trade(
        self,
        pred: Prediction,
        entry_price: float,
        exit_price: float,
        capital: float,
    ) -> TradeResult:
        """Simulate a single long/short trade based on direction prediction."""
        alloc = capital * self.position_size
        shares = alloc / entry_price if entry_price > 0 else 0

        if pred.direction == "UP":
            raw_pnl = (exit_price - entry_price) * shares
            correct = exit_price > entry_price
        elif pred.direction == "DOWN":
            raw_pnl = (entry_price - exit_price) * shares
            correct = exit_price < entry_price
        else:
            # FLAT – no position taken
            raw_pnl = 0.0
            correct = abs(exit_price - entry_price) / entry_price < 0.005

        pnl_pct = raw_pnl / alloc if alloc > 0 else 0.0

        return TradeResult(
            ticker=pred.ticker,
            direction=pred.direction,
            confidence=pred.confidence,
            entry_price=entry_price,
            exit_price=exit_price,
            pnl=round(raw_pnl, 4),
            pnl_pct=round(pnl_pct, 4),
            correct=correct,
        )
