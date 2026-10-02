import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from config.settings import settings
from src.models.xgboost_model import MarketImpactXGBoost
from src.api.ws_manager import manager

logger = logging.getLogger(__name__)
router = APIRouter()

# Global memory cache for the model
loaded_models = {}

class PredictionRequest(BaseModel):
    ticker: str
    headline: str
    summary: str

def get_model_and_calibrator(ticker: str):
    """Loads the model and calibrator lazily and caches them."""
    if ticker in loaded_models:
        return loaded_models[ticker]
        
    model_dir = settings.project_root / "models" / "saved"
    model_path = model_dir / f"xgb_{ticker}_latest.json"
    calib_path = model_dir / f"calibrator_{ticker}_latest.pkl"
    
    if not model_path.exists():
        raise HTTPException(status_code=404, detail=f"No trained model found for {ticker}")
        
    # Load XGBoost
    xgb_model = MarketImpactXGBoost()
    xgb_model.load_model(str(model_path))
    
    # Load Calibrator
    calibrator = None
    if calib_path.exists():
        try:
            calibrator = joblib.load(str(calib_path))
        except Exception as e:
            logger.warning(f"Could not load calibrator for {ticker}: {e}")
            
    loaded_models[ticker] = (xgb_model, calibrator)
    return xgb_model, calibrator

async def run_prediction_pipeline(request: PredictionRequest):
    """
    Simulates the entire inference pipeline:
    1. Grabs live market data (Simulated here by pulling the last row of our dataset)
    2. Runs FinBERT (Simulated)
    3. Feeds into XGBoost
    4. Pushes result to WebSockets
    """
    try:
        xgb_model, calibrator = get_model_and_calibrator(request.ticker)
        
        # In a full production system, we would run FinBERT on the request text here
        # and fetch live Yahoo Finance data to build the feature vector.
        # For this Phase 10 demo, we will load the last known feature row for this ticker 
        # to guarantee the shape matches the model perfectly.
        dataset_path = settings.data_dir / "processed" / f"{request.ticker}_final_dataset.csv"
        if not dataset_path.exists():
            return
            
        df = pd.read_csv(dataset_path)
        
        # Exact preprocessing as in training
        cols_to_drop = [
            'event_id', 'headline', 'summary', 'url', 'publisher', 'source', 
            'published_at', 'duplicate_sources', 'Direction', 'CAR_1d', 'Impact_Score',
            'Fwd_Ret_1d', 'Fwd_Ret_1d_SPY', 'Timestamp', 'market_reaction_time', 'Target'
        ]
        df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
        
        if 'event_type' in df.columns:
            df = pd.get_dummies(df, columns=['event_type'], drop_first=True)
            
        df = df.select_dtypes(include=[np.number])
        
        # Grab the very latest state of the market
        X_live = df.iloc[[-1]]
        
        # Predict
        raw_prob = xgb_model.predict_proba(X_live)[0]
        
        # Calibrate
        final_prob = raw_prob
        if calibrator is not None and calibrator.calibrator is not None:
            # Calibrator expects 2D array
            raw_prob_2d = np.array([[raw_prob]])
            final_prob = calibrator.predict_proba(X_live)[0] # Or use calibrator if it was platt scaled directly
            # Wait, in calibration.py, predict_proba expects X, not raw_prob.
            final_prob = calibrator.predict_proba(X_live)[0]
            
        # Determine Signal
        signal = "UNCERTAIN"
        if final_prob > 0.60:
            signal = "BUY"
        elif final_prob < 0.40:
            signal = "SELL"
            
        # Construct the payload
        payload = {
            "ticker": request.ticker,
            "headline": request.headline,
            "signal": signal,
            "confidence_score": round(float(final_prob) * 100, 2),
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
        # Broadcast via WebSockets
        await manager.broadcast(payload)
        logger.info(f"Broadcasted prediction: {payload}")
        
    except Exception as e:
        logger.error(f"Pipeline error: {e}")

@router.post("/predict")
async def trigger_prediction(request: PredictionRequest, background_tasks: BackgroundTasks):
    """
    REST Endpoint. Receives a news headline and triggers the AI pipeline in the background.
    """
    background_tasks.add_task(run_prediction_pipeline, request)
    return {"status": "Processing", "message": "Prediction pipeline started. Result will be broadcasted via WebSocket."}
