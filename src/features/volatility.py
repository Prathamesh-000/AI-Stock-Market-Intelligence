import pandas as pd
import numpy as np

class VolatilityFeatures:
    """
    Calculates volatility metrics like Average True Range (ATR) and Bollinger Bands.
    """
    
    @staticmethod
    def add_atr(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """Average True Range (ATR) - Measures absolute volatility"""
        df = df.copy()
        
        # True Range calculation
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        
        # ATR is the moving average of True Range
        df[f'ATR_{window}'] = true_range.rolling(window=window).mean()
        
        # Normalized ATR (ATR as a percentage of Close price)
        df[f'NATR_{window}'] = (df[f'ATR_{window}'] / df['Close']) * 100
        return df

    @staticmethod
    def add_bollinger_bands(df: pd.DataFrame, column: str = 'Close', window: int = 20, num_std: int = 2) -> pd.DataFrame:
        """Bollinger Bands - Measures relative volatility and extremes"""
        df = df.copy()
        rolling_mean = df[column].rolling(window=window).mean()
        rolling_std = df[column].rolling(window=window).std()
        
        df['BB_Mid'] = rolling_mean
        df['BB_Upper'] = rolling_mean + (rolling_std * num_std)
        df['BB_Lower'] = rolling_mean - (rolling_std * num_std)
        
        # %B indicator (where price is relative to the bands: >1 is above upper, <0 is below lower)
        df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Mid']
        df['BB_Pct'] = (df[column] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
        return df
