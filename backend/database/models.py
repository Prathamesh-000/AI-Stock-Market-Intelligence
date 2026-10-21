"""SQLAlchemy ORM models for logging predictions and historical market snapshots."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from backend.database.session import Base

class PredictionRecord(Base):
    """Stores full historical AI inference logs for auditable trade history."""
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    headline = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    direction = Column(String(20), nullable=False)
    signal = Column(String(20), nullable=False)
    impact_score = Column(Float, nullable=False)
    sentiment_score = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    volatility_risk = Column(Float, nullable=False)
    rag_similarity = Column(Float, nullable=True, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class MarketSnapshot(Base):
    """Stores periodic OHLCV quotes and market regime indicators."""
    __tablename__ = "market_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    price = Column(Float, nullable=False)
    change_pct = Column(Float, nullable=False)
    volume = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

