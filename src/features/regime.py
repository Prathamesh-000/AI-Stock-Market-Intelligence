import pandas as pd
import numpy as np

class MarketRegime:
    """
    Determines if the broader market is in a Bull, Bear, or Choppy regime.
    This context helps the NLP engine understand how news might be received.
    """
    
    @staticmethod
    def detect_regime(df_benchmark: pd.DataFrame, fast_window: int = 50, slow_window: int = 200) -> pd.DataFrame:
        """
        Uses SMA cross logic on a benchmark (like SPY) to determine macro regime.
        Returns a dataframe with a 'Market_Regime' column aligned to the index.
        Regimes: 1 (Bull), -1 (Bear), 0 (Transition/Choppy)
        """
        df = df_benchmark.copy()
        
        df[f'SMA_{fast_window}'] = df['Close'].rolling(window=fast_window).mean()
        df[f'SMA_{slow_window}'] = df['Close'].rolling(window=slow_window).mean()
        
        # Bull = Fast > Slow AND Price > Fast
        # Bear = Fast < Slow AND Price < Fast
        # Otherwise = Choppy
        
        conditions = [
            (df[f'SMA_{fast_window}'] > df[f'SMA_{slow_window}']) & (df['Close'] > df[f'SMA_{fast_window}']),
            (df[f'SMA_{fast_window}'] < df[f'SMA_{slow_window}']) & (df['Close'] < df[f'SMA_{fast_window}'])
        ]
        choices = [1, -1]
        
        df['Market_Regime'] = np.select(conditions, choices, default=0)
        
        # Return only the relevant columns to be merged back into the main stock data
        if 'Timestamp' in df.columns:
            return df[['Timestamp', 'Market_Regime']]
        return df[['Market_Regime']]

