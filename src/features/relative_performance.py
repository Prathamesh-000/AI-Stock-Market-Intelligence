import pandas as pd
import numpy as np

class RelativePerformance:
    """
    Calculates how the target stock is performing relative to benchmarks (SPY, XLK).
    """
    
    @staticmethod
    def calculate_relative_strength(
        df_stock: pd.DataFrame, 
        df_benchmark: pd.DataFrame, 
        window: int = 20,
        prefix: str = 'SPY'
    ) -> pd.DataFrame:
        """
        Calculates rolling relative performance (Alpha) of stock vs benchmark.
        Assumes both dataframes have 'Timestamp' and 'Close' columns and are sorted.
        """
        # Ensure we don't mutate original
        stock = df_stock.copy()
        bench = df_benchmark.copy()
        
        # Merge on Timestamp to ensure perfect alignment
        merged = pd.merge(
            stock[['Timestamp', 'Close']], 
            bench[['Timestamp', 'Close']], 
            on='Timestamp', 
            how='left', 
            suffixes=('', f'_{prefix}')
        )
        
        # Calculate daily returns
        merged['Ret'] = merged['Close'].pct_change()
        merged[f'Ret_{prefix}'] = merged[f'Close_{prefix}'].pct_change()
        
        # Calculate rolling cumulative returns over the window
        # (1 + r).cumprod() - 1 formula for small windows approximated by sum for speed, 
        # but exact product is better for accuracy.
        
        # Rolling Alpha = Stock Return - Benchmark Return
        merged[f'Alpha_{prefix}'] = merged['Ret'] - merged[f'Ret_{prefix}']
        
        # Rolling cumulative Alpha over N days
        merged[f'Cum_Alpha_{prefix}_{window}'] = merged[f'Alpha_{prefix}'].rolling(window=window).sum()
        
        # A simple ratio of stock price to benchmark price (normalized to 1 at start of window)
        # This shows if the stock is trending harder than the market
        merged[f'RS_Ratio_{prefix}'] = merged['Close'] / merged[f'Close_{prefix}']
        
        # Return just the new columns attached to Timestamp
        cols_to_keep = ['Timestamp', f'Alpha_{prefix}', f'Cum_Alpha_{prefix}_{window}', f'RS_Ratio_{prefix}']
        return merged[cols_to_keep]
