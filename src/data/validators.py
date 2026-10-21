"""
Data validation utilities.

Provides validation helpers for tickers, headlines, and prediction requests
before they are passed to NLP/ML pipelines.
"""

from __future__ import annotations

import re
from typing import Tuple

# Allowed US equity tickers – extend as needed.
ALLOWED_TICKERS = {
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "TSLA", "NVDA",
    "AMD", "INTC", "NFLX", "BABA", "JPM", "GS", "MS", "BAC", "WFC",
    "V", "MA", "PYPL", "DIS", "NFLX", "UBER", "LYFT", "SNAP", "TWTR",
    "CRM", "ORCL", "SAP", "IBM", "CSCO", "QCOM", "TXN", "AVGO",
    "SPY", "QQQ", "IWM", "DIA",  # ETFs
}

_TICKER_RE = re.compile(r"^[A-Z]{1,5}$")

MIN_HEADLINE_LEN = 10
MAX_HEADLINE_LEN = 512
MAX_SUMMARY_LEN = 4096


def validate_ticker(ticker: str) -> bool:
    """
    Validate that a ticker symbol is in the allowed list and well-formed.

    Args:
        ticker: Raw ticker string (e.g. ``"AAPL"``).

    Returns:
        ``True`` if the ticker is valid, ``False`` otherwise.
    """
    if not ticker or not isinstance(ticker, str):
        return False
    ticker = ticker.strip().upper()
    if not _TICKER_RE.match(ticker):
        return False
    return ticker in ALLOWED_TICKERS


def validate_headline(headline: str) -> bool:
    """
    Validate a news headline.

    Rules:
    - Must be a non-empty string.
    - Length must be between :data:`MIN_HEADLINE_LEN` and :data:`MAX_HEADLINE_LEN`.

    Args:
        headline: Raw headline text.

    Returns:
        ``True`` if valid.
    """
    if not headline or not isinstance(headline, str):
        return False
    stripped = headline.strip()
    return MIN_HEADLINE_LEN <= len(stripped) <= MAX_HEADLINE_LEN


def validate_summary(summary: str) -> bool:
    """
    Validate a news article summary / body text.

    Args:
        summary: Raw summary text.

    Returns:
        ``True`` if valid (non-empty, within length limit).
    """
    if not summary or not isinstance(summary, str):
        return False
    return 0 < len(summary.strip()) <= MAX_SUMMARY_LEN


def validate_prediction_request(
    ticker: str,
    headline: str,
    summary: str,
) -> Tuple[bool, str]:
    """
    Validate a complete prediction request payload.

    Args:
        ticker: Stock ticker symbol.
        headline: News headline string.
        summary: News article body / summary.

    Returns:
        A tuple ``(is_valid: bool, error_message: str)``.
        ``error_message`` is an empty string when valid.
    """
    if not validate_ticker(ticker):
        return False, (
            f"Invalid or unsupported ticker '{ticker}'. "
            f"Supported tickers: {sorted(ALLOWED_TICKERS)}"
        )

    if not validate_headline(headline):
        return False, (
            f"Headline must be between {MIN_HEADLINE_LEN} and {MAX_HEADLINE_LEN} "
            "characters and must not be empty."
        )

    if not validate_summary(summary):
        return False, (
            f"Summary must be a non-empty string up to {MAX_SUMMARY_LEN} characters."
        )

    return True, ""
