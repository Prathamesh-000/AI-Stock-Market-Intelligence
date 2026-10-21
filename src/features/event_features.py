"""
Event feature engineering for news headlines and summaries.

Extracts boolean flags and numerical features that are used downstream
by the XGBoost impact-prediction model.
"""

from __future__ import annotations

import re
from typing import Dict

# ---------------------------------------------------------------------------
# Keyword sets – extend to improve recall
# ---------------------------------------------------------------------------

_EARNINGS_KEYWORDS = {
    "earnings", "eps", "revenue", "profit", "loss", "quarterly results",
    "beats estimates", "misses estimates", "guidance", "forecast",
    "net income", "operating income", "ebitda",
}

_ACQUISITION_KEYWORDS = {
    "acquires", "acquisition", "merger", "takeover", "buyout", "buys",
    "deal", "purchase", "bid for", "offer to buy", "acquired by",
    "strategic combination",
}

_LAYOFF_KEYWORDS = {
    "layoff", "layoffs", "job cuts", "workforce reduction", "downsizing",
    "redundancies", "retrenchment", "fired", "let go", "restructuring",
    "headcount reduction",
}

_FDA_KEYWORDS = {
    "fda", "food and drug administration", "approval", "approved",
    "clinical trial", "phase 3", "phase 2", "drug approval", "nda",
    "biologics", "pdufa", "breakthrough therapy",
}

_LAWSUIT_KEYWORDS = {
    "lawsuit", "sued", "sues", "litigation", "legal action", "court",
    "settlement", "class action", "regulatory fine", "penalty",
    "investigation", "subpoena", "antitrust",
}

_PARTNERSHIP_KEYWORDS = {
    "partnership", "collaboration", "joint venture", "strategic alliance",
    "agreement", "contract", "deal signed", "mou", "memorandum",
}

_LEADERSHIP_KEYWORDS = {
    "ceo", "cfo", "coo", "cto", "president", "resigns", "appointed",
    "steps down", "named", "hire", "executive",
}


def _contains_any(text_lower: str, keywords: set) -> bool:
    """Return True if any keyword appears in the lower-cased text."""
    return any(kw in text_lower for kw in keywords)


def extract_event_features(headline: str, summary: str) -> Dict[str, float]:
    """
    Extract structured event features from a news headline and summary.

    Args:
        headline: News headline string.
        summary:  News article body or summary.

    Returns:
        A dict of feature name -> float (booleans encoded as 0.0 / 1.0).

    Example::

        features = extract_event_features(
            "Apple beats earnings estimates by 15%",
            "Apple Inc. reported Q4 earnings ...",
        )
        # {"has_earnings": 1.0, "has_acquisition": 0.0, ...}
    """
    combined = (headline + " " + summary).lower()
    words = re.findall(r"\b\w+\b", combined)
    headline_lower = headline.lower()

    features: Dict[str, float] = {
        # Boolean event flags (0.0 / 1.0)
        "has_earnings": float(_contains_any(combined, _EARNINGS_KEYWORDS)),
        "has_acquisition": float(_contains_any(combined, _ACQUISITION_KEYWORDS)),
        "has_layoff": float(_contains_any(combined, _LAYOFF_KEYWORDS)),
        "has_fda_approval": float(_contains_any(combined, _FDA_KEYWORDS)),
        "has_lawsuit": float(_contains_any(combined, _LAWSUIT_KEYWORDS)),
        "has_partnership": float(_contains_any(combined, _PARTNERSHIP_KEYWORDS)),
        "has_leadership_change": float(_contains_any(combined, _LEADERSHIP_KEYWORDS)),
        # Numeric / linguistic features
        "word_count": float(len(words)),
        "headline_word_count": float(len(re.findall(r"\b\w+\b", headline_lower))),
        "exclamation_count": float(headline.count("!") + summary.count("!")),
        "question_count": float(headline.count("?") + summary.count("?")),
        "uppercase_ratio": (
            sum(1 for c in headline if c.isupper()) / max(len(headline), 1)
        ),
        "number_count": float(len(re.findall(r"\d+", combined))),
        "percent_mentions": float(len(re.findall(r"\d+\.?\d*\s*%", combined))),
        # Multi-event flag (more than one type of event)
        "is_multi_event": float(
            sum([
                _contains_any(combined, _EARNINGS_KEYWORDS),
                _contains_any(combined, _ACQUISITION_KEYWORDS),
                _contains_any(combined, _LAYOFF_KEYWORDS),
                _contains_any(combined, _FDA_KEYWORDS),
                _contains_any(combined, _LAWSUIT_KEYWORDS),
            ]) > 1
        ),
    }

    return features
