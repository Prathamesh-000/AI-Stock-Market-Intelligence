import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import logging

logger = logging.getLogger(__name__)

class DriftDetector:
    """
    Monitors Data Drift (changes in input features) and Concept Drift (changes in market regime).
    If drift is detected, it signals that the AI needs to be retrained.
    """
    def __init__(self, p_value_threshold: float = 0.05):
        self.p_value_threshold = p_value_threshold
        
    def detect_feature_drift(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, features: list) -> dict:
        """
        Uses the Kolmogorov-Smirnov (KS) test to check if the statistical distribution 
        of live features has diverged from the training features.
        """
        drift_report = {}
        drift_detected = False
        
        for feature in features:
            if feature not in reference_data.columns or feature not in current_data.columns:
                continue
                
            ref_values = reference_data[feature].dropna()
            cur_values = current_data[feature].dropna()
            
            if len(ref_values) == 0 or len(cur_values) == 0:
                continue
                
            # KS Test: p-value < threshold means the distributions are fundamentally different
            statistic, p_value = ks_2samp(ref_values, cur_values)
            
            is_drifting = p_value < self.p_value_threshold
            if is_drifting:
                drift_detected = True
                
            drift_report[feature] = {
                "is_drifting": is_drifting,
                "p_value": p_value,
                "statistic": statistic
            }
            
        return {
            "drift_detected": drift_detected,
            "feature_details": drift_report
        }

    def detect_concept_drift(self, recent_win_rate: float, historical_win_rate: float, threshold: float = 10.0) -> bool:
        """
        Detects Concept Drift (Market Regime Change). 
        If the live win rate drops significantly below the backtested win rate, the market has changed.
        """
        drop = historical_win_rate - recent_win_rate
        if drop > threshold:
            logger.warning(f"🚨 CONCEPT DRIFT DETECTED: Win rate dropped by {drop:.2f}% (Threshold: {threshold}%)")
            return True
        return False
