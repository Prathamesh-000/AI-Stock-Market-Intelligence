import numpy as np
import pandas as pd
import logging
import joblib
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)

class ConfidenceCalibrator:
    """
    Calibrates the raw probabilities of a Machine Learning model using Platt Scaling (Logistic Regression).
    This ensures that when the model says "80% confident", it actually has an 80% accuracy rate historically.
    """
    
    def __init__(self, method: str = 'sigmoid'):
        self.calibrator = LogisticRegression()
        self.model = None
        
    def fit(self, model, X_val: pd.DataFrame, y_val: pd.Series):
        """
        Fits the calibrator using a pre-fitted model and a validation dataset.
        """
        logger.info("Fitting Probability Calibrator (Platt Scaling) on validation set...")
        self.model = model
        
        # Get raw probabilities from the validation set
        raw_probs = self.model.predict_proba(X_val)[:, 1].reshape(-1, 1)
        
        # Train a simple Logistic Regression to map raw_probs -> true y_val
        try:
            self.calibrator.fit(raw_probs, y_val)
            logger.info("Calibration complete.")
        except ValueError as e:
            logger.warning(f"Calibration skipped due to small dataset issue: {e}. Falling back to uncalibrated probabilities.")
            self.calibrator = None
        
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Returns perfectly calibrated probabilities for the positive class (1 / UP).
        """
        if self.model is None:
            logger.error("Calibrator is not fitted yet!")
            return np.zeros(len(X))
            
        # Get raw probabilities
        raw_probs = self.model.predict_proba(X)[:, 1].reshape(-1, 1)
        
        # If calibration failed (due to small dataset), just return raw probabilities
        if self.calibrator is None:
            return raw_probs.flatten()
            
        # Calibrate
        calibrated_probs = self.calibrator.predict_proba(raw_probs)[:, 1]
        return calibrated_probs
        
    def filter_actionable_trades(self, probabilities: np.ndarray, lower_threshold: float = 0.40, upper_threshold: float = 0.60) -> dict:
        """
        Takes an array of probabilities and categorizes them into Actionable vs Uncertain.
        If prob > upper_threshold: BUY
        If prob < lower_threshold: SELL
        Else: UNCERTAIN
        """
        total = len(probabilities)
        
        buy_signals = np.sum(probabilities > upper_threshold)
        sell_signals = np.sum(probabilities < lower_threshold)
        uncertain = total - buy_signals - sell_signals
        
        actionable_pct = ((buy_signals + sell_signals) / total) * 100 if total > 0 else 0
        
        return {
            "Total_Events": total,
            "Actionable_Buys": int(buy_signals),
            "Actionable_Sells": int(sell_signals),
            "Uncertain_Ignored": int(uncertain),
            "Actionable_Percentage": round(actionable_pct, 2)
        }
        
    def save(self, filepath: str):
        if self.calibrator:
            joblib.dump(self.calibrator, filepath)
            logger.info(f"Calibrator saved to {filepath}")
