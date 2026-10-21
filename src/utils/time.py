"""
Time utilities for US equity market hours.

All times are in US Eastern Time (ET).  The implementation avoids heavy
dependencies – it uses the stdlib ``datetime``, ``zoneinfo`` (Python 3.9+),
or falls back to a UTC offset when ``zoneinfo`` is unavailable.
"""

from __future__ import annotations

import datetime
from typing import Dict

try:
    from zoneinfo import ZoneInfo
    _ET = ZoneInfo("America/New_York")
    _HAS_ZONEINFO = True
except Exception:
    _ET = None  # type: ignore
    _HAS_ZONEINFO = False

# NYSE / NASDAQ regular session (Eastern Time)
_MARKET_OPEN_HOUR = 9
_MARKET_OPEN_MINUTE = 30
_MARKET_CLOSE_HOUR = 16
_MARKET_CLOSE_MINUTE = 0

# Weekday indices: Monday=0, …, Friday=4, Saturday=5, Sunday=6
_TRADING_DAYS = {0, 1, 2, 3, 4}  # Mon–Fri (holidays not considered)


def get_market_hours() -> Dict[str, str]:
    """
    Return the regular NYSE/NASDAQ session hours in ET.

    Returns:
        Dict with keys ``"open"`` and ``"close"`` (HH:MM strings).
    """
    return {
        "open": f"{_MARKET_OPEN_HOUR:02d}:{_MARKET_OPEN_MINUTE:02d}",
        "close": f"{_MARKET_CLOSE_HOUR:02d}:{_MARKET_CLOSE_MINUTE:02d}",
        "timezone": "America/New_York",
    }


def _now_et() -> datetime.datetime:
    """Return current datetime in US Eastern Time."""
    if _HAS_ZONEINFO:
        return datetime.datetime.now(tz=_ET)
    # Fallback: approximate ET as UTC-5 (ignores DST)
    utc_now = datetime.datetime.now(tz=datetime.timezone.utc)
    et_offset = datetime.timezone(datetime.timedelta(hours=-5))
    return utc_now.astimezone(et_offset)


def is_market_open() -> bool:
    """
    Check whether the US stock market is currently open.

    Considers weekdays only – does not account for public holidays.

    Returns:
        ``True`` if the current ET time falls within regular trading hours
        on a weekday.
    """
    now = _now_et()
    if now.weekday() not in _TRADING_DAYS:
        return False

    open_time = now.replace(
        hour=_MARKET_OPEN_HOUR, minute=_MARKET_OPEN_MINUTE, second=0, microsecond=0
    )
    close_time = now.replace(
        hour=_MARKET_CLOSE_HOUR, minute=_MARKET_CLOSE_MINUTE, second=0, microsecond=0
    )
    return open_time <= now < close_time


def get_next_trading_day(date: datetime.date) -> datetime.date:
    """
    Return the next calendar day that is a trading day (Mon–Fri).

    Args:
        date: Reference date.

    Returns:
        Next trading date after *date* (skips weekends).
    """
    if isinstance(date, datetime.datetime):
        date = date.date()

    next_day = date + datetime.timedelta(days=1)
    while next_day.weekday() not in _TRADING_DAYS:
        next_day += datetime.timedelta(days=1)
    return next_day


def seconds_until_open() -> int:
    """
    Return the number of seconds until the next market open.

    Returns 0 if the market is currently open.
    """
    if is_market_open():
        return 0

    now = _now_et()
    today_open = now.replace(
        hour=_MARKET_OPEN_HOUR, minute=_MARKET_OPEN_MINUTE, second=0, microsecond=0
    )

    if now < today_open and now.weekday() in _TRADING_DAYS:
        return int((today_open - now).total_seconds())

    # Find next trading day's open
    next_date = get_next_trading_day(now.date())
    next_open = datetime.datetime(
        next_date.year,
        next_date.month,
        next_date.day,
        _MARKET_OPEN_HOUR,
        _MARKET_OPEN_MINUTE,
        tzinfo=now.tzinfo,
    )
    return int((next_open - now).total_seconds())
