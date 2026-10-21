"""
scripts/run_pipeline.py
-----------------------
Main end-to-end pipeline runner:
1. Fetch latest news for all tickers
2. Process each headline through LLM
3. Run XGBoost predictions
4. Save results to database
"""

import sys
import json
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.nlp.llm_processor import LLMProcessor
from src.models.xgboost_model import MarketImpactXGBoost
from src.database.db import SessionLocal
from src.database.models import PredictionLog
import feedparser
import yfinance as yf

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

TICKERS = ['NVDA', 'AMD', 'AAPL', 'TSLA', 'MSFT']


def fetch_news(ticker: str, limit: int = 5) -> list[dict]:
    """Fetch latest news for a ticker via Yahoo Finance RSS."""
    url = f'https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US'
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:limit]:
        articles.append({
            'ticker': ticker,
            'headline': entry.get('title', ''),
            'summary': entry.get('summary', ''),
            'published': entry.get('published', '')
        })
    return articles


def run_pipeline(tickers: list[str] = TICKERS, news_per_ticker: int = 3):
    """Run the full prediction pipeline for all tickers."""
    llm = LLMProcessor()
    results = []

    for ticker in tickers:
        logger.info(f"Processing {ticker}...")
        articles = fetch_news(ticker, news_per_ticker)

        for article in articles:
            headline = article['headline']
            summary = article['summary']

            if not headline:
                continue

            try:
                # LLM extraction
                llm_features = llm.extract_features(headline, summary)

                # Load model
                from src.models.xgboost_model import MarketImpactXGBoost
                model = MarketImpactXGBoost(ticker)
                model.load()

                # Build feature vector
                features = {
                    'polarity_score': llm_features.get('sentiment_score', 0.0),
                    'subjectivity': 0.5,
                    'compound_score': llm_features.get('sentiment_score', 0.0),
                    'severity_score': {'HIGH': 1.0, 'MEDIUM': 0.5, 'LOW': 0.2}.get(
                        llm_features.get('severity', 'MEDIUM'), 0.5),
                    'magnitude_estimate': llm_features.get('magnitude_estimate', 5.0),
                    'rag_similarity': 0.0,
                    'is_earnings': 0,
                    'is_merger': 0,
                    'is_layoff': 0,
                    'is_regulatory': 0,
                    'rsi_14': 50.0,
                    'macd_signal': 0.0,
                    'volume_ratio': 1.0,
                    'price_momentum_5d': 0.0,
                }

                prediction = model.predict(features)
                logger.info(f"{ticker} | {headline[:60]}... → {prediction['direction']}")
                results.append({'ticker': ticker, 'headline': headline, **prediction})

            except Exception as e:
                logger.error(f"Error processing {ticker} article: {e}")
                continue

    logger.info(f"\nPipeline complete. Processed {len(results)} articles.")
    return results


if __name__ == '__main__':
    results = run_pipeline()
    print(json.dumps(results[:3], indent=2, default=str))
