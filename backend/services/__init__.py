"""Business logic services orchestrating market data, NLP parsing, and inference."""

import logging
from typing import List, Dict, Any, Optional
from src.data.market_data import MarketDataProvider
from src.nlp.llm_processor import LLMProcessor
from src.models.xgboost_model import MarketImpactXGBoost

logger = logging.getLogger("backend.services")

class PredictionService:
    """Service layer coordinating news feature extraction and model prediction."""

    def __init__(self):
        self.market_provider = MarketDataProvider()
        self.llm_processor = LLMProcessor()

    def analyze_headline(self, ticker: str, headline: str, summary: str = "") -> Dict[str, Any]:
        """Runs the complete inference pipeline for a given stock and news event."""
        model = MarketImpactXGBoost(ticker)
        model.load()
        
        nlp_features = self.llm_processor.extract_features(headline, summary)
        
        features = {
            "polarity_score": nlp_features.get("sentiment_score", 0.0),
            "subjectivity": 0.5,
            "compound_score": nlp_features.get("sentiment_score", 0.0),
            "severity_score": 0.5,
            "magnitude_estimate": nlp_features.get("magnitude_estimate", 5.0),
            "rag_similarity": 0.0,
            "is_earnings": 1 if "earnings" in headline.lower() else 0,
            "is_merger": 1 if any(w in headline.lower() for w in ["deal", "merger", "acquire"]) else 0,
            "is_layoff": 1 if "layoff" in headline.lower() else 0,
            "is_regulatory": 1 if any(w in headline.lower() for w in ["sec", "investigation", "fine"]) else 0,
            "rsi_14": 52.0,
            "macd_signal": 0.0,
            "volume_ratio": 1.0,
            "price_momentum_5d": 0.0,
        }
        
        prediction = model.predict(features)
        prediction["headline"] = headline
        prediction["ticker"] = ticker
        return prediction

__all__ = ["PredictionService"]

