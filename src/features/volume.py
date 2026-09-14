import pandas as pd
import numpy as np

class VolumeFeatures:
    """
    Analyzes trading volume anomalies and momentum.
    """
    
    @staticmethod
    def add_relative_volume(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """Relative Volume (RVOL) - Ratio of current volume to historical average"""
        df = df.copy()
        
        # Calculate moving average of volume
        df[f'Vol_SMA_{window}'] = df['Volume'].rolling(window=window).mean()
        
        # RVOL = Current Volume / Average Volume
        df[f'RVOL_{window}'] = df['Volume'] / df[f'Vol_SMA_{window}']
        
        # Fill infs if average volume was 0
        df[f'RVOL_{window}'] = df[f'RVOL_{window}'].replace([np.inf, -np.inf], 0)
        return df
        
    @staticmethod
    def add_volume_trend(df: pd.DataFrame) -> pd.DataFrame:
        """Calculates if volume is increasing or decreasing"""
        df = df.copy()
        df['Vol_Change_Pct'] = df['Volume'].pct_change() * 100
        # A simple boolean flag if today's volume is greater than yesterday's
        df['Vol_Increasing'] = (df['Volume'] > df['Volume'].shift(1)).astype(int)
        return df
