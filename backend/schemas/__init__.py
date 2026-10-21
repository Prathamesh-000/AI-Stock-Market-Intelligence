"""Pydantic schemas for request validation and response serialization."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class StockQuote(BaseModel):
    ticker: str
    price: float
    change: float
    change_pct: float
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class NewsArticle(BaseModel):
    id: Optional[str] = None
    ticker: str
    headline: str
    summary: str
    source: Optional[str] = "Yahoo Finance"
    url: Optional[str] = None
    published_at: Optional[str] = None
    sentiment_polarity: Optional[float] = 0.0

class PredictionRequestSchema(BaseModel):
    ticker: str = Field(..., description="Stock symbol (e.g., NVDA, AAPL, AMD, TSLA, MSFT)")
    headline: str = Field(..., min_length=5, description="Financial news headline")
    summary: Optional[str] = Field("", description="Detailed news summary or body context")

class PredictionResponseSchema(BaseModel):
    ticker: str
    headline: str
    direction: str = Field(..., description="BULLISH, BEARISH, or NEUTRAL")
    signal: str = Field(..., description="STRONG BUY, BUY, HOLD, SELL, or STRONG SELL")
    impact_score: float = Field(..., description="Predicted price impact (0-10)")
    sentiment_score: float = Field(..., description="Polarity score (-1.0 to 1.0)")
    confidence_score: float = Field(..., description="Calibrated model confidence (0-100%)")
    volatility_risk: float = Field(..., description="Estimated risk score (0-10)")
    rag_similarity: float = Field(..., description="Historical context similarity (0-100%)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[Dict[str, Any]] = None

__all__ = [
    "StockQuote",
    "NewsArticle",
    "PredictionRequestSchema",
    "PredictionResponseSchema",
]

