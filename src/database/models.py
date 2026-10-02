from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from src.database.db import Base

class PredictionLog(Base):
    """
    SQLAlchemy ORM Model representing a single AI Prediction / Trade Signal.
    """
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # The context of the prediction
    ticker = Column(String(10), index=True, nullable=False)
    headline = Column(String(500), nullable=False)
    
    # The AI's output
    signal = Column(String(20), nullable=False) # 'BUY', 'SELL', 'UNCERTAIN'
    confidence_score = Column(Float, nullable=False) # 0.0 to 100.0
    
    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # For Phase 13 (Backtesting): We will eventually fill this in with the actual 
    # market return to see if the AI was correct.
    actual_return = Column(Float, nullable=True)
    is_correct = Column(Integer, nullable=True) # 1 for True, 0 for False
