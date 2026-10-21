"""
Entity linking – extracts named entities from financial text and maps
company names to their stock ticker symbols.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Company-name → ticker mapping (extend as needed)
# ---------------------------------------------------------------------------
_COMPANY_TO_TICKER: Dict[str, str] = {
    "apple": "AAPL",
    "apple inc": "AAPL",
    "microsoft": "MSFT",
    "microsoft corporation": "MSFT",
    "alphabet": "GOOGL",
    "google": "GOOGL",
    "amazon": "AMZN",
    "amazon.com": "AMZN",
    "meta": "META",
    "meta platforms": "META",
    "facebook": "META",
    "tesla": "TSLA",
    "nvidia": "NVDA",
    "amd": "AMD",
    "advanced micro devices": "AMD",
    "intel": "INTC",
    "intel corporation": "INTC",
    "netflix": "NFLX",
    "alibaba": "BABA",
    "jpmorgan": "JPM",
    "jp morgan": "JPM",
    "goldman sachs": "GS",
    "morgan stanley": "MS",
    "bank of america": "BAC",
    "wells fargo": "WFC",
    "visa": "V",
    "mastercard": "MA",
    "paypal": "PYPL",
    "disney": "DIS",
    "walt disney": "DIS",
    "uber": "UBER",
    "lyft": "LYFT",
    "snap": "SNAP",
    "snapchat": "SNAP",
    "salesforce": "CRM",
    "oracle": "ORCL",
    "ibm": "IBM",
    "cisco": "CSCO",
    "qualcomm": "QCOM",
    "texas instruments": "TXN",
    "broadcom": "AVGO",
}

# Regex for raw ticker-like patterns (1–5 uppercase letters, optionally $-prefixed)
_TICKER_RE = re.compile(r"\b\$?([A-Z]{1,5})\b")

# Simple heuristic for person names (title case, 2–3 words)
_PERSON_RE = re.compile(
    r"\b(?:Mr\.|Ms\.|Dr\.|CEO|CFO|CTO)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b"
)


def extract_entities(text: str) -> List[Dict]:
    """
    Extract named entities (companies, tickers, people) from text.

    Args:
        text: Raw news headline or article body.

    Returns:
        List of entity dicts::

            [
                {"type": "ticker",  "text": "AAPL",       "ticker": "AAPL"},
                {"type": "company", "text": "Apple",      "ticker": "AAPL"},
                {"type": "person",  "text": "Tim Cook",   "ticker": None},
            ]
    """
    entities: List[Dict] = []
    seen: set = set()

    # --- Raw ticker mentions ---
    for match in _TICKER_RE.finditer(text):
        candidate = match.group(1)
        if candidate in _get_known_tickers() and candidate not in seen:
            seen.add(candidate)
            entities.append({"type": "ticker", "text": candidate, "ticker": candidate})

    # --- Company name mentions ---
    text_lower = text.lower()
    for company_name, ticker in _COMPANY_TO_TICKER.items():
        if company_name in text_lower and ticker not in seen:
            seen.add(ticker)
            entities.append(
                {"type": "company", "text": company_name.title(), "ticker": ticker}
            )

    # --- Person name mentions ---
    for match in _PERSON_RE.finditer(text):
        person = match.group(0).strip()
        if len(person) > 4 and person not in seen:
            seen.add(person)
            entities.append({"type": "person", "text": person, "ticker": None})

    return entities


def link_to_ticker(entity: str) -> Optional[str]:
    """
    Map a company name or raw ticker string to a ticker symbol.

    Args:
        entity: Company name (e.g. ``"Apple"``) or ticker (e.g. ``"AAPL"``).

    Returns:
        Ticker symbol if found, ``None`` otherwise.
    """
    if not entity:
        return None

    stripped = entity.strip()

    # Direct ticker match (uppercase)
    upper = stripped.upper()
    if upper in _get_known_tickers():
        return upper

    # Company name lookup (case-insensitive)
    lower = stripped.lower()
    return _COMPANY_TO_TICKER.get(lower)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_known_tickers() -> set:
    """Return the set of all tickers present in the mapping."""
    return set(_COMPANY_TO_TICKER.values())
