"""Endpoints for executing model inference, retrieving historical logs, and exporting CSVs."""

import io
import csv
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.database.models import PredictionRecord
from backend.database.repositories import PredictionRepository
from backend.schemas import PredictionRequestSchema, PredictionResponseSchema
from backend.services import PredictionService

logger = logging.getLogger("api.predictions")
router = APIRouter(prefix="/predictions", tags=["predictions"])
service = PredictionService()

@router.post("/predict", response_model=PredictionResponseSchema)
async def predict_headline(
    req: PredictionRequestSchema,
    db: Session = Depends(get_db)
):
    """Processes a news headline through LLM NLP extraction and XGBoost classification."""
    try:
        result = service.analyze_headline(
            ticker=req.ticker,
            headline=req.headline,
            summary=req.summary or ""
        )
        
        # Persist to database
        repo = PredictionRepository(db)
        repo.create({
            "ticker": req.ticker.upper(),
            "headline": req.headline,
            "summary": req.summary,
            "direction": result.get("direction", "NEUTRAL"),
            "signal": result.get("signal", "HOLD"),
            "impact_score": float(result.get("impact_score", 5.0)),
            "sentiment_score": float(result.get("sentiment_score", 0.0)),
            "confidence_score": float(result.get("confidence_score", 60.0)),
            "volatility_risk": float(result.get("volatility_risk", 3.0)),
            "rag_similarity": float(result.get("rag_similarity", 0.0)),
        })

        return PredictionResponseSchema(
            ticker=req.ticker.upper(),
            headline=req.headline,
            direction=result.get("direction", "NEUTRAL"),
            signal=result.get("signal", "HOLD"),
            impact_score=float(result.get("impact_score", 5.0)),
            sentiment_score=float(result.get("sentiment_score", 0.0)),
            confidence_score=float(result.get("confidence_score", 60.0)),
            volatility_risk=float(result.get("volatility_risk", 3.0)),
            rag_similarity=float(result.get("rag_similarity", 0.0)),
            timestamp=datetime.utcnow(),
            details=result.get("features", {})
        )
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{ticker}")
async def get_prediction_history(
    ticker: str,
    limit: int = 50,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Retrieves stored historical predictions for a given stock symbol."""
    repo = PredictionRepository(db)
    records = repo.get_by_ticker(ticker, limit=limit)
    return [
        {
            "id": r.id,
            "ticker": r.ticker,
            "headline": r.headline,
            "direction": r.direction,
            "signal": r.signal,
            "impact_score": r.impact_score,
            "sentiment_score": r.sentiment_score,
            "confidence_score": r.confidence_score,
            "volatility_risk": r.volatility_risk,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else ""
        }
        for r in records
    ]

@router.get("/export/csv")
async def export_predictions_csv(db: Session = Depends(get_db)):
    """Exports all past predictions as a downloadable CSV report."""
    repo = PredictionRepository(db)
    records = repo.get_all(limit=500)
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Ticker", "Timestamp", "Headline", "Direction",
        "Signal", "Impact Score", "Sentiment Score", "Confidence (%)", "Risk"
    ])
    for r in records:
        writer.writerow([
            r.id,
            r.ticker,
            r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else "",
            r.headline,
            r.direction,
            r.signal,
            r.impact_score,
            r.sentiment_score,
            r.confidence_score,
            r.volatility_risk
        ])

    csv_content = output.getvalue()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=market_predictions.csv"}
    )

