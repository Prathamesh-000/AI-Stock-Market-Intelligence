import finnhub
import yfinance as yf
import logging
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any
from src.data.data_provider import AbstractNewsProvider

logger = logging.getLogger(__name__)

class FinnhubNewsProvider(AbstractNewsProvider):
    def __init__(self, api_key: str):
        self.client = finnhub.Client(api_key=api_key)

    def fetch_news(self, ticker: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        logger.info(f"Fetching Finnhub news for {ticker} | {start_date} to {end_date}")
        normalized_news = []
        try:
            # Finnhub requires YYYY-MM-DD
            raw_news = self.client.company_news(ticker, _from=start_date, to=end_date)
            
            for item in raw_news:
                # Convert unix timestamp to ISO 8601
                pub_time = datetime.fromtimestamp(item.get('datetime', 0), tz=timezone.utc)
                
                # Create a deterministic event ID based on url or headline + time
                unique_str = f"{item.get('url', '')}_{item.get('headline', '')}"
                event_id = hashlib.md5(unique_str.encode('utf-8')).hexdigest()
                
                normalized_record = {
                    "event_id": event_id,
                    "ticker": ticker,
                    "headline": item.get("headline", ""),
                    "summary": item.get("summary", ""),
                    "publisher": item.get("source", ""),
                    "url": item.get("url", ""),
                    "published_at": pub_time.isoformat(),
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "source": "Finnhub",
                    "raw_data": item  # Preserve original raw response
                }
                normalized_news.append(normalized_record)
        except Exception as e:
            logger.error(f"Error fetching Finnhub news for {ticker}: {str(e)}")
            
        return normalized_news


class YahooNewsProvider(AbstractNewsProvider):
    def fetch_news(self, ticker: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Note: yfinance ticker.news only returns recent news (usually last 30-40 items).
        It does not fully support date filtering via the API, so we fetch all available
        and filter locally.
        """
        logger.info(f"Fetching Yahoo news for {ticker}")
        normalized_news = []
        try:
            ticker_obj = yf.Ticker(ticker)
            raw_news = ticker_obj.news
            
            start_dt = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            end_dt = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            
            for item in raw_news:
                pub_time = datetime.fromtimestamp(item.get('providerPublishTime', 0), tz=timezone.utc)
                
                # Filter by requested date range
                if not (start_dt <= pub_time <= end_dt):
                    continue
                    
                unique_str = f"{item.get('link', '')}_{item.get('title', '')}"
                event_id = hashlib.md5(unique_str.encode('utf-8')).hexdigest()
                
                normalized_record = {
                    "event_id": event_id,
                    "ticker": ticker,
                    "headline": item.get("title", ""),
                    "summary": item.get("summary", ""),
                    "publisher": item.get("publisher", ""),
                    "url": item.get("link", ""),
                    "published_at": pub_time.isoformat(),
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "source": "Yahoo",
                    "raw_data": item
                }
                normalized_news.append(normalized_record)
        except Exception as e:
            logger.error(f"Error fetching Yahoo news for {ticker}: {str(e)}")
            
        return normalized_news

