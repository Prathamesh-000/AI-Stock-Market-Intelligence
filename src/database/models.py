from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from src.database.db import Base

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticker = Column(String(10), index=True, nullable=False)
    headline = Column(String(500), nullable=False)
    signal = Column(String(20), nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    predicted_impact = Column(Float, nullable=True)
    actual_return = Column(Float, nullable=True)
    is_correct = Column(Integer, nullable=True)
