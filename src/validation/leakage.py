import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class LeakageDetector:
    """
    Analyzes the Feature Matrix to ensure there is no Data Leakage or Lookahead Bias.
    """
    
    @staticmethod
    def check_target_leakage(df: pd.DataFrame, target_col: str, threshold: float = 0.95) -> list:
        """
        Checks if any feature has an impossibly high correlation with the target.
        A correlation > 0.95 usually means the feature accidentally contains the target data.
        """
        leaks = []
        # Only check numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        if target_col not in numeric_df.columns:
            logger.error(f"Target column '{target_col}' not found or not numeric.")
            return leaks
            
        correlations = numeric_df.corrwith(numeric_df[target_col]).abs()
        
        for col, corr in correlations.items():
            if col != target_col and corr > threshold:
                leaks.append(col)
                logger.warning(f"🚨 POTENTIAL LEAK: '{col}' has {corr:.2f} correlation with '{target_col}'")
                
        if not leaks:
            logger.info("✅ Target Leakage Check Passed: No impossibly high correlations found.")
            
        return leaks

    @staticmethod
    def check_chronological_order(df: pd.DataFrame, time_col: str = 'market_reaction_time') -> bool:
        """
        Ensures the dataset is strictly ordered by time, which is mandatory for Time-Series ML.
        """
        if time_col not in df.columns:
            logger.error(f"Time column '{time_col}' not found.")
            return False
            
        # Convert to datetime just in case
        times = pd.to_datetime(df[time_col])
        
        # Check if the array is perfectly sorted
        is_sorted = times.is_monotonic_increasing
        
        if is_sorted:
            logger.info("✅ Chronological Check Passed: Data is perfectly ordered forward in time.")
        else:
            logger.error("🚨 LOOKAHEAD BIAS DETECTED: Time column is not strictly increasing.")
            
        return is_sorted
        
    @staticmethod
    def check_missing_targets(df: pd.DataFrame, target_col: str) -> bool:
        """
        Checks if the target column has NaNs (which would break model training).
        """
        missing = df[target_col].isna().sum()
        if missing > 0:
            logger.warning(f"🚨 Target Missing: '{target_col}' has {missing} NaN values.")
            return False
        else:
            logger.info("✅ Target Integrity Passed: No missing values in target column.")
            return True
