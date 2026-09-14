import pandas as pd
import numpy as np

class TechnicalFeatures:
    """
    Calculates trend and momentum indicators using standard pandas operations.
    """
    
    @staticmethod
    def add_sma(df: pd.DataFrame, column: str = 'Close', windows: list = [10, 20, 50, 200]) -> pd.DataFrame:
        """Simple Moving Average"""
        df = df.copy()
        for window in windows:
            df[f'SMA_{window}'] = df[column].rolling(window=window).mean()
        return df

    @staticmethod
    def add_ema(df: pd.DataFrame, column: str = 'Close', windows: list = [12, 26]) -> pd.DataFrame:
        """Exponential Moving Average"""
        df = df.copy()
        for window in windows:
            df[f'EMA_{window}'] = df[column].ewm(span=window, adjust=False).mean()
        return df

    @staticmethod
    def add_rsi(df: pd.DataFrame, column: str = 'Close', window: int = 14) -> pd.DataFrame:
        """Relative Strength Index (RSI)"""
        df = df.copy()
        delta = df[column].diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        # Handle division by zero
        rs = rs.replace([np.inf, -np.inf], 100.0) 
        
        df[f'RSI_{window}'] = np.where(loss == 0, 100, 100 - (100 / (1 + rs)))
        return df

    @staticmethod
    def add_macd(df: pd.DataFrame, column: str = 'Close') -> pd.DataFrame:
        """Moving Average Convergence Divergence"""
        df = df.copy()
        ema_12 = df[column].ewm(span=12, adjust=False).mean()
        ema_26 = df[column].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema_12 - ema_26
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        return df

