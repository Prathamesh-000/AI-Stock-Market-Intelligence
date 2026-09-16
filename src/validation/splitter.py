import pandas as pd
import logging

logger = logging.getLogger(__name__)

class TimeSeriesSplitter:
    """
    Splits the dataset into Train and Test sets strictly by time,
    and applies an 'Embargo' (Purge) window to prevent rolling averages from leaking.
    """
    
    @staticmethod
    def purged_split(df: pd.DataFrame, test_size: float = 0.2, purge_days: int = 20, time_col: str = 'market_reaction_time'):
        """
        Splits dataframe into Train and Test sets.
        Deletes 'purge_days' worth of rows between Train and Test to prevent
        data bleeding from rolling features (like a 20-day SMA).
        """
        df = df.copy()
        df[time_col] = pd.to_datetime(df[time_col])
        df = df.sort_values(time_col)
        
        total_rows = len(df)
        train_end_idx = int(total_rows * (1 - test_size))
        
        # Split conceptually
        train_df = df.iloc[:train_end_idx]
        test_df = df.iloc[train_end_idx:]
        
        # Apply Purge Window
        # We must drop rows from the beginning of the test set that overlap in time
        # with the rolling indicators of the train set.
        train_end_date = train_df[time_col].max()
        
        # Calculate the embargo cutoff date
        purge_cutoff = train_end_date + pd.Timedelta(days=purge_days)
        
        original_test_size = len(test_df)
        
        # Keep only test data strictly AFTER the purge cutoff
        test_df = test_df[test_df[time_col] > purge_cutoff]
        
        purged_amount = original_test_size - len(test_df)
        
        logger.info(f"Time-Series Split: {len(train_df)} Train | {len(test_df)} Test")
        logger.info(f"Purged {purged_amount} rows between Train/Test to prevent leakage (Embargo: {purge_days} days).")
        
        return train_df, test_df
