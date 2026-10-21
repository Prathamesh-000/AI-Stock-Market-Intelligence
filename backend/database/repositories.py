"""Data access repository for querying and persisting predictions."""

from typing import List, Optional
from sqlalchemy.orm import Session
from backend.database.models import PredictionRecord

class PredictionRepository:
    """Encapsulates database operations for prediction logs."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, record_data: dict) -> PredictionRecord:
        """Persists a new prediction record."""
        record = PredictionRecord(**record_data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_by_ticker(self, ticker: str, limit: int = 50) -> List[PredictionRecord]:
        """Fetches the latest prediction records for a specific stock."""
        return (
            self.db.query(PredictionRecord)
            .filter(PredictionRecord.ticker == ticker.upper())
            .order_by(PredictionRecord.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_all(self, limit: int = 100) -> List[PredictionRecord]:
        """Retrieves recent records across all supported stocks."""
        return (
            self.db.query(PredictionRecord)
            .order_by(PredictionRecord.created_at.desc())
            .limit(limit)
            .all()
        )
