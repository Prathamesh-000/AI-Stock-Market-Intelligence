from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime

class AbstractMarketProvider(ABC):
    """
    Abstract base class for market data providers (yfinance, Alpaca, Polygon, etc.)
    Ensures the rest of the application is independent of the specific data vendor.
    """
    
    @abstractmethod
    def fetch_historical_data(
        self, 
        ticker: str, 
        start_date: str, 
        end_date: str, 
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV data for a given ticker.
        """
        pass

    @abstractmethod
    def fetch_market_and_benchmarks(
        self, 
        ticker: str, 
        benchmark: str, 
        sector: str, 
        start_date: str, 
        end_date: str, 
        interval: str = "1d"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for the target stock, broad market benchmark, and sector benchmark.
        Returns a dictionary mapping ticker to its DataFrame.
        """
        pass


class AbstractNewsProvider(ABC):
    """
    Abstract base class for financial news providers (Finnhub, Yahoo, Alpha Vantage, etc.)
    """
    
    @abstractmethod
    def fetch_news(
        self, 
        ticker: str, 
        start_date: str, 
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Fetch financial news for a specific ticker.
        Must return a list of dictionaries adhering to the canonical schema:
        {
            "event_id": str,
            "ticker": str,
            "headline": str,
            "summary": str,
            "publisher": str,
            "url": str,
            "published_at": str (ISO 8601),
            "collected_at": str (ISO 8601),
            "source": str,
            "raw_data": dict (original provider payload)
        }
        """
        pass

