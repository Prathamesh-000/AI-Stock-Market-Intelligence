import yfinance as yf
import pandas as pd
import logging
from typing import Dict, Optional
from src.data.data_provider import AbstractMarketProvider

logger = logging.getLogger(__name__)

class YFinanceMarketProvider(AbstractMarketProvider):
    """
    yfinance implementation of the Market Data Provider.
    """
    
    def fetch_historical_data(
        self, 
        ticker: str, 
        start_date: str, 
        end_date: str, 
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Fetches OHLCV and corporate action data from yfinance.
        """
        logger.info(f"Fetching yfinance data for {ticker} | {start_date} to {end_date} | {interval}")
        try:
            ticker_obj = yf.Ticker(ticker)
            
            # auto_adjust=False keeps Close and Adj Close distinct, useful for some backtesting logic
            # However, for ML, adjusted prices are generally preferred to handle splits/dividends.
            df = ticker_obj.history(start=start_date, end=end_date, interval=interval, auto_adjust=True)
            
            if df.empty:
                logger.warning(f"No data returned for {ticker} at interval {interval}. May be restricted or delisted.")
                return pd.DataFrame()
            
            df.reset_index(inplace=True)
            
            # Ensure standard column naming
            # Date/Datetime, Open, High, Low, Close, Volume, Dividends, Stock Splits
            if 'Date' in df.columns:
                df.rename(columns={'Date': 'Timestamp'}, inplace=True)
            elif 'Datetime' in df.columns:
                df.rename(columns={'Datetime': 'Timestamp'}, inplace=True)
                
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker} via yfinance: {str(e)}")
            return pd.DataFrame()

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
        Fetches data for the stock, the broad market, and the sector.
        Gracefully handles missing data by returning empty DataFrames for those symbols.
        """
        results = {}
        for symbol in [ticker, benchmark, sector]:
            if not symbol:
                continue
            df = self.fetch_historical_data(symbol, start_date, end_date, interval)
            results[symbol] = df
            
        return results

