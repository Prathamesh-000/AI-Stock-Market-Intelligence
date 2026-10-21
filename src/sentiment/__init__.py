"""Sentiment package – exports entity linking and severity utilities."""

from .entity_linking import extract_entities, link_to_ticker
from .severity import classify_severity, get_severity_multiplier

__all__ = [
    "extract_entities",
    "link_to_ticker",
    "classify_severity",
    "get_severity_multiplier",
]
