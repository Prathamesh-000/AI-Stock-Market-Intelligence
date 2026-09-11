import pandas as pd
import logging

logger = logging.getLogger(__name__)

class MarketCleaner:
    """
    Cleans raw OHLCV market data, handling missing values and anomalies.
    """
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
            
        cleaned_df = df.copy()
        
        # Ensure Timestamp is datetime
        if 'Timestamp' in cleaned_df.columns:
            # Drop timezone info if it exists to make it easier to work with locally
            cleaned_df['Timestamp'] = pd.to_datetime(cleaned_df['Timestamp'], utc=True)
            cleaned_df.sort_values('Timestamp', inplace=True)
            
        # Drop rows where Volume is exactly 0 or missing (usually indicates market was closed or glitch)
        if 'Volume' in cleaned_df.columns:
            original_len = len(cleaned_df)
            cleaned_df = cleaned_df[cleaned_df['Volume'] > 0]
            dropped = original_len - len(cleaned_df)
            if dropped > 0:
                logger.info(f"Dropped {dropped} rows with zero volume.")

        # Forward fill missing price data
        price_cols = ['Open', 'High', 'Low', 'Close']
        for col in price_cols:
            if col in cleaned_df.columns:
                cleaned_df[col] = cleaned_df[col].ffill()
                
        # Drop any remaining NaNs
        cleaned_df.dropna(subset=['Close'], inplace=True)
        
        return cleaned_df

