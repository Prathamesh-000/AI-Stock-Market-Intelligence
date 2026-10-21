"""Endpoints for fetching real-time RSS financial news feeds with sentiment tagging."""

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
import feedparser

logger = logging.getLogger("api.news")
router = APIRouter(prefix="/news", tags=["news"])

BULLISH_KEYWORDS = ["surge", "jump", "record", "beat", "rally", "growth", "breakthrough", "expansion", "profit", "bull", "upgrade"]
BEARISH_KEYWORDS = ["drop", "plunge", "fall", "miss", "halt", "loss", "fire", "investigation", "lawsuit", "delay", "downgrade", "cut"]

@router.get("/{ticker}")
async def get_news_feed(ticker: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Fetches and parses live financial headlines for a specific stock."""
    ticker_upper = ticker.upper()
    rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker_upper}&region=US&lang=en-US"
    
    try:
        feed = feedparser.parse(rss_url)
        articles = []
        for entry in feed.entries[:limit]:
            title = entry.get("title", "")
            lower_title = title.lower()
            
            # Simple sentiment tagger
            pos_matches = sum(1 for w in BULLISH_KEYWORDS if w in lower_title)
            neg_matches = sum(1 for w in BEARISH_KEYWORDS if w in lower_title)
            
            if pos_matches > neg_matches:
                sentiment = "BULLISH"
            elif neg_matches > pos_matches:
                sentiment = "BEARISH"
            else:
                sentiment = "NEUTRAL"

            articles.append({
                "ticker": ticker_upper,
                "headline": title,
                "summary": entry.get("summary", ""),
                "published": entry.get("published", ""),
                "link": entry.get("link", ""),
                "sentiment": sentiment,
            })
        return articles
    except Exception as e:
        logger.error(f"Error fetching news for {ticker_upper}: {e}")
        return []

