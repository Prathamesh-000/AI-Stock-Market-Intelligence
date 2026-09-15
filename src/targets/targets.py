import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class TargetCreator:
    """
    Calculates the true market reaction (Targets / y-variables) following a news event.
    """
    
    @staticmethod
    def calculate_abnormal_return(df: pd.DataFrame, target_prefix: str = 'SPY') -> pd.DataFrame:
        """
        Calculates the Cumulative Abnormal Return (CAR) for the period following the event.
        We look at the 'Close' vs 'Open' of the reaction day (or next N days).
        Because we shifted timestamps in Phase 2, the 'reaction date' is the exact bar the market trades on.
        """
        df = df.copy()
        
        # Calculate daily forward return: (Close tomorrow - Close today) / Close today
        # Since we want to know what happened *after* the news broke, we look at the forward return.
        # df['Close'].shift(-1) gives us tomorrow's close.
        df['Fwd_Ret_1d'] = df['Close'].shift(-1) / df['Close'] - 1
        
        if f'Close_{target_prefix}' in df.columns:
            df[f'Fwd_Ret_1d_{target_prefix}'] = df[f'Close_{target_prefix}'].shift(-1) / df[f'Close_{target_prefix}'] - 1
            # CAR = Stock Forward Return - Benchmark Forward Return
            df['CAR_1d'] = df['Fwd_Ret_1d'] - df[f'Fwd_Ret_1d_{target_prefix}']
        else:
            # If no benchmark is provided, CAR is just absolute return
            df['CAR_1d'] = df['Fwd_Ret_1d']
            
        return df

    @staticmethod
    def calculate_impact_score(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates a 0-100 Impact Magnitude Score.
        Combines Absolute CAR and Relative Volume.
        """
        df = df.copy()
        
        if 'CAR_1d' not in df.columns or 'RVOL_20' not in df.columns:
            logger.warning("Missing CAR or RVOL columns. Cannot calculate Impact Score.")
            return df
            
        # We care about magnitude, so we take absolute value of CAR
        abs_car = np.abs(df['CAR_1d'])
        
        # Scale CAR (Assume 5% abnormal return is highly significant, cap at 10%)
        # 0.05 return -> 50 score, 0.10 return -> 100 score
        car_score = np.clip(abs_car * 1000, 0, 100)
        
        # Volume Multiplier (If RVOL > 1, institutional validation exists)
        # Cap RVOL multiplier at 2.0 to prevent absurd volume from skewing
        vol_multiplier = np.clip(df['RVOL_20'], 0.5, 2.0)
        
        raw_impact = car_score * vol_multiplier
        
        # Final normalization to 0-100
        df['Impact_Score'] = np.clip(raw_impact, 0, 100).round(2)
        
        return df

    @staticmethod
    def calculate_direction(df: pd.DataFrame, threshold: float = 0.005) -> pd.DataFrame:
        """
        Calculates categorical Direction Label based on CAR.
        1 (UP), -1 (DOWN), 0 (NEUTRAL).
        Threshold prevents noise (e.g., 0.005 = 0.5% abnormal return required to trigger).
        """
        df = df.copy()
        
        if 'CAR_1d' not in df.columns:
            return df
            
        conditions = [
            (df['CAR_1d'] > threshold),
            (df['CAR_1d'] < -threshold)
        ]
        choices = [1, -1]
        
        df['Direction'] = np.select(conditions, choices, default=0)
        
        return df
